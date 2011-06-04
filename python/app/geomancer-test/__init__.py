import sys
import os
path = os.path.abspath(os.path.dirname(os.path.realpath(__file__))).replace('app/geomancer-test', 'app')
sys.path.append(path)
print sys.path

import geomancer
from geomancer import Point
from geomancer import Datums
import math
import logging
import unittest
import simplejson

class TestGeomancer(unittest.TestCase):
    
    def test_distanceunits(self):
        distunits = geomancer.constants.DistanceUnits.all()
        for unit in distunits:
            logging.info(unit)

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
        logging.info(geomancer.georef_feature(geocode))

    def test_point2wgs84(self):
        agd66point = Point(144.966666667, -37.8)
        wgs84point = geomancer.point2wgs84(agd66point, Datums.AGD84)
        logging.info(wgs84point)
        logging.info(Datums.AGD84)
    #    144.96797984155188, -37.798491994062296
    #    144.96798640000000, -37.798480400000000

    def test_distanceprecision(self):
        d = '110'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        
        d = '0'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        d = '1'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '2'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '5'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '9'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '11'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '12'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '19'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '20'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '21'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '49'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '50'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '51'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '99'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '100'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '101'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '109'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '110'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '111'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '149'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '150'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '151'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '199'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '200'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '201'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '210'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '999'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '1000'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
    
        
        d = '10.000'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.001'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.00'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.01'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.0'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.1'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.9'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.125'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.25'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.3333'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '10.5'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.625'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.75'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.5'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        d = '0.66667'
        p = geomancer.getDistancePrecision(d)
        logging.info(d+" "+str(p))
        
    def test_georeference_feature(self):
        geocode = get_example_geocode()
        georef = geomancer.georef_feature(geocode)
        logging.info('Georeference: %s'%(georef))
    
    def test_point_from_dist_at_bearing(self):
        point = Point(0,0)
        distance = 1000000
        bearing = 45 
        endpoint = geomancer.get_point_from_distance_at_bearing(point, distance, bearing)
        logging.info("%s meters at bearing %s from %s, %s: %s"%(distance, bearing, point.lng, point.lat, endpoint) )
        
    def test_haversine_distance(self):
        point = Point(0,0)
        distance = 1000000
        bearing = 45 
        endpoint = geomancer.get_point_from_distance_at_bearing(point, distance, bearing)
        hdist = geomancer.haversine_distance(point, endpoint)
        logging.info("%s meters"%(hdist) )
        diff = math.fabs(distance - hdist) 
        if diff >= 0.5:
            logging.info("FAIL: test_haversine_distance(): difference = %s meters"%(diff) )
        else:
            logging.info("PASS: test_haversine_distance(): difference = %s meters"%(diff) )        

def get_example_geocode():
    """Returns an Google Geocoding JSON response for "Mountain View"."""
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
    return geocode

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

