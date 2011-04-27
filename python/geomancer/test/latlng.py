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

"""This module provides unit testing for the LatLng class."""

# Python module imports:
import logging
import os
import sys
import unittest

# Updates sys.path to include geomancer source:
sys.path = [os.path.abspath(os.path.realpath('../src'))] + sys.path

# Geomancer module imports:
from geomancer import LatLng

class LatLngTest(unittest.TestCase):
    """Provides unit testing for FieldType class."""
    
    def test_degrees_from_dms(self):
        lat = LatLng.degrees_from_dms(1, 2, 3)
        #self.assertTrue(lat == 12)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
