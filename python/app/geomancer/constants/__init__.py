import collections
import copy
import csv
import logging
import os
import sys

def constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)

# ==============================================================================
# DistanceUnit

def _build_distanceunit_class():
    """Dynamically builds the DistanceUnit class from data in a CSV file."""
    props = {}
    data = {'FOOT': 'foot', 'KILOMETER': 'kilometer', 'METER': 'meter', 
             'MILE': 'mile', 'NAUTICAL_MILE': 'nautical mile', 'YARD': 'yard'}                        
    
    for unit in data.keys():
        props[unit] = data.get(unit)
    
    @classmethod
    def units(cls):
        return data.keys()
    props['units'] = units

    @classmethod
    def all(cls):
        return iter(data.values())
    props['all'] = all
    
    return type('DistanceUnit', (), props)

DistanceUnit = _build_distanceunit_class()


# ==============================================================================
# DistanceConversion

class _DistanceConversion(object):
    @constant
    def METER_PER_FEET():
        return 1.0 / 3.2808399
    @constant
    def METER_PER_KILOMETER():
        return 1000
    @constant
    def METER_PER_MILE():
        return 1609.344
    @constant
    def METER_PER_YARD():
        return 0.9144
    @constant
    def METER_PER_NAUTICAL_MILE():
        return 1851.989

DistanceConversion = _DistanceConversion()

# ==============================================================================
# Conversion calculator

class _Conversion(object):
    def __init__(self, du_from, du_to, factor):
        self.du_from = du_from
        self.du_to = du_to
        self.factor = factor

    def __str__(self):
        return str(self.__dict__)

_conversions = [
    _Conversion(DistanceUnit.METER, DistanceUnit.FOOT, DistanceConversion.METER_PER_FEET),
    _Conversion(DistanceUnit.METER, DistanceUnit.METER, 1),
    _Conversion(DistanceUnit.METER, DistanceUnit.KILOMETER, DistanceConversion.METER_PER_KILOMETER),
    _Conversion(DistanceUnit.METER, DistanceUnit.YARD, DistanceConversion.METER_PER_YARD),
    _Conversion(DistanceUnit.METER, DistanceUnit.MILE, DistanceConversion.METER_PER_MILE),
    _Conversion(DistanceUnit.METER, DistanceUnit.NAUTICAL_MILE, DistanceConversion.METER_PER_NAUTICAL_MILE)
]

_conversion_map = {DistanceUnit.METER: {}}

for c in _conversions:
    _conversion_map.get(DistanceUnit.METER)[c.du_to] = c

def convert_distance(value, dufrom, duto):
    if dufrom == duto:
        return value
    x = _conversion_map.get(DistanceUnit.METER).get(dufrom).factor
    y = _conversion_map.get(DistanceUnit.METER).get(duto).factor
    return float(value) * x/y

# ==============================================================================
# Direction

class _Direction(object):
    @constant
    def NORTH():
        return 'north'
    @constant
    def EAST():
        return 'east'
    @constant
    def WEST():
        return 'west'
    @constant
    def SOUTH():
        return 'south'

Direction = _Direction()

# ==============================================================================
# CoordiateSystem

class _CoordinateSystem(object):
    @constant
    def DD():
        return 'dd'
    @constant
    def DDM():
        return 'ddm'
    @constant
    def DMS():
        return 'dms'

CoordinateSystem = _CoordinateSystem()

# ==============================================================================
# CoordinateSource

class _CoordinateSource(object):
    @constant
    def GAZETTEER():
        return 0
    @constant
    def GPS():
        return 0
    @constant
    def LOCALITY_DESCRIPTION():
        return 0
    @constant
    def NTS_A_1_TO_250000():
        return 125 * DistanceConversion.FEET_PER_METER
    @constant
    def NTS_A_1_TO_50000():
        return 25 * DistanceConversion.FEET_PER_METER
    @constant
    def NTS_B_1_TO_250000():
        return 250 * DistanceConversion.FEET_PER_METER
    @constant
    def NTS_B_1_TO_50000():
        return 50 * DistanceConversion.FEET_PER_METER
    @constant
    def NTS_C_1_TO_250000():
        return 375 * DistanceConversion.FEET_PER_METER
    @constant
    def NTS_C_1_TO_50000():
        return 75 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_10000():
        return 10 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_100000():
        return 100 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_1000000():
        return 1000 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_150000():
        return 150 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_180000():
        return 180 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_20000():
        return 20 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_200000():
        return 200 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_2500():
        return 2.5 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_250000():
        return 250 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_2500000():
        return 2500 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_3000000():
        return 3000 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_32500():
        return 32.5 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_40000():
        return 40 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_50000():
        return 50 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_500000():
        return 500 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_60000():
        return 60 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_62500():
        return 62.5 * DistanceConversion.FEET_PER_METER
    @constant
    def OTHER_1_TO_80000():
        return 80 * DistanceConversion.FEET_PER_METER
    @constant
    def USGS_1_TO_100000():
        return 167
    @constant
    def USGS_1_TO_10000():
        return 27.8
    @constant
    def USGS_1_TO_1200():
        return 3.3
    @constant
    def USGS_1_TO_12000():
        return 33.3
    @constant
    def USGS_1_TO_2400():
        return 6.7
    @constant
    def USGS_1_TO_24000():
        return 40
    @constant
    def USGS_1_TO_25000():
        return 41.8
    @constant
    def USGS_1_TO_250000():
        return 417
    @constant
    def USGS_1_TO_4800():
        return 13.3
    @constant
    def USGS_1_TO_63360():
        return 106

CoordinateSource = _CoordinateSource()

# ==============================================================================
# Datum

class Datum(object):
    def __init__(self, name, code, ellipsoid_name, ellipsoid_code, flatting, axis, dx, dy, dz, epsgcode, rmserror):
        # TODO: This param list is out of control... maybe make it a dict instead.
        self._name = name
        self._code = code
        self._ellipsoid_name = ellipsoid_name
        self._ellipsoid_code = ellipsoid_code
        self._flattening = flatting
        self._axis = axis
        self._dx = dx
        self._dy = dy
        self._dz = dz
        self._epsgcode = epsgcode
        self._rmserror = rmserror

    def get_name(self):
        return self._name
    name = property(get_name)

    def getcode(self):
        return self._code
    code = property(getcode)

    def get_ellipsoid_name(self):
        return self._ellipsoid_name
    ellipsoid_name = property(get_ellipsoid_name)

    def get_ellipsoid_code(self):
        return self._ellipsoid_code
    ellipsoid_code = property(get_ellipsoid_code)
    
    def get_flattening(self):
        return self._flattening
    flattening = property(get_flattening)
    
    def get_axis(self):
        return self._axis
    axis = property(get_axis)

    def get_dx(self):
        return self._dx
    dx = property(get_dx)

    def get_dy(self):
        return self._dy
    dy = property(get_dy)

    def get_dz(self):
        return self._dz
    dz = property(get_dz)
    
    def get_epsgcode(self):
        return self._epsgcode
    epsgcode = property(get_epsgcode)

    def get_rmserror(self):
        return self._rmserror
    rmserror = property(get_rmserror)

    def __str__(self):
        return str(self.__dict__)

def _build_datums_class():
    """Dynamically builds the Datums class from data in a CSV file."""
    path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.join(path, 'DatumTransformationToWGS84Parameters.csv')
    dr = csv.DictReader(open(path, 'r'), skipinitialspace=True)
    props = {}
    datums = {}
    epsgmap = {}
    for row in dr:
        code = row['DatumCode']
        name = row['DatumName']
        ecode = row['EllipsoidCode']
        ename = row['EllipsoidName']
        dx = int(row['dX'])
        dy = int(row['dY'])
        dz = int(row['dZ'])
        f = float(row['Flattening'] or -1)
        a = float(row['SemiMajorAxis'] or -1)
        epsgcode = None
        try:
            # Some datums don't have an EPSG code:
            epsgcode = int(row['EPSGCode'])
        except:
            pass
        rmserror = float(row['RMSError'])
        d = Datum(name, code, ename, ecode, f, a, dx, dy, dz, epsgcode, rmserror)
        props[code] = d
        datums[code] = d
        epsgmap[epsgcode] = d
    
    @classmethod
    def fromepsgcode(cls, epsgcode):
        return epsgmap.get(epsgcode)
    props['fromepsgcode'] = fromepsgcode

    @classmethod
    def codes(cls):
        return datums.keys()
    props['codes'] = codes

    @classmethod
    def fromcode(cls, code):
        return datums.get(code)
    props['fromcode'] = fromcode

    @classmethod
    def all(cls):
        return iter(datums.values())
    props['all'] = all
    
    return type('Datums', (), props)

# The Datums class:
Datums = _build_datums_class()

class Heading(object):
    def __init__(self, code, bearing, error, name, forms):
        self.code = code
        self.bearing = bearing
        self.error = error
        self.name = name
        self.forms = forms

    def __str__(self):
        return str(self.__dict__)

def _build_headings_class():
    """Dynamically builds the Headings class from data in a CSV file."""
    path = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.join(path, 'HeadingsBearings.csv')
    dr = csv.DictReader(open(path, 'r'), skipinitialspace=True)
    props = {}
    headings = {}
    for row in dr:
        code = row['code']
        bearing = row['bearing']
        error = row['error']
        name = row['name']
        forms = [x.strip() for x in row['forms'].split(',')]
        d = Heading(code, bearing, error, name, forms)
        props[code] = d
        headings[code] = d
        
    @classmethod
    def codes(cls):
        return headings.keys()
    props['codes'] = codes

    @classmethod
    def fromcode(cls, code):
        return headings.get(code)
    props['fromcode'] = fromcode

    @classmethod
    def all(cls):
        return iter(headings.values())
    props['all'] = all
    
    return type('Headings', (), props)

# The Datums class:
Headings = _build_headings_class()

if __name__ == '__main__':
    pass
