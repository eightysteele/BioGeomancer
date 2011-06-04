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

#from constants import convert_distance
from constants import DistanceUnits
from constants import Datums
from constants import Headings
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
        if math.fabs(self.lat) <= 90:
            if math.fabs(self.lng) <=180:
                return True
        return False

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
    def get_status(cls, object):
        if not object.has_key('status'):
            return None
        return (object.get('status'))
        
    @classmethod
    def get_first_result(cls, object):
        if not object.has_key('results'):
            return None
        return (object.get('results')[0])
        
    @classmethod
    def get_point(cls, geometry):
        if geometry is None:
            return None
        if not geometry.has_key('location'):
            return None
        return (geometry.get('location').get('lng'), geometry.get('location').get('lat'))
    
    @classmethod
    def get_bounds(cls, geometry):
        if not geometry.has_key('bounds'):
            return None
        return geometry.get('bounds')
    
    @classmethod
    def calc_radius(cls, geometry):
        """Returns a radius in meters for the feature in the geometry. Assumes geometry exists."""
        bb = cls.get_bounds(geometry)
        if bb == None:
            if geometry.get('location_type') == 'ROOFTOP':
                return 100 # default radius ROOFTOP type
            else: # location_type other than ROOFTOP and no bounds
                return 1000
        center = cls.get_point(geometry)
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

def haversine_distance(start_lng_lat, end_lng_lat):
    """ Returns the distance along a great circle between two lng lats on the surface of a
    *sphere* of radius SEMI_MAJOR_AXIS using the Haversine formula.
        Arguments:
            start_lng_lat - 
            end_lng_lat -
    """
    dlng = math.radians(end_lng_lat[0] - start_lng_lat[0]) 
    dlat = math.radians(end_lng_lat[1] - start_lng_lat[1])
    '''a is the square of half the chord length between the points.'''
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos( math.radians(start_lng_lat[1]) ) * math.cos( math.radians(end_lng_lat[1]) ) * math.sin(dlng/2) * math.sin(dlng/2)
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

class Georeference(object):
    def __init__(self, point, error):
        self.point = point
        self.error = error
    
    def __str__(self):
        return str(self.__dict__)

def get_unit(unitstr):
    """Return a DistanceUnit instance from a string."""
    u = unitstr.replace('.', '').strip().lower()
    for unit in DistanceUnits.all():
        for form in unit.forms:
            if u == form:
                return unit
    return None

def get_heading(headingstr):
    """Return a Heading instance from a string."""
    h = headingstr.replace('-', '').replace(',', '').strip().lower()
    for heading in Headings.all():
        for form in heading.forms:
            if h == form:
                return heading
    return None

def georef_feature(geocode):
    """Returns a Georeference from the Geomancer API.
        Arguments:
            geocode - a Maps API JSON response for a feature
    """
    if not geocode:
        return None
    status = geocode.get('status')
    if status != 'OK':
        #Geocode failed, no results, no georeference possible.
        return None
    if geocode.get('results')[0].has_key('geometry') == False:
        #First result has no geometry, no georeference possible.
        return None
    g = geocode.get('results')[0].get('geometry')
    point = GeocodeResultParser.get_point(g)
    error = GeocodeResultParser.calc_radius(g)
    return Georeference(point, error)

def georeference(locality):
    """Returns a Georeference given a Locality object as input.
        Arguments:
            locality - an instance of a Locality object to georeference
    """
    if not locality:
        return None
    if not locality.loctype:
        # Georeference as feature-only using the geocode.
        return georef_feature(locality.geocode)
    if locality.loctype == 'foh':
        unitstr = locality.parts.get('offset_unit')
        headingstr = locality.parts.get('heading')
        offset = locality.parts.get('offset_value')
        featuregeocode = locality.parts.get('feature').get('geocode')
        # Get the feature, then do the georeference.
        feature = georef_feature(featuregeocode)
        error = foh_error(feature.point, feature.error, offset, unitstr, headingstr)
        # get a bearing from the heading
        bearing = get_heading(headingstr).bearing
        newpoint = foh_point(feature.point, offset, bearing)
        return Georeference(newpoint, error)

def foh_point(point, offset, bearing):
    """Returns the new point given by going the offset distance from the point at the bearing.
        Arguments:
            point - the center (lng, lat) of the feature staring point
            offset - the linear distance (float) from the starting coordinate
            bearing - the compass bearing (float) in degree from the starting coordinate
    """
    # TODO: Do the offset using great circle at bearing calculation
    return point 

def foh_error(point, extent, offset, offsetunits, headingstr):
    # No datum error - always WGS84
    # No source error from Maps API
    # Extent always in meters - comes from Maps API
    # No coordinate error from Maps API
    # error in meters
    error = 0
#      error += datumError(datum, point)
#      error += sourceError(source)
    error += extent
    # offset must be a string in this call
    distprecision = getDistancePrecision(offset)
    logging.info('foh_error: offset: %s type: %s offsetunits: %s'%(offset, type(offset), offsetunits))
    fromunit = get_unit(offsetunits)
    # distance precision in meters
    dpm = distprecision * float(fromunit.tometers)
    error += dpm
    # Convert offset to meters
    offsetinmeters = float(offset) * float(fromunit.tometers)
    # Get error angle from heading
    error = getDirectionError(error, offsetinmeters, headingstr)
#    error += coordinatesPrecisionError(coordinates)
    return error

def getDirectionError(starterror, offset, headingstr):
    """Returns a final error given a starting error, an offset, and a heading
        Arguments:
            starterror - accumulated error (float) from extent, etc.
            offset - the linear distance (float) from the starting coordinate
            heading - the compass direction (str) from the starting coordinate
    """ 
    headingerror = float(get_heading(headingstr).error)
    x = offset * math.cos(math.radians(headingerror))
    y = offset * math.sin(math.radians(headingerror))
    xp = offset + starterror
    neterror = math.sqrt(math.pow(xp - x, 2) + math.pow(y, 2))
    return neterror

def getDistancePrecision(distance):
    """Determine the uncertainty associated with the distance.
    Force distance to be a string on input.
    Methods taken from Wieczorek, et al. 2004, but modified for fractions to
    be one-half of that described in the paper, which we now believe to be unreasonably conservative."""
    logging.info('distance: %s type: %s'%(distance,type(distance)))
    if type(distance) != str and type(distance) != unicode:
        return None
    try:
        float(distance)
    except:
        return None
    if float(distance) < 0:
        return None
    if float(distance) < 0.001:
        return 0.0
    # distance is a non-negative number expressed as a string
    #Strip it of white space and make it into english decimal format
    d = distance.strip().replace(',','.')
    offsetuncertainty = 0.0
    offset = float(distance)
    sigdigits = 0 # significant digits to the right of the decimal
    offsetuncertainty = 1
    hasdecimal = len(distance.split('.')) - 1
    if hasdecimal > 0:    
        sigdigits = len(distance.split('.')[1])
    if sigdigits > 0:
        #If the last digit is a zero, the original was specified to that level of precision.
        if distance[len(distance)-1] == '0':
            offsetuncertainty = 1.0 * math.pow(10.0, -1.0 * sigdigits) 
            ''' Example: offsetstring = "10.0" offsetuncertainty = 0.1'''
        else:
            #Significant digits, but last one not '0'
            #Otherwise get the fractional part of the interpreted offset. We'll use this to determine uncertainty.
            fracpart, intpart = math.modf(float(offset))
            #Test to see if the fracpart can be turned in to any of the target fractions.
            #fracpart/testfraction = integer within a predefined level of tolerance.
            denominators = [2.0, 3.0, 4.0, 8.0, 10.0, 100.0, 1000.0]
            for d in denominators:
              numerator, extra = math.modf(fracpart * d)
#              nearestint = math.ceil(numerator)
              '''If the numerator is within tolerance of being an integer, then the
                denominator represents the distance precision in the original
                units.'''
              if numerator < 0.001 or math.fabs(numerator - 1) < 0.001:
                  #This denominator appears to represent a viable fraction.
                  offsetuncertainty = 1.0 / d
                  break
    else:
        powerfraction, powerint = math.modf(math.log10(offset))
        #If the offset is a positive integer power of ten.
        while offset % math.pow(10, powerint) > 0:
            powerint -= 1
        offsetuncertainty = math.pow(10.0, powerint)
    offsetuncertainty = offsetuncertainty * 0.5
    return offsetuncertainty
    
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
    logging.info(georeference(geocode))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_point2wgs84()
    test_georef()
#    test_distanceprecision()
#    test_heading()
    
