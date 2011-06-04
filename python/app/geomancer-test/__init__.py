import sys
import os
path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))).replace('app/geomancer-test', 'app')
sys.path.append(path)
print sys.path

import geomancer
import logging
import unittest
import simplejson

class TestGeomancer(unittest.TestCase):
    def test_headings(self):
        headings = geomancer.constants.Headings.all()
        for heading in headings:
            logging.info(heading)

    def test_datums(self):
        datums = geomancer.constants.Datums.all()
        for datum in datums:
            logging.info(datum)

    def test_georef(self):
        geocode = simplejson.loads("""{
       "results" : [
          {
             "address_components" : [
                {
                   "long_name" : "Mountain View",
                   "short_name" : "Mountain View",
                   "types" : [ "locality", "political" ]
                },
                {
                   "long_name" : "San Jose",
                   "short_name" : "San Jose",
                   "types" : [ "administrative_area_level_3", "political" ]
                },
                {
                   "long_name" : "Santa Clara",
                   "short_name" : "Santa Clara",
                   "types" : [ "administrative_area_level_2", "political" ]
                },
                {
                   "long_name" : "California",
                   "short_name" : "CA",
                   "types" : [ "administrative_area_level_1", "political" ]
                },
                {
                   "long_name" : "United States",
                   "short_name" : "US",
                   "types" : [ "country", "political" ]
                }
             ],
             "formatted_address" : "Mountain View, CA, USA",
             "geometry" : {
                "bounds" : {
                   "northeast" : {
                      "lat" : 37.4698870,
                      "lng" : -122.0446720
                   },
                   "southwest" : {
                      "lat" : 37.35654100000001,
                      "lng" : -122.1178620
                   }
                },
                "location" : {
                   "lat" : 37.38605170,
                   "lng" : -122.08385110
                },
                "location_type" : "APPROXIMATE",
                "viewport" : {
                   "northeast" : {
                      "lat" : 37.42150620,
                      "lng" : -122.01982140
                   },
                   "southwest" : {
                      "lat" : 37.35058040,
                      "lng" : -122.14788080
                   }
                }
             },
             "types" : [ "locality", "political" ]
          }
       ],
       "status" : "OK"
    }""")
        logging.info(georeference(geocode))

    def test_point2wgs84(self):
        agd66point = Point(144.966666667, -37.8)
        wgs84point = point2wgs84(agd66point, Datums.AGD84)
        logging.info(wgs84point)
        logging.info(Datums.AGD84)
    #    144.96797984155188, -37.798491994062296
    #    144.96798640000000, -37.798480400000000

    def test_distanceprecision(self):
        d = '110'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        
        d = '0'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        d = '1'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '2'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '5'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '9'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '11'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '12'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '19'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '20'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '21'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '49'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '50'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '51'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '99'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '100'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '101'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '109'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '110'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '111'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '149'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '150'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '151'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '199'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '200'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '201'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '210'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '999'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '1000'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        
        d = '10.000'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.001'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.00'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.01'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.0'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.1'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.9'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.125'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.25'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.3333'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.5'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.625'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.75'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.5'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.66667'
        p = getDistancePrecision(d)
        logging.info(d+" "+str(p))
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

