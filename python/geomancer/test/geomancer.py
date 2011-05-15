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

"""This module provides unit testing for the geomancer module."""

# Python module imports:
import logging
import os
import sys
import unittest
import math

# Updates sys.path to include geomancer source:
sys.path = [os.path.abspath(os.path.realpath('../src'))] + sys.path

# Geomancer module imports:
import geomancer
from geomancer import Point, MetersPerDegree, PaperMap, point2wgs84
from geomancer.constants import Datums, DistanceUnit, convert_distance

# class DistanceConversionTest(unittest.TestCase):
#     def test_convert(self):
#         val = convert_distance(1, DistanceUnit.KILOMETER, DistanceUnit.MILE)        
#         logging.info('Val = ' + str(val))
#         self.assertEqual(val, 1)

# class PointTest(unittest.TestCase):
#     def test_init(self):
#         pass

# class MetersPerDegreeTest(unittest.TestCase):
#     def test_init(self):
#         pass

# class PaperMapTest(unittest.TestCase):
#     pass
#     def test_getpoint(self):
#         corner = Point(1, 2)
#         for unit in DistanceUnit.all():
#             for datum in Datums.all():
#                 papermap = PaperMap(unit, datum)
#                 point = papermap.getpoint(corner, ndist=1, edist=1)
#                 backagain = papermap.getpoint(point, sdist=1, wdist=1)
#                 self.assertEqual(corner.lat,backagain.lat)
#                 self.assertEqual(corner.lng,backagain.lng)

class DatumTest(unittest.TestCase):
    def test_datum(self):
        logging.info(Datums.AGD84)
        logging.info(Datums.fromcode('AGD84'))
        logging.info(Datums.codes())
        for d in Datums.all():
            logging.info(d)
        logging.info('Datum with EPSG code 7001: ' + str(Datums.fromepsgcode(7001)))

class Point2WGS84Test(unittest.TestCase):
    def test_point2wgs84(self):
        agd66point = Point(144.966666667, -37.8)
        wgs84point = point2wgs84(agd66point, Datums.AGD84)
        logging.info(wgs84point)
        logging.info(Datums.AGD84)
        self.assertTrue(math.fabs(-37.798480353567406 - wgs84point.lat) < 1e-7)
        self.assertTrue(math.fabs(144.96798635963754 - wgs84point.lng) < 1e-7)

# class DistanceUnitTest(unittest.TestCase):
#     def test_distanceunit(self):
#         logging.info(DistanceUnit.METER)
#         logging.info(DistanceUnit.units())
#         for d in DistanceUnit.all():
#             logging.info(d)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
    Point2WGS84Test.test_point2wgs84()
