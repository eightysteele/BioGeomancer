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
import logging
import simplejson

from constants import convert_distance
from constants import DistanceUnit
from constants import Datums
'''
A_WGS84 is the radius of the sphere at the equator for the WGS84 datum. 
'''
A_WGS84 = 6378137.0

class Locality(object):

      def __init__(self, loc, loctype=None, parts={}, geocode=None):
          """Constructs a Locality.

          Arguments:
              loc - The string locality (required)
              loctype - The string locality type abbreviation
              parts - A dictionary containing locality parts based on type
              geocode - The raw Google Geocode API response object
          """
          self.loc = loc
          self.loctype = loctype
          self.parts = parts
          self.geocode = geocode

class Point(object):
    def __init__(self, lng, lat):
        self._lng = lng
        self._lat = lat

    def get_lng(self):
        return self._lng
    lng = property(get_lng)

    def get_lat(self):
        return self._lat
    lat = property(get_lat)

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
        f = 1.0/d.flattening
        e = 2.0 * f - math.pow(f, 2.0)
        lat = p.lat
        
        # Radius of curvature in the prime vertical:
        # N is the radius of curvature in the prime vertical. It's tangent to
        # ellipsoid at the latitude: N(lat) = a/(1-e^2*sin^2(lat))^0.5
        n = a / math.sqrt(1.0 -e * (math.pow(math.sin(lat * math.pi / 180.0), 2.0)))

        # Radius of curvature in the prime meridian:
        # M is the radius of curvature in the prime meridian. It's tangent to
        # ellipsoid at the latitude: M(lat) = a(1-e^2)/(1-e^2*sin^2(lat))^1.5
        m = a * (1.0 - e) / math.pow(1.0 - e * math.pow(math.sin(lat * math.pi / 180.0), 2.0), 1.5)

        # Orthogonal distance to the polar axis
        # Longitude is irrelevant for the calculations to follow so simplify by
        # using longitude = 0, such that Y = 0 and X = Ncos(lat)cos(long). Note
        # that long = 0, so cos(long) = 1.0.
        x = n * math.cos(lat * math.pi / 180.0) * 1.0

        self._mlat = math.pi * m / 180.0
        self._mlng = math.pi * x / 180.0
                          
class GeocodeResultParser(object):
    @classmethod
    def get_point(cls, geometry):
        """Assumes geometry exists."""
        return (geometry.get('location').get('lng'), geometry.get('location').get('lat'))
    
    @classmethod
    def get_bounds(cls, geometry):
        """Assumes geometry exists."""
        if geometry.has_key('bounds') == False:
            return None
        return geometry.get('bounds')
    
    @classmethod
    def calc_error(cls, geometry):
        """Assumes geometry exists."""
        bb = get_bounds(geometry) 
        if bb == None:
            """Default error for a feature without a bounds entry is 100m."""
            return 100
        center = get_point(geometry)
        ne = ( bb.get('northeast').get('lng'), bb.get('northeast').get('lat') )
        sw = ( bb.get('southwest').get('lng'), bb.get('southwest').get('lat') )
        distne = haversine_distance(center, ne)
        distsw = haversine_distance(center, sw)
        if distne >= distsw:
            return distne
        return distsw
        
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
        lat = 1.0 * round(lat * 10000000.0) / 10000000.0

        # Calculates point longitude:
        lng = corner.lng + lngdelta
        lng = 1.0 * round(lng * 10000000.0) / 10000000.0

        return Point(lng, lat)

def sqr(x):
    '''Square of x.'''
    return x * x

def lng180(lng):
    '''Given a longitude in degrees, returns a longitude in degrees between {-180, 180].'''
    newlng = float(lng)
    if lng <= -180:
        return lng + 360
    if newlng > 180:
        return lng - 360
    return lng

def haversine_distance(start_lat_lng, end_lat_lng):
    '''
    Returns the distance along a great circle between two lat longs on the surface of a
    sphere of radius SEMI_MAJOR_AXIS using the Haversine formula.
    '''
    dLat = math.radians(end_lat_lng[0] - start_lat_lng[0])
    dLon = math.radians(end_lat_lng[1] - start_lat_lng[1]) 
    '''a is the square of half the chord length between the points.'''
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos( math.radians(start_lat_lng[0]) ) * math.cos( math.radians(end_lat_lng[0]) ) * math.sin(dLon/2) * math.sin(dLon/2)
    '''Account for rounding errors. If a is very close to 1 set it to one to avoid domain exception.'''
    if math.fabs(1-a) < 1e-10:
        a = 1
    '''c is the angular distance in radians between the points.'''
    x = math.sqrt(1-a)
    y = math.sqrt(a)
    c = 2 * math.atan2(y, x)
    return A_WGS84 * c 
    
def point2wgs84(point, datum):
    """Converts a Point in a given datum to a Point in WGS84."""
    '''
    Uses the Abridged Molodensky Transformation.
    See: 
    Deakin, R.E. 2004. THE STANDARD AND ABRIDGED MOLDENSKY COORDINATE TRANSFORMATION FORMULAE. 
    Department of Mathematical and Geospatial Sciences, RMIT University.
    http://user.gs.rmit.edu.au/rod/files/publications/Molodensky%20V2.pdf
    '''
    latr = math.radians(point.lat)
    lngr = math.radians(point.lng)
    
    '''Semi-major axis of given datum.'''
    a = datum.axis
    
    '''Flattening of given datum (get_flattening actually return the inverse flattening).'''
    f = 1.0/datum.flattening
    dx = datum.dx
    dy = datum.dy
    dz = datum.dz
    
    '''Difference in the semi-major axes.'''
    da = Datums.WGS84.axis - a
    
    '''Difference in the flattenings.'''
    df = 1.0/Datums.WGS84.flattening - f
    
    e_squared = f*(2-f)
    rho = a*(1-e_squared)/math.pow((1-e_squared*sqr(math.sin(latr))),1.5)
    nu = a/math.pow((1-e_squared*sqr(math.sin(latr))),0.5)
    dlat = (1/rho)*(-dx*math.sin(latr)*math.cos(lngr) - dy*math.sin(latr)*math.sin(lngr) + dz*math.cos(latr) + (f*da + a*df)*math.sin(2*latr))
    dlng = (-dx*math.sin(lngr) + dy*math.cos(lngr))/(nu*math.cos(latr))
    newlng = lng180(math.degrees(lngr + dlng))
    newlat = math.degrees(latr + dlat)
    return Point(newlng, newlat)

def DatumTransformToWGS84(lng, lat, a, f, dx, dy, dz):
    '''
    Return a lng, lat in WGS84 given a lng, lat, semi-major axis, inverse flattening, and
    cartesian offsets in x, y, z for the original datum. Uses the Abridged Molodensky Transformation.
    See: 
    Deakin, R.E. 2004. THE STANDARD AND ABRIDGED MOLDENSKY COORDINATE TRANSFORMATION FORMULAE. 
    Department of Mathematical and Geospatial Sciences, RMIT University.
    user.gs.rmit.edu.au/rod/files/publications/Molodensky%20V2.pdf
    '''
    F_WGS84 = 1.0/298.257223563 
    latr = math.radians(lat)
    lngr = math.radians(lng)
    da = A_WGS84 - a
    df = F_WGS84 - f
    e_squared = f*(2-f)
    rho = a*(1-e_squared)/math.pow((1-e_squared * math.pow(math.sin(latr), 2)),1.5)
    nu = a/math.pow((1-e_squared * math.pow(math.sin(latr), 2)),0.5)
    dlat = (1/rho)*(-dx*math.sin(latr)*math.cos(lngr) - dy*math.sin(latr)*math.sin(lngr) + dz*math.cos(latr) + (f*da + a*df)*math.sin(2*latr))
    dlng = (-dx*math.sin(lngr) + dy*math.cos(lngr))/(nu*math.cos(latr))
    
    return (lng + math.degrees(dlng), lat + math.degrees(dlat))

def test_point2wgs84():
    agd66point = Point(144.966666667, -37.8)
    wgs84point = point2wgs84(agd66point, Datums.AGD84)
    logging.info(wgs84point)
    logging.info(Datums.AGD84)
#    144.96797984155188, -37.798491994062296
#    144.96798640000000, -37.798480400000000

def test_georef():
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
    logging.info(georef(geocode))
    

def predict(locality):
    """Returns a locality type from Google Prediction API."""
    pass # Aaron

def geocode(locality):
    """Returns a geocode response object from Google Geocode API."""
    pass # Aaron

def georef_feature(geocode, loctype=None):
    """Returns a Georeference from the Geomancer API."""
    status = geocode.get('status')
    if status != 'OK':
        #Geocode failed, no results, no georeference possible.
        return None
    if geocode.get('results')[0].has_key('geometry') == False:
        #First result has no geometry, no georeference possible.
        return None
    g = geocode.get('results')[0].get('geometry')
    point = GeocodeResultParser.get_point(g)
    error = GeocodeResultParser.calc_error(g)
    return Georeference(point, error)
    

class Georeference(object):
    def __init__(self, point, error):
        self.point = point
        self.error = error
    
    def __str__(self):
        return str(self.__dict__)

def georeference(locality):
    """Entry point to georeferencing."""
    if locality.loctype:
        loctype = locality.loctype.lower()
    else:
        loctype = None
    if loctype is None:
        result = locality.geocode.get('results')[0] # TODO handle multiple results
        location = result.get('geometry').get('location')
        point = Point(float(location.get('lat')), float(location.get('lng')))
        if result.get('geometry').get('location_type') is 'ROOFTOP':
            error = 100 # TODO
        else:
            error = 1000 # TODO
        return Georeference(point, error) # TODO 
    elif loctype == 'foh':
        # TODO (John)
        result = locality.geocode.get('results')[0] # TODO handle multiple results
        location = result.get('geometry').get('location')
        point = Point(float(location.get('lat')), float(location.get('lng')))
        if result.get('geometry').get('location_type') is 'ROOFTOP':
            error = 100 # TODO
        else:
            error = 1000 # TODO
        return Georeference(point, error) # TODO 
        
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_point2wgs84()
    test_georef()
    
