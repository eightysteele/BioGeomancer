import sys
import os
path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))).replace('app/geomancer-test', 'app')
sys.path.append(path)
print sys.path

import geomancer
import logging
import unittest

class TestGeomancer(unittest.TestCase):
    def test_headings(self):
        headings = geomancer.constants.Headings.all()
        for heading in headings:
            logging.info(heading)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

