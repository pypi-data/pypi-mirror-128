#!/usr/bin/env python

'''
extract ISBH and ISBD messages from AP_Logging files and produce APSD plots
See https://blog.endaq.com/why-the-power-spectral-density-psd-is-the-gold-standard-of-vibration-analysis
'''

import numpy
import os
import pylab
import sys
import time

from pymavlink import mavutil
from MAVProxy.modules.lib.multiproc_util import MPDataLogChildTask

class MavPSD(MPDataLogChildTask):
    '''A class used to launch a PSD display in a child process'''

    def __init__(self, *args, **kwargs):
        '''
        Parameters
        ----------
        mlog : DFReader
            A dataflash or telemetry log
        xlimits: MAVExplorer.XLimits
            An object capturing timestamp limits
        '''

        super(MavPSD, self).__init__(*args, **kwargs)

        # all attributes are implicitly passed to the child process 
        self.xlimits = kwargs['xlimits']

    # @override
    def child_task(self):
        '''Launch `mavpsd_display`'''

        # run the psd tool
        mavpsd_display(self.mlog, self.xlimits.timestamp_in_range)

def mavpsd_display(mlog, timestamp_in_range):
    '''display PSD for raw ACC data from ISBD in logfile'''

    '''object to store data about a single PSD plot'''
    class PlotData(object):
        def __init__(self, psdh):
            self.seqno = -1
            self.psdnum = psdh.N
            self.sensor_type = psdh.type
            self.instance = psdh.instance
            self.sample_rate_hz = psdh.smp_rate
            self.multiplier = psdh.mul
            self.data = {}
            self.data["X"] = []
            self.data["Y"] = []
            self.data["Z"] = []
            self.holes = False
            self.freq = None

        def add_psdd(self, psdd):
            if psdd.N != self.psdnum:
                print("Skipping ISBD with wrong psdnum (%u vs %u)\n" % (psdd.psdnum, self.psdnum))
                return
            if self.holes:
                print("Skipping ISBD(%u) for ISBH(%u) with holes in it" % (psdd.seqno, self.psdnum))
                return
            if psdd.seqno != self.seqno+1:
                print("ISBH(%u) has holes in it" % psdd.N)
                self.holes = True
                return
            self.seqno += 1
            self.data["X"].extend(psdd.x)
            self.data["Y"].extend(psdd.y)
            self.data["Z"].extend(psdd.z)

        def prefix(self):
            if self.sensor_type == 0:
                return "Accel"
            elif self.sensor_type == 1:
                return "Gyro"
            else:
                return "?Unknown Sensor Type?"

        def tag(self):
            return str(self)

        def __str__(self):
            return "%s[%u]" % (self.prefix(), self.instance)

    print("Processing log for ISBH and ISBD messages")

    things_to_plot = []
    plotdata = None
    start_time = time.time()
    mlog.rewind()

    while True:
        m = mlog.recv_match(type=['ISBH','ISBD'])
        if m is None:
            break
        in_range = timestamp_in_range(m._timestamp)
        if in_range < 0:
            continue
        if in_range > 0:
            break
        msg_type = m.get_type()
        if msg_type == "ISBH":
            if plotdata is not None:
                # close off previous data collection
                things_to_plot.append(plotdata)
            # initialise plot-data collection object
            plotdata = PlotData(m)
            continue

        if msg_type == "ISBD":
            if plotdata is None:
                continue
            plotdata.add_psdd(m)

    if len(things_to_plot) == 0:
        print("No PSD data. Did you set INS_LOG_BAT_MASK?")
        return
    time_delta = time.time() - start_time
    print("Extracted %u psd data sets" % len(things_to_plot))

    sum_psd = {}
    freqmap = {}
    count = 0

    first_freq = None
    for thing_to_plot in things_to_plot:
        for axis in [ "X","Y","Z" ]:
            d = numpy.array(thing_to_plot.data[axis])/float(thing_to_plot.multiplier)
            if len(d) == 0:
                print("No data?!?!?!")
                continue
            
            avg = numpy.sum(d) / len(d)
            d -= avg
            d_psd = numpy.psd.rpsd(d)
            if thing_to_plot.tag() not in sum_psd:
                sum_psd[thing_to_plot.tag()] = {
                    "X": 0,
                    "Y": 0,
                    "Z": 0
                }
            sum_psd[thing_to_plot.tag()][axis] = numpy.add(sum_psd[thing_to_plot.tag()][axis], d_psd)
            count += 1
            freq = numpy.psd.rpsdfreq(len(d), 1.0/thing_to_plot.sample_rate_hz)
            freqmap[thing_to_plot.tag()] = freq

    for sensor in sum_psd:
        pylab.figure(str(sensor))
        for axis in [ "X","Y","Z" ]:
            pylab.plot(freqmap[sensor], numpy.abs(sum_psd[sensor][axis]/count), label=axis)
        pylab.legend(loc='upper right')
        pylab.xlabel('Hz')

    pylab.show()
