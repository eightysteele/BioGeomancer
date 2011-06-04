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

from constants import DistanceUnits
from constants import Datums
from constants import Headings
"""A_WGS84 is the radius of the sphere at the equator for the WGS84 datum."""
A_WGS84 = 6378137.0

"""DEGREE_DIGITS is the number of significant digits to the right of the decimal
to use in latitude and longitude equality determination and representation. This 
should be set to 7 to preserve reversible transformations between coordinate systems 
down to a resolution of roughly 1 m."""
DEGREE_DIGITS = 7

FORMAT = """.%sf"""

def truncate(x, digits):
    """Returns x including precision to the right of the decimal equal to digits."""
    format_x = FORMAT % digits
    return format(x,format_x)

def sqr(x):
    """Returns the square of x."""
    return x * x

def lng180(lng):
    """Returns a longitude in degrees between {-180, 180] given a longitude in degrees."""
    newlng = float(lng)
    if lng <= -180:
        return lng + 360
    if newlng > 180:
        return lng - 360
    return lng

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

    def __str__(self):
        return str(self.__dict__)

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
        """Returns a Point for the location element of a geometry."""
        if geometry is None:
            return None
        if not geometry.has_key('location'):
            return None
        return Point(geometry.get('location').get('lng'), geometry.get('location').get('lat'))
    
    @classmethod
    def get_bounds(cls, geometry):
        if not geometry.has_key('bounds'):
            return None
        return geometry.get('bounds')
    
    @classmethod
    def calc_radius(cls, geometry):
        """Returns a radius in meters from the center to the furthest corner of the bounds of the geometry."""
        if not geometry:
            return None
        bb = cls.get_bounds(geometry)
        if bb == None:
            if geometry.get('location_type') == 'ROOFTOP':
                return 100 # default radius ROOFTOP type
            else: # location_type other than ROOFTOP and no bounds
                return 1000
        center = cls.get_point(geometry)
        ne = Point( bb.get('northeast').get('lng'), bb.get('northeast').get('lat') )
        sw = Point( bb.get('southwest').get('lng'), bb.get('southwest').get('lat') )
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
        """Returns a lng, lat given a starting lng, lat and orthogonal offset distances.

        Arguments:
            corner - the lng, lat of the starting point.
            ndist - the distance north from corner along the same line of longitude to the 
                    latitude of the final point.
            sdist - the distance north from corner along the same line of longitude to the 
                    latitude of the final point.
            edist - the distance east from corner along the same line of latitude to the 
                    longitude of the final point.
            wdist - the distance west from corner along the same line of latitude to the 
                    longitude of the final point."""

        if (not ndist and not sdist) or (not edist and not wdist):
            return None
        if not self.unit:
            return None
        ns = 0.0
        ew = 0.0
        if ndist:
            ns = float(ndist)
            nsbearing = 0
        elif sdist:
            ns = float(sdist)
            nsbearing = 180
        if edist:
            ew = float(edist)
            ewbearing = 90
        elif wdist:
            ew = -float(wdist)
            ewbearing = 270
        # convert distances to meters
        ns = ns * get_unit(self.unit).tometers
        ew = ew * get_unit(self.unit).tometers
        # get coordinates of ns offset and ew offset
        nspoint = get_point_from_distance_at_bearing(corner, ns, nsbearing)
        ewpoint = get_point_from_distance_at_bearing(corner, ew, ewbearing)
        return Point(ewpoint.lng, nspoint.lat)

class Georeference(object):
    def __init__(self, point, error):
        self.point = point
        self.error = error
        
    def get_error(self):
        # error formatted to the nearest higher meter.
        ferror = int(math.ceil(self.error))
        return ferror
    
    def get_point(self):
        # latitude, longitude formatted to standardized precision
        flat = truncate(self.point.lat, DEGREE_DIGITS)
        flng = truncate(self.point.lng,DEGREE_DIGITS)
        return Point(flng, flat)
    
    def __str__(self):
        return str(self.__dict__)

def get_point_from_distance_at_bearing(point, distance, bearing):
    """Returns the destination point in degrees lng, lat truncated to the default number of
    digits of precision by going the given distance at the bearing from the start_lng_lat.
    
    Arguments:
        point - the starting Point
        distance - the distance from the starting Point, in meters
        bearing - the clockwise angle of the direction from the starting Point, in degrees from North
         
    Reference: http://www.movable-type.co.uk/scripts/latlong.html."""

    # ad is the angular distance (in radians) traveled.
    ad = distance/A_WGS84
    # lat1 is the latitude of the starting point in radians.
    lat1 = math.radians(point.lat)
    # lng1 is the longitude of the starting point in radians.
    lng1 = math.radians(point.lng)
    # b is the bearing direction in radians.
    b = math.radians(bearing)
    # lat2 is the latitude of the end point in radians.
    lat2 = math.asin( math.sin(lat1) * math.cos(ad) + math.cos(lat1) * math.sin(ad) * math.cos(b) )
    y = math.sin(b) * math.sin(ad) * math.cos(lat1)
    x = math.cos(ad) - math.sin(lat1) * math.sin(lat2)
    
    """Account for rounding errors. If x is very close to 0, set it to 0 to avoid 
    incorrect hemisphere determination.
    For example, if x = -1.1e-16, atan2(0,x) will be -math.pi when it should be 0."""
    if math.fabs(x) < 1e-10:
        x = 0
    # lng2 is the longitude of the end point in radians.
    lng2 = lng1 + math.atan2(y, x)
    lng2d = math.degrees(lng2)
    lat2d = math.degrees(lat2)
    return Point(float(truncate(lng2d,DEGREE_DIGITS)), float(truncate(lat2d,DEGREE_DIGITS)))

def haversine_distance(point, end_point):
    """Returns the distance in meters along a great circle between two Points on the surface of a
    *sphere* of radius A_WGS84 (WGS84 radius) using the Haversine formula. This is an 
    approximation of the distance on an ellipsoid.
    Arguments:
        point - the Point of the beginning of the arc  
        end_point - the Point of the end of the arc
    """

    dlng = math.radians(end_point.lng - point.lng) 
    dlat = math.radians(end_point.lat - point.lat)
    # a is the square of half the chord length between the points.'''
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos( math.radians(point.lat) ) * math.cos( math.radians(end_point.lat) ) * math.sin(dlng/2) * math.sin(dlng/2)
    # Account for rounding errors. If a is very close to 1 set it to one to avoid domain exception.'''
    if math.fabs(1-a) < 1e-10:
        a = 1
    # c is the angular distance in radians between the points.'''
    x = math.sqrt(1-a)
    y = math.sqrt(a)
    c = 2 * math.atan2(y, x)
    return A_WGS84 * c 

def point2wgs84(point, datum):
    """Returns a Point in WGS84 given a Point in any datum using the Abridged Molodensky Transformation.
    
    Arguments:
        point - the Point to transform
        datum - the Datum of the Point to transform
    
    Reference: Deakin, R.E. 2004. THE STANDARD AND ABRIDGED MOLDENSKY COORDINATE TRANSFORMATION FORMULAE. 
    Department of Mathematical and Geospatial Sciences, RMIT University.
    http://user.gs.rmit.edu.au/rod/files/publications/Molodensky%20V2.pdf
    """
    latr = math.radians(point.lat)
    lngr = math.radians(point.lng)
    
    # a is the semi-major axis of given datum.
    a = datum.axis
    
    # f is the flattening of given datum (get_flattening actually returns the inverse flattening).
    f = 1.0/datum.flattening
    dx = datum.dx
    dy = datum.dy
    dz = datum.dz
    
    # da is the difference between the semi-major axes.
    da = Datums.WGS84.axis - a
    
    # df is the difference between the flattenings.'''
    df = 1.0/Datums.WGS84.flattening - f
    
    e_squared = f*(2-f)
    rho = a*(1-e_squared)/math.pow((1-e_squared*sqr(math.sin(latr))),1.5)
    nu = a/math.pow((1-e_squared*sqr(math.sin(latr))),0.5)
    dlat = (1/rho)*(-dx*math.sin(latr)*math.cos(lngr) - dy*math.sin(latr)*math.sin(lngr) + dz*math.cos(latr) + (f*da + a*df)*math.sin(2*latr))
    dlng = (-dx*math.sin(lngr) + dy*math.cos(lngr))/(nu*math.cos(latr))
    newlng = lng180(math.degrees(lngr + dlng))
    newlat = math.degrees(latr + dlat)
    return Point(newlng, newlat)

def get_unit(unitstr):
    """Returns a DistanceUnit from a string."""
    u = unitstr.replace('.', '').strip().lower()
    for unit in DistanceUnits.all():
        for form in unit.forms:
            if u == form:
                return unit
    return None

def get_heading(headingstr):
    """Returns a Heading from a string."""
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
        # Geocode failed, no results, no georeference possible.
        return None
    if geocode.get('results')[0].has_key('geometry') == False:
        # First result has no geometry, no georeference possible.
        return None
    g = geocode.get('results')[0].get('geometry')
    point = GeocodeResultParser.get_point(g)
    error = GeocodeResultParser.calc_radius(g)
    return Georeference(point, error)

def georeference(locality):
    """Returns a Georeference given a Locality.
        Arguments:
            locality - the Locality to georeference
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
        bearing = float(get_heading(headingstr).bearing)
        fromunit = get_unit(unitstr)
        offsetinmeters = float(offset) * float(fromunit.tometers)        
        newpoint = get_point_from_distance_at_bearing(feature.point, offsetinmeters, bearing)
        return Georeference(newpoint, error)

def foh_error(point, extent, offsetstr, offsetunits, headingstr):
    """Returns the radius in meters from a Point containing all of the uncertainties
    for a Locality of type Feature Offset Heading.
    
    Arguments:
        point - the center of the feature in the Locality
        extent - the radius from the center of the Feature to the furthest corner of the bounding
                 box containing the feature, in meters
        offset - the distance from the center of the feature, as a string
        offsetunits - the units of the offset
        headingstr - the direction from the feature to the location
        
    Note: all sources for error are shown, though some do not apply under the assumption of using the 
    Google Geocoding API for get the feature information."""
    # error in meters
    error = 0
    # No datum error - always WGS84
#      error += datumError(datum, point)
    # No source error from Maps Geocoding API
#      error += sourceError(source)
    error += extent
    # offset must be a string in this call
    distprecision = getDistancePrecision(offsetstr)
    fromunit = get_unit(offsetunits)
    # distance precision in meters
    dpm = distprecision * float(fromunit.tometers)
    error += dpm
    # Convert offset to meters
    offsetinmeters = float(offsetstr) * float(fromunit.tometers)
    # Get error angle from heading
    error = getDirectionError(error, offsetinmeters, headingstr)
    # No coordinate error from Maps Geocoding API - more than six digits retained
#    error += coordinatesPrecisionError(coordinates)
    return error

def getDirectionError(starterror, offset, headingstr):
    """Returns the error due to direction given a starting error, an offset, and a heading from a Point.

    Arguments:
        starterror - accumulated initial error from extent, etc., in meters
        offset - the linear distance from the starting coordinate, in meters
        headingstr - the direction from the feature to the location""" 
    
    headingerror = float(get_heading(headingstr).error)
    x = offset * math.cos(math.radians(headingerror))
    y = offset * math.sin(math.radians(headingerror))
    xp = offset + starterror
    neterror = math.sqrt(math.pow(xp - x, 2) + math.pow(y, 2))
    return neterror

def getDistancePrecision(distance):
    """Returns the precision of the string representation of the distance as a value in the same units.
    
    Arguments:
        distance - the distance for which the precision is to be determined, as a string

    Reference: Wieczorek, et al. 2004, MaNIS/HerpNet/ORNIS Georeferencing Guidelines, 
    http://manisnet.org/GeorefGuide.html
    
    Note: Calculations modified for fractions to be one-half of that described in the paper, 
    which we now believe to be unreasonably conservative."""
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
    # Strip it of white space and put it in English decimal format
    d = distance.strip().replace(',','.')
    offsetuncertainty = 0.0
    offset = float(distance)
    # significant digits to the right of the decimal
    sigdigits = 0 
    offsetuncertainty = 1
    hasdecimal = len(distance.split('.')) - 1
    if hasdecimal > 0:    
        sigdigits = len(distance.split('.')[1])
    if sigdigits > 0:
        #If the last digit is a zero, the original was specified to that level of precision.
        if distance[len(distance)-1] == '0':
            offsetuncertainty = 1.0 * math.pow(10.0, -1.0 * sigdigits) 
            # Example: offsetstring = "10.0" offsetuncertainty = 0.1
        else:
            # Significant digits, but last one not '0'
            # Otherwise get the fractional part of the interpreted offset. 
            # We'll use this to determine uncertainty.
            fracpart, intpart = math.modf(float(offset))
            # Test to see if the fracpart can be turned in to any of the target fractions.
            # fracpart/testfraction = integer within a predefined level of tolerance.
            denominators = [2.0, 3.0, 4.0, 8.0, 10.0, 100.0, 1000.0]
            for d in denominators:
              numerator, extra = math.modf(fracpart * d)
              '''If the numerator is within tolerance of being an integer, then the
                denominator represents the distance precision in the original
                units.'''
              if numerator < 0.001 or math.fabs(numerator - 1) < 0.001:
                  # This denominator appears to represent a viable fraction.
                  offsetuncertainty = 1.0 / d
                  break
    else:
        powerfraction, powerint = math.modf(math.log10(offset))
        # If the offset is a positive integer power of ten.
        while offset % math.pow(10, powerint) > 0:
            powerint -= 1
        offsetuncertainty = math.pow(10.0, powerint)
    offsetuncertainty = offsetuncertainty * 0.5
    return offsetuncertainty
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
#    test_georeference_feature()
#    test_point_from_dist_at_bearing()
#    test_haversine_distance()
    
