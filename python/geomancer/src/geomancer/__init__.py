#!/usr/bin/env python

# Copyright 2011 University of California at Berkeley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = "Aaron Steele and John Wieczorek"

"""This module provides classes for calculating georeferencing errors."""

import copy
import math

from constants import *

class LatLng(object):
    
    @staticmethod
    def degrees_from_dms(d, m, s):
        return math.fabs(s / 3600.0) + math.fabs(m / 60.0) + math.fabs(d)

    @staticmethod
    def degrees_from_dm(d, m):
        return math.fabs(m / 60.0) + math.fabs(d)
    
    @staticmethod
    def lat_from_dms(d, m, s, direction):
        lat = LatLng.degress_from_dms(d, m, s)
        if direction is Direction.SOUTH:
            lat = -lat
        return lat

    @staticmethod
    def lng_from_dms(lngdeg, lngmin, lngsec, lngdir):
        lng = LatLng.degress_from_dms(d, m, s)
        if direction is Directions.WEST:
            lng = -lng
        return lng
    
    def __init__(self, lng, lat):
        self._lng = lng
        self._lat = lat
        
    def getlng(self):
        return self._lng
    lng = property(fget=getlng)

    def getlat(self):
        return self._lat
    lat = property(fget=getlat)

    def valid(self):
        return self.lat >= -90 and self.lat <= 90 \
            and self.lng >= -180 and self.lng <= 180

    def __str__(self):
        return str(self.__dict__)

class Coordinates(object):
    
    def __init__(self, config):
        self._config = copy.copy(config)
        
    def get_datum(self):
        return self._config.get('datum')
    datum = property(fget=get_datum)
            
    def get_point(self):
        return self._config.get('point')
    point = property(fget=get_point)

    def get_source(self):
        return self._config.get('source')
    source = property(fget=get_source)

    def get_system(self):
        return self._config.get('system')
    system = property(fget=get_system)

    def get_unit(self):
        return self._config.get('unit')
    unit = property(fget=get_unit)

if __name__ == '__main__':
    c = Coordinates({'point': LatLng(1, 2)})
    print c.point

