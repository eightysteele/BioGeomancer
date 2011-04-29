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

import math

import constants import convert_distance
import constants import DistanceUnit

class Point(object):
    def __init__(self, lng, lat):
        self._lng = lng
        self._lat = lat

    def getlng(self):
        return self._lng
    lng = property(getlng)

    def getlat(self):
        return self._lat
    lat = property(getlat)

    def isvalid(self):
        pass

    def __str__(self):
        return str(self.__dict__)

class MetersPerDegree(object):
    def __init__(self, point, datum):
        self._point = point
        self._datum = datum
        self._calculate()

    def getpoint(self):
        return self._point
    point = property(getpoint)

    def getdatum(self):
        return self._datum
    datum = property(getdatum)

    def getmlat(self):
        return self._mlat
    mlat = property(getmlat)

    def getmlng(self):
        return self._mlng
    mlng = property(getmlng)
    
    def _calculate(self):
        d = self._datum
        p = self._point
        a = d.axis
        f = d.flattening
        e = 2.0 * f - math.pow(f, 2.0)
        lat = p.lat
        
        # Radius of curvature in the prime vertical:
        n = a / math.sqrt(1.0 -e * (math.pow(math.sin(lat * math.pi / 180.0), 2.0)))

        # Radius of curvature in the prime meridian:
        m = a * (1.0 - e) / math.pow(1.0 - e * math.pow(math.sin(lat * math.pi / 180.0), 2.0), 1.5)

        # Orthogonal distance to the polar axis
        x = n * math.cos(lat * math.pi / 180.0) * 1.0

        self._mlat = math.pi * m / 180.0
        self._mlng = math.pi * x / 180.0
                          

class PaperMap(object):
    def __init__(self, unit, datum):
        self._unit = unit
        self._datum = datum

    def getunit(self):
        return self._unit
    unit = property(getunit)

    def getdatum(self):
        return self._datum
    datum = property(getdatum)

    def getpoint(self, corner, ndist=None, sdist=None, edist=None, wdist=None):
        # TODO: Calculations should be based on great circles.

        if (not ndist and not sdist) or (not edist and not wdist):
            return None
        
        mpd = MetersPerDegree(corner, self.datum)

        # Calculates latitude delta:
        if ndist:
            distmeters = convert_distance(ndist, self.unit, DistanceUnit.METER)
            latdelta = distmeters / mpd.mlat
        else:
            distmeters = convert_distance(sdist, self.unit, DistanceUnit.METER)
            latdelta = -(distmeters / mpd.mlat)
        
        # Calculates longitude delta:
        if edist:
            distmeters = convert_distance(edist, self.unit, DistanceUnit.METER)
            lngdelta = distmeters / mpd.mlng
        else:
            distmeters = convert_distance(wdist, self.unit, DistanceUnit.METER)
            lngdelta = -(distmeters / mpd.mlng)

        # Calulates point latitude:
        lat = corner.lat + latdelta
        lat = 1.0 * math.round(lat * 10000000.0) / 10000000.0

        # Calculates point longitude:
        lng = cornder.lng + lngdelta
        lng = 1.0 * math.round(lng * 10000000) / 10000000

        return Point(lng, lat)


        
