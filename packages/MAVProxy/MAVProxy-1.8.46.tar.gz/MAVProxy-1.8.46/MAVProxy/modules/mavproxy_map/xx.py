#!/usr/bin/env python3

# https://cfis.savagexi.com/2006/05/03/google-maps-deconstructed/

import math
from math import *

from MAVProxy.modules.lib import mp_util
from math import log, tan, radians, degrees, sin, cos, exp, pi, asin, atan

def coord_from_area(x, y, lat, lon, width, ground_width):
    '''return (lat,lon) for a pixel in an area image
    x is pixel coord to the right from top,left
    y is pixel coord down from top left
    '''
    scale1 = mp_util.constrain(cos(radians(lat)), 1.0e-15, 1)
    pixel_width = ground_width / float(width)
    dy = y * pixel_width
    (lat2,lon2) = mp_util.gps_offset(lat, lon, 0, -dy)

     # iterative form for the latitude change. We should replace this with a closed form
     # solution
    pixel_width_equator = (ground_width / float(width)) / cos(radians(lat))
    latr = radians(lat)
    for yi in range(max(0,int(y+0.5))):
        pw = pixel_width_equator * cos(latr)
        dlatr = pw / mp_util.radius_of_earth
        latr -= dlatr
    lat2 = degrees(latr)

    dx = pixel_width_equator * cos(radians(lat2)) * x

    (lat2,lon2) = mp_util.gps_offset(lat2, lon, dx, 0)

    return (lat2,lon2)

def coord_to_pixel(lat, lon, width, ground_width, lat2, lon2):
    '''return pixel coordinate (px,py) for position (lat2,lon2)
    in an area image. Note that the results are relative to top,left
    and may be outside the image
    ground_width is with at lat,lon
    px is pixel coord to the right from top,left
    py is pixel coord down from top left
    '''
    pixel_width_equator = (ground_width / float(width)) / cos(radians(lat))
    epsilon = 1.0e-10
    latr = radians(mp_util.constrain(lat,-90+epsilon,90-epsilon))
    lat2r = radians(mp_util.constrain(lat2,-90+epsilon,90-epsilon))

    C = mp_util.radius_of_earth / pixel_width_equator
    y = C * (log(abs(1.0/cos(latr) + tan(latr))) - log(abs(1.0/cos(lat2r) + tan(lat2r))))
    y = int(y+0.5)

    dx = mp_util.gps_distance(lat2, lon, lat2, lon2)
    if mp_util.gps_bearing(lat2, lon, lat2, lon2) > 180:
        dx = -dx
    x = int(0.5 + dx / (pixel_width_equator * cos(radians(lat2))))
    return (x,y)

def coord_from_area2(x, y, lat, lon, width, ground_width):
    '''return (lat,lon) for a pixel in an area image
    x is pixel coord to the right from top,left
    y is pixel coord down from top left
    '''
    scale1 = mp_util.constrain(cos(radians(lat)), 1.0e-15, 1)
    pixel_width = ground_width / float(width)

    pixel_width_equator = (ground_width / float(width)) / cos(radians(lat))

    latr = radians(lat)
    y0 = abs(1.0/cos(latr) + tan(latr))
    lat2 = 2 * atan(y0 * exp(-(y * pixel_width_equator) / mp_util.radius_of_earth)) - pi/2.0
    lat2 = degrees(lat2)

    dx = pixel_width_equator * cos(radians(lat2)) * x

    (lat2,lon2) = mp_util.gps_offset(lat2, lon, dx, 0)

    return (lat2,lon2)

x0=331
y0=510
lat0=-4.062620387215275
lon0=105.69177392744751
width=600
ground_width=6118864.606628966
lat2=-45.25136746566276
lon2=136.0916320779915
radius_of_earth = 6378100.0 # in meters

(x,y) = coord_to_pixel(lat0,lon0,width, ground_width,lat2,lon2)
print(x,y)

(lat,lon) = coord_from_area(x,y, lat0, lon0, width, ground_width)

print(lat,lon)

(lat,lon) = coord_from_area2(x,y, lat0, lon0, width, ground_width)

print(lat,lon)

