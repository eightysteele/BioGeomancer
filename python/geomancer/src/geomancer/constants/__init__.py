import copy

def constant(f):
    def fset(self, value):
        raise SyntaxError
    def fget(self):
        return f()
    return property(fget, fset)

# ==============================================================================
# DistanceUnit

class _DistanceUnit(object):
    @constant
    def FOOT():
        return 'foot'
    @constant
    def KILOMETER():
        return 'kilometer'
    @constant
    def METER():
        return 'meter'
    @constant
    def MILE():
        return 'mile'
    @constant
    def NAUTICAL_MILE():
        return 'nautical mile'
    @constant
    def YARD():
        return 'yard'


DistanceUnit = _DistanceUnit()

# ==============================================================================
# DistanceConversion

class _DistanceConversion(object):
    @constant
    def METER_PER_FEET():
        return 0.3048
    @constant
    def METER_PER_KILOMETER():
        return 1000.0
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

_conversions = [
    _Conversion(DistanceUnit.METER, DistanceUnit.FOOT, DistanceConversion.METER_PER_FEET),
    _Conversion(DistanceUnit.METER, DistanceUnit.KILOMETER, DistanceConversion.METER_PER_KILOMETER),
    _Conversion(DistanceUnit.METER, DistanceUnit.YARD, DistanceConversion.METER_PER_YARD),
    _Conversion(DistanceUnit.METER, DistanceUnit.MILE, DistanceConversion.METER_PER_MILE),
    _Conversion(DistanceUnit.METER, DistanceUnit.NAUTICAL_MILE, DistanceConversion.METER_PER_NAUTICAL_MILE),
]

_conversion_map = {}

for unit in [DistanceUnit.FOOT, DistanceUnit.KILOMETER, DistanceUnit.METER,
             DistanceUnit.MILE, DistanceUnit.YARD, DistanceUnit.NAUTICAL_MILE]:
    _conversion_map[unit] = {}

for c in _conversions:
    _conversion_map.get(c.du_from)[c.du_to] = c

def convert_distance(value, dufrom, duto):
    if dufrom == duto:
        return value
    return float(value) / _conversion_map.get(dufrom).get(duto).factor

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


class D(object):
    def __init__(self):
        dr = csv.DictReader(open('datums.csv', 'r'), skipinitialspace=True)
        er = csv.DictReader(open('ellipsoids.csv', 'r'), skipinitialspace=True)

class _Datum(object):    
    def __init__(self, name, ellipsoidName, flatting, axis):
        self._name = name
        self._ellipsoidName = ellipsoidName
        self._flattening = flatting
        self._axis = axis

    def get_name(self):
        return self._name
    name = property(get_name)

    def get_ellipsoidName(self):
        return self._ellipsoidName
    ellipsoidName = property(get_ellipsoidName)
    
    def get_flattening(self):
        return self._flattening
    flattening = property(get_flattening)
    
    def get_axis(self):
        return self._axis
    axis = property(get_axis)
    
    def __str__(self):
        return 'Name=%s, EllipsoidName=%s, Flattening=%s, Axis=%s' % (
            self.name, self.ellipsoidName, self.flattening, self.axis)

class Datum(object):
    _all = {}
    _all['NOT_RECORDED'] = _Datum("Not Recorded (forcing WGS84)", "WGS84", 298.257224, 6378137.000000)
    _all['WGS84_WORLD_GEODETIC_SYSTEM_1984'] = _Datum("(WGS84) World Geodetic System 1984", "WGS84", 298.257224, 6378137.000000)
    _all['NAD83_NORTH_AMERICAN_1983'] = _Datum("(NAD83) North American 1983", "GRS80", 298.257222, 6378137.000000)
    _all['NAD27_NORTH_AMERICAN_1927'] = _Datum("(NAD27) North American 1927", "Clarke 1866", 294.978698, 6378206.400000)
    _all['ADINDAN'] = _Datum("Adindan", "Clarke 1880", 293.465000, 6378249.145000)
    _all['AFGOOYE'] = _Datum("Afgooye", "Krassovsky 1940", 298.300000, 6378245.000000)
    _all['AIN_EL_ABD_1970'] = _Datum("Ain el Abd 1970", "International 1924", 297.000000, 6378388.000000)

    _all['AIRY_1830_ELLIPSOID'] = _Datum("Airy 1830 ellipsoid", "Airy 1830", 299.3249646, 6377563.396000)
    
    _all['AMERICAN_SAMOA_1962'] = _Datum("American Samoa 1962", "Clarke 1866", 294.978698, 6378206.400000)
    _all['ANNA_1_ASTRO_1965'] = _Datum("Anna 1 Astro 1965", "Australian National", 298.250000, 6378160.000000)
    _all['ANTIGUA_ISLAND_ASTRO_1943'] = _Datum("Antigua Island Astro 1943", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ARC_1950'] = _Datum("Arc 1950", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ARC_1960'] = _Datum("Arc 1960", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ASCENSION_ISLAND_1958'] = _Datum("Ascension Island 1958", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_BEACON_E_1945'] = _Datum("Astro Beacon E 1945", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_DOS_71_4'] = _Datum("Astro DOS 71/4", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_TERN_ISLAND_FRIG_1961'] = _Datum("Astro Tern Island (FRIG) 1961", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_NO_1_1951'] = _Datum("Astronomic Station No. 1 1951", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND'] = _Datum("Astronomic Station No. 2 1951 (Truk Island)", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_PONAPE_1951'] = _Datum("Astronomic Station Ponape 1951", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMICAL_STATION_1952'] = _Datum("Astronomical Station 1952", "International 1924", 297.000000, 6378388.000000)
    _all['AUSTRALIAN_GEODETIC_1966'] = _Datum("Australian Geodetic 1966", "Australian National", 298.250000, 6378160.000000)
    _all['AUSTRALIAN_GEODETIC_1984'] = _Datum("Australian Geodetic 1984", "Australian National", 298.250000, 6378160.000000)
    
    _all['AUSTRALIAN_NATIONAL_ELLIPSOID'] = _Datum("Australian National ellipsoid", "Australian National", 298.250000, 6378160.000000)
    
    _all['AYABELLE_LIGHTHOUSE'] = _Datum("Ayabelle Lighthouse", "Clarke 1880", 293.465000, 6378249.145000)
    _all['BEKAA_VALLEY_1920_IGN'] = _Datum("Bekaa Valley 1920 (IGN)", "Clarke 1880", 293.465000, 6378249.145000)
    _all['BELLEVUE_IGN'] = _Datum("Bellevue (IGN)", "International 1924", 297.000000, 6378388.000000)
    _all['BERMUDA_1957'] = _Datum("Bermuda 1957", "Clarke 1866", 294.978698, 6378206.400000)

    _all['BESSEL_1841_NAMIBIA_ELLIPSOID'] = _Datum("Bessel 1841 ellipsoid (Namibia)", "Bessel 1841 Namibia", 299.1528128, 6377483.865000)
    _all['BESSEL_1841_ELLIPSOID'] = _Datum("Bessel 1841 ellipsoid", "Bessel 1841", 299.1528128, 6377397.155000)

    _all['BISSAU'] = _Datum("Bissau", "International 1924", 297.000000, 6378388.000000)
    _all['BOGOTA_OBSERVATORY'] = _Datum("Bogota Observatory", "International 1924", 297.000000, 6378388.000000)
    _all['BUKIT_RIMPAH'] = _Datum("Bukit Rimpah", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['CAMP_AREA_ASTRO'] = _Datum("Camp Area Astro", "International 1924", 297.000000, 6378388.000000)
    _all['CAMPO_INCHAUSPE'] = _Datum("Campo Inchauspe", "International 1924", 297.000000, 6378388.000000)
    _all['CANTON_ASTRO_1966'] = _Datum("Canton Astro 1966", "International 1924", 297.000000, 6378388.000000)
    _all['CAPE'] = _Datum("Cape", "Clarke 1880", 293.465000, 6378249.145000)
    _all['CAPE_CANAVERAL'] = _Datum("Cape Canaveral", "Clarke 1866", 294.978698, 6378206.400000)
    _all['CARTHAGE'] = _Datum("Carthage", "Clarke 1880", 293.465000, 6378249.145000)
    _all['CHATHAM_ISLAND_ASTRO_1971'] = _Datum("Chatham Island Astro 1971", "International 1924", 297.000000, 6378388.000000)
    _all['CHUA_ASTRO'] = _Datum("Chua Astro", "International 1924", 297.000000, 6378388.000000)

    _all['CLARKE_1858_ELLIPSOID'] = _Datum("Clarke 1858 ellipsoid", "Clarke 1858", 294.260000, 6378293.600000)
    _all['CLARKE_1866_ELLIPSOID'] = _Datum("Clarke 1866 ellipsoid", "Clarke 1866", 294.9786982, 6378206.400000)
    _all['CLARKE_1880_ELLIPSOID'] = _Datum("Clarke 1880 ellipsoid", "Clarke 1880", 294.9786982, 6378249.145000)

    _all['COORDINATE_SYSTEM_1937_OF_ESTONIA'] = _Datum("Co-ordinate System 1937 of Estonia", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['CORREGO_ALEGRE'] = _Datum("Corrego Alegre", "International 1924", 297.000000, 6378388.000000)
    _all['DABOLA'] = _Datum("Dabola", "Clarke 1880", 293.465000, 6378249.145000)
    _all['DECEPTION_ISLAND'] = _Datum("Deception Island", "Clarke 1880", 293.465000, 6378249.145000)
    _all['DJAKARTA_BATAVIA'] = _Datum("Djakarta (Batavia)", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['DOS_1968'] = _Datum("DOS 1968", "International 1924", 297.000000, 6378388.000000)
    _all['EASTER_ISLAND_1967'] = _Datum("Easter Island 1967", "International 1924", 297.000000, 6378388.000000)
    _all['EUROPEAN_1950'] = _Datum("European 1950", "International 1924", 297.000000, 6378388.000000)
    _all['EUROPEAN_1979'] = _Datum("European 1979", "International 1924", 297.000000, 6378388.000000)

    _all['EVEREST_ELLIPSOID'] = _Datum("Everest ellipsoid (Brunei, Sabah, Sarawak)", "Everest Brunei and E. Malaysia (Sabah and Sarawak)", 300.801700, 6377298.556000)
    _all['EVEREST_INDIA_1830_ELLIPSOID'] = _Datum("Everest India 1830 ellipsoid", "Everest India 1830", 300.801700, 6377276.345000)
    _all['EVEREST_INDIA_1856_ELLIPSOID'] = _Datum("Everest India 1856 ellipsoid", "Everest India 1856", 300.801700, 6377301.243000)
    _all['EVEREST_PAKISTAN_ELLIPSOID'] = _Datum("Everest Pakistan ellipsoid", "Everest Pakistan", 300.801700, 6377309.613000)
    _all['EVEREST_WEST_MALAYSIA_1948_ELLIPSOID'] = _Datum("Everest W. Malaysia and Singapore 1948 ellipsoid", "Everest W. Malaysia and Singapore 1948", 300.801700, 6377304.063000)
    _all['EVEREST_WEST_MALAYSIA_1969_ELLIPSOID'] = _Datum("Everest W. Malaysia 1969 ellipsoid", "Everest W. Malaysia 1969", 300.801700, 6377295.664000)

    _all['FORT_THOMAS_1955'] = _Datum("Fort Thomas 1955", "Clarke 1880", 293.465000, 6378249.145000)
    _all['GAN_1970'] = _Datum("Gan 1970", "International 1924", 297.000000, 6378388.000000)
    _all['GEODETIC_DATUM_1949'] = _Datum("Geodetic Datum 1949", "International 1924", 297.000000, 6378388.000000)
    _all['GRACIOSA_BASE_SW_1948'] = _Datum("Graciosa Base SW 1948", "International 1924", 297.000000, 6378388.000000)

    _all['GRS80_ELLIPSOID'] = _Datum("GRS80 ellipsoid", "GRS80", 298.257222, 6378137.000000)

    _all['GUAM_1963'] = _Datum("Guam 1963", "Clarke 1866", 294.978698, 6378206.400000)
    _all['GUNUNG_SEGARA'] = _Datum("Gunung Segara", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['GUX_1_ASTRO'] = _Datum("GUX 1 Astro", "International 1924", 297.000000, 6378388.000000)

    _all['HELMERT_1906_ELLIPSOID'] = _Datum("Helmert 1906 ellipsoid", "Helmert 1906", 298.300000, 6378200.000000)

    _all['HERAT_NORTH'] = _Datum("Herat North", "International 1924", 297.000000, 6378388.000000)
    _all['HERMANNKOGEL'] = _Datum("Hermannkogel", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['HITO_XVIII_1963'] = _Datum("Hito XVIII 1963", "International 1924", 297.000000, 6378388.000000)
    _all['HJORSEY_1955'] = _Datum("Hjorsey 1955", "International 1924", 297.000000, 6378388.000000)
    _all['HONG_KONG_1963'] = _Datum("Hong Kong 1963", "International 1924", 297.000000, 6378388.000000)

    _all['HOUGH_1960_ELLIPSOID'] = _Datum("Hough 1960 ellipsoid", "Hough 1960", 297.000000, 6378270.000000)

    _all['HU_TZU_SHAN'] = _Datum("Hu-Tzu-Shan", "International 1924", 297.000000, 6378388.000000)
    _all['INDIAN'] = _Datum("Indian", "Everest India 1956", 300.801700, 6377301.243000)
    _all['INDIAN_1954'] = _Datum("Indian 1954", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDIAN_1960'] = _Datum("Indian 1960", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDIAN_1975'] = _Datum("Indian 1975", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDONESIAN_1974'] = _Datum("Indonesian 1974", "Indonesian 1974", 298.247000, 6378160.000000)

    _all['INTERNATIONAL_1924_ELLIPSOID'] = _Datum("International 1924 ellipsoid", "International 1924", 297.000000, 6378388.000000)

    _all['IRELAND_1965'] = _Datum("Ireland 1965", "Modified Airy", 299.324965, 6377340.189000)
    _all['ISTS_061_ASTRO_1968'] = _Datum("ISTS 061 Astro 1968", "International 1924", 297.000000, 6378388.000000)
    _all['ISTS_073_ASTRO_1969'] = _Datum("ISTS 073 Astro 1969", "International 1924", 297.000000, 6378388.000000)
    _all['JAPANESE_GEODETIC_DATUM_2000'] = _Datum("Japanese Geodetic Datum 2000", "GRS80 (NAD83)", 298.257222, 6378137.000000)
    _all['JOHNSTON_ISLAND_1961'] = _Datum("Johnston Island 1961", "International 1924", 297.000000, 6378388.000000)
    _all['KANDAWALA'] = _Datum("Kandawala", "Everest India 1830", 300.801700, 6377276.345000)
    _all['KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951'] = _Datum("Kapingamarangi Astronomic Station No. 3 1951", "International 1924", 297.000000, 6378388.000000)
    _all['KERGUELEN_ISLAND_1949'] = _Datum("Kerguelen Island 1949", "International 1924", 297.000000, 6378388.000000)
    _all['KERTAU_1948'] = _Datum("Kertau 1948", "Everest W. Malaysia and Singapore 1948", 300.801700, 6377304.063000)
    _all['KOREAN_GEODETIC_SYSTEM_1995'] = _Datum("Korean Geodetic System 1995", "WGS84", 298.257224, 6378137.000000)

    _all['KRASSOVSKY_1940_ELLIPSOID'] = _Datum("Krassovsky 1940 ellipsoid", "Krassovsky 1940", 298.300000, 6378245.000000)

    _all['KUSAIE_ASTRO_1951'] = _Datum("Kusaie Astro 1951", "International 1924", 297.000000, 6378388.000000)
    _all['L_C_5_ASTRO_1961'] = _Datum("L.C. 5 Astro 1961", "Clarke 1866", 294.978698, 6378206.400000)
    _all['LEIGON'] = _Datum("Leigon", "Clarke 1880", 293.465000, 6378249.145000)
    _all['LEMUTA'] = _Datum("Lemuta", "International 1924", 297.000000, 6378388.000000)
    _all['LIBERIA_1964'] = _Datum("Liberia 1964", "Clarke 1880", 293.465000, 6378249.145000)
    _all['LUZON'] = _Datum("Luzon", "Clarke 1866", 294.978698, 6378206.400000)
    _all['MAHE_1971'] = _Datum("Mahe 1971", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MASSAWA'] = _Datum("Massawa", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['MERCHICH'] = _Datum("Merchich", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MIDWAY_ASTRO_1961'] = _Datum("Midway Astro 1961", "International 1924", 297.000000, 6378388.000000)
    _all['MINNA'] = _Datum("Minna", "Clarke 1880", 293.465000, 6378249.145000)

    _all['MODIFIED_AIRY_ELLIPSOID'] = _Datum("Modified Airy ellipsoid", "Modified Airy", 299.324965, 6377340.189000)
    _all['MODIFIED_FISCHER_1960_ELLIPSOID'] = _Datum("Modified Fischer 1960 ellipsoid", "Modified Fischer 1960", 298.300000, 6378155.000000)

    _all['MONTSERRAT_ISLAND_ASTRO_1958'] = _Datum("Montserrat Island Astro 1958", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MPORALOKO'] = _Datum("M'Poraloko", "Clarke 1880", 293.465000, 6378249.145000)
    _all['NAHRWAN'] = _Datum("Nahrwan", "Clarke 1880", 293.465000, 6378249.145000)
    _all['NAPARIMA_BWI'] = _Datum("Naparima, BWI", "International 1924", 297.000000, 6378388.000000)
    _all['NAPARIMA_1972'] = _Datum("Naparima 1972", "International 1924", 297.000000, 6378388.000000)
    _all['NORTH_SAHARA_1959'] = _Datum("North Sahara 1959", "Clarke 1880", 293.465000, 6378249.145000)
    _all['OBSERVATORIO_METEOROLOGICO_1939'] = _Datum("Observatorio Meteorologico 1939", "International 1924", 297.000000, 6378388.000000)
    _all['OCOTEPEQUE_1935'] = _Datum("Ocotepeque 1935", "Clarke 1866", 294.978698, 6378206.400000)
    _all['OLD_EGYPTIAN_1907'] = _Datum("Old Egyptian 1907", "Helmert 1906", 298.300000, 6378200.000000)
    _all['OLD_HAWAIIAN_CLARKE_1866'] = _Datum("Old Hawaiian, Clarke 1866", "Clarke 1866", 294.978698, 6378206.400000)
    _all['OLD_HAWAIIAN_INTERNATIONAL_1924'] = _Datum("Old Hawaiian, International 1924", "International 1924", 297.000000, 6378388.000000)
    _all['OLD_TRINIDAD_1903'] = _Datum("Old Trinidad 1903, Clarke 1858", "Clarke 1858", 294.260000, 6378293.600000)
    _all['OMAN'] = _Datum("Oman", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ORDNANCE_SURVEY_OF_GREAT_BRITAIN_1936'] = _Datum("Ordnance Survey of Great Britain 1936", "Airy 1830", 299.3249646, 6377563.396000)
    _all['PICO_DE_LAS_NIEVES'] = _Datum("Pico de las Nieves", "International 1924", 297.000000, 6378388.000000)
    _all['PITCAIRN_ASTRO_1967'] = _Datum("Pitcairn Astro 1967", "International 1924", 297.000000, 6378388.000000)
    _all['POINT_58'] = _Datum("Point 58", "Clarke 1880", 293.465000, 6378249.145000)
    _all['POINT_NOIRE_1958'] = _Datum("Point Noire 1958", "Clarke 1880", 293.465000, 6378249.145000)
    _all['PORTO_SANTO_1936'] = _Datum("Porto Santo 1936", "International 1924", 297.000000, 6378388.000000)
    _all['PROVISIONAL_SOUTH_AMERICAN_1956'] = _Datum("Provisional South American 1956", "International 1924", 297.000000, 6378388.000000)
    _all['PROVISIONAL_SOUTH_CHILEAN_1963'] = _Datum("Provisional South Chilean 1963", "International 1924", 297.000000, 6378388.000000)
    _all['PUERTO_RICO'] = _Datum("Puerto Rico", "Clarke 1866", 294.978698, 6378206.400000)
    _all['QATAR_NATIONAL'] = _Datum("Qatar National", "International 1924", 297.000000, 6378388.000000)
    _all['QORNOQ'] = _Datum("Qornoq", "International 1924", 297.000000, 6378388.000000)
    _all['REUNION'] = _Datum("Reunion", "International 1924", 297.000000, 6378388.000000)
    _all['ROME_1940'] = _Datum("Rome 1940", "International 1924", 297.000000, 6378388.000000)
    _all['S_42_PULKOVO_1942'] = _Datum("S-42 (Pulkovo 1942)", "Krassovsky 1940", 298.300000, 6378245.000000)
    _all['SANTO_DOS_1965'] = _Datum("Santo (DOS) 1965", "International 1924", 297.000000, 6378388.000000)
    _all['SAO_BRAZ'] = _Datum("Sao Braz", "International 1924", 297.000000, 6378388.000000)
    _all['SAPPER_HILL_1943'] = _Datum("Sapper Hill 1943", "International 1924", 297.000000, 6378388.000000)
    _all['SCHWARZECK'] = _Datum("Schwarzeck", "Bessel 1841 Namibia", 299.1528128, 6377483.865000)
    _all['SELVAGEM_GRANDE_1938'] = _Datum("Selvagem Grande 1938", "International 1924", 297.000000, 6378388.000000)
    _all['SIERRA_LEONE_1960'] = _Datum("Sierra Leone 1960", "Clarke 1880", 293.465000, 6378249.145000)
    _all['S_JTSK'] = _Datum("S-JTSK", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['SOUTH_AMERICAN_1969'] = _Datum("South American 1969", "South American 1969", 298.2500000, 6378160.000000)
    _all['SIRGAS_SOUTH_AMERICAN_GEOCENTRIC_REFERENCE_SYSTEM'] = _Datum("SIRGAS - South American Geocentric Reference System", "GRS80", 298.257222, 6378137.000000)
    _all['SOUTH_ASIA'] = _Datum("South Asia", "Modified Fischer 1960", 298.300000, 6378155.000000)
    _all['TANANARIVE_OBSERVATORY_1925'] = _Datum("Tananarive Observatory 1925", "International 1924", 297.000000, 6378388.000000)
    _all['TIMBALAI_1948'] = _Datum("Timbalai 1948", "Everest Brunei and E. Malaysia (Sabah and Sarawak)", 300.801700, 6377298.556000)
    _all['TOKYO'] = _Datum("Tokyo", "Bessel 1841", 299.1528128, 6377397.155000)
    _all['TRISTAN_ASTRO_1968'] = _Datum("Tristan Astro 1968", "International 1924", 297.000000, 6378388.000000)
    _all['VITI_LEVU_1916'] = _Datum("Viti Levu 1916", "Clarke 1880", 293.465000, 6378249.145000)
    _all['VOIROL_1874'] = _Datum("Voirol 1874", "Clarke 1880", 293.465000, 6378249.145000)
    _all['VOIROL_1960'] = _Datum("Voirol 1960", "Clarke 1880", 293.465000, 6378249.145000)
    _all['WAKE_ENIWETOK_1960'] = _Datum("Wake-Eniwetok 1960", "Hough 1960", 297.000000, 6378270.000000)
    _all['WAKE_ISLAND_ASTRO_1952'] = _Datum("Wake Island Astro 1952", "International 1924", 297.000000, 6378388.000000)
    _all['WGS66'] = _Datum("(WGS66) World Geodetic System 1966", "WGS66", 298.250000, 6378145.000000)
    _all['WGS72'] = _Datum("(WGS72) World Geodetic System 1972", "WGS72", 298.260000, 6378135.000000)
    _all['YACARE'] = _Datum("Yacare", "International 1924", 297.000000, 6378388.000000)
    _all['ZANDERIJ'] = _Datum("Zanderij", "International 1924", 297.000000, 6378388.000000)
    _all['USER_DEFINED'] = _Datum("", "WGS84", 298.257224, 6378137.000000)

    NOT_RECORDED = _all.get('NOT_RECORDED')
    WGS84_WORLD_GEODETIC_SYSTEM_1984 = _all.get('WGS84_WORLD_GEODETIC_SYSTEM_1984')
    NAD83_NORTH_AMERICAN_1983 = _all.get('NAD83_NORTH_AMERICAN_1983')
    NAD27_NORTH_AMERICAN_1927 = _all.get('NAD27_NORTH_AMERICAN_1927')
    ADINDAN = _all.get('ADINDAN')
    AFGOOYE = _all.get('AFGOOYE')
    AIN_EL_ABD_1970 = _all.get('AIN_EL_ABD_1970')

    AIRY_1830_ELLIPSOID = _all.get('AIRY_1830_ELLIPSOID')


    AMERICAN_SAMOA_1962 = _all.get('AMERICAN_SAMOA_1962')
    ANNA_1_ASTRO_1965 = _all.get('ANNA_1_ASTRO_1965')
    ANTIGUA_ISLAND_ASTRO_1943 = _all.get('ANTIGUA_ISLAND_ASTRO_1943')
    ARC_1950 = _all.get('ARC_1950')
    ARC_1960 = _all.get('ARC_1960')
    ASCENSION_ISLAND_1958 = _all.get('ASCENSION_ISLAND_1958')
    ASTRO_BEACON_E_1945 = _all.get('ASTRO_BEACON_E_1945')
    ASTRO_DOS_71_4 = _all.get('ASTRO_DOS_71_4')
    ASTRO_TERN_ISLAND_FRIG_1961 = _all.get('ASTRO_TERN_ISLAND_FRIG_1961')
    ASTRONOMIC_STATION_NO_1_1951 = _all.get('ASTRONOMIC_STATION_NO_1_1951')
    ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND = _all.get('ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND')
    ASTRONOMIC_STATION_PONAPE_1951 = _all.get('ASTRONOMIC_STATION_PONAPE_1951')
    ASTRONOMICAL_STATION_1952 = _all.get('ASTRONOMICAL_STATION_1952')
    AUSTRALIAN_GEODETIC_1966 = _all.get('AUSTRALIAN_GEODETIC_1966')
    AUSTRALIAN_GEODETIC_1984 = _all.get('AUSTRALIAN_GEODETIC_1984')

    AUSTRALIAN_NATIONAL_ELLIPSOID = _all.get('AUSTRALIAN_NATIONAL_ELLIPSOID')

    AYABELLE_LIGHTHOUSE = _all.get('AYABELLE_LIGHTHOUSE')
    BEKAA_VALLEY_1920_IGN = _all.get('BEKAA_VALLEY_1920_IGN')
    BELLEVUE_IGN = _all.get('BELLEVUE_IGN')
    BERMUDA_1957 = _all.get('BERMUDA_1957')

    BESSEL_1841_NAMIBIA_ELLIPSOID = _all.get('BESSEL_1841_NAMIBIA_ELLIPSOID')
    BESSEL_1841_ELLIPSOID = _all.get('BESSEL_1841_ELLIPSOID')

    BISSAU = _all.get('BISSAU')
    BOGOTA_OBSERVATORY = _all.get('BOGOTA_OBSERVATORY')
    BUKIT_RIMPAH = _all.get('BUKIT_RIMPAH')
    CAMPO_INCHAUSPE = _all.get('CAMPO_INCHAUSPE')
    CANTON_ASTRO_1966 = _all.get('CANTON_ASTRO_1966')
    CAPE = _all.get('CAPE')
    CAPE_CANAVERAL = _all.get('CAPE_CANAVERAL')
    CARTHAGE = _all.get('CARTHAGE')
    CHATHAM_ISLAND_ASTRO_1971 = _all.get('CHATHAM_ISLAND_ASTRO_1971')
    CHUA_ASTRO = _all.get('CHUA_ASTRO')

    CLARKE_1858_ELLIPSOID = _all.get('CLARKE_1858_ELLIPSOID')
    CLARKE_1866_ELLIPSOID = _all.get('CLARKE_1866_ELLIPSOID')
    CLARKE_1880_ELLIPSOID = _all.get('CLARKE_1880_ELLIPSOID')

    COORDINATE_SYSTEM_1937_OF_ESTONIA = _all.get('COORDINATE_SYSTEM_1937_OF_ESTONIA')
    CORREGO_ALEGRE = _all.get('CORREGO_ALEGRE')
    DABOLA = _all.get('DABOLA')
    DECEPTION_ISLAND = _all.get('DECEPTION_ISLAND')
    DJAKARTA_BATAVIA = _all.get('DJAKARTA_BATAVIA')
    DOS_1968 = _all.get('DOS_1968')
    EASTER_ISLAND_1967 = _all.get('EASTER_ISLAND_1967')
    EUROPEAN_1950 = _all.get('EUROPEAN_1950')
    EUROPEAN_1979 = _all.get('EUROPEAN_1979')

    EVEREST_ELLIPSOID = _all.get('EVEREST_ELLIPSOID')
    EVEREST_INDIA_1830_ELLIPSOID = _all.get('EVEREST_INDIA_1830_ELLIPSOID')
    EVEREST_INDIA_1856_ELLIPSOID = _all.get('EVEREST_INDIA_1856_ELLIPSOID')
    EVEREST_PAKISTAN_ELLIPSOID = _all.get('EVEREST_PAKISTAN_ELLIPSOID')
    EVEREST_WEST_MALAYSIA_1948_ELLIPSOID = _all.get('EVEREST_WEST_MALAYSIA_1948_ELLIPSOID')
    EVEREST_WEST_MALAYSIA_1969_ELLIPSOID = _all.get('EVEREST_WEST_MALAYSIA_1969_ELLIPSOID')
    
    FORT_THOMAS_1955 = _all.get('FORT_THOMAS_1955')
    GAN_1970 = _all.get('GAN_1970')
    GEODETIC_DATUM_1949 = _all.get('GEODETIC_DATUM_1949')
    GRACIOSA_BASE_SW_1948 = _all.get('GRACIOSA_BASE_SW_1948')

    GRS80_ELLIPSOID = _all.get('GRS80_ELLIPSOID')
    
    GUAM_1963 = _all.get('GUAM_1963')
    GUNUNG_SEGARA = _all.get('GUNUNG_SEGARA')
    GUX_1_ASTRO = _all.get('GUX_1_ASTRO')

    HELMERT_1906_ELLIPSOID = _all.get('HELMERT_1906_ELLIPSOID')
    
    HITO_XVIII_1963 = _all.get('HITO_XVIII_1963')
    HJORSEY_1955 = _all.get('HJORSEY_1955')
    HONG_KONG_1963 = _all.get('HONG_KONG_1963')
    
    HOUGH_1960_ELLIPSOID = _all.get('HOUGH_1960_ELLIPSOID')
    
    HU_TZU_SHAN = _all.get('HU_TZU_SHAN')
    INDIAN = _all.get('INDIAN')
    INDIAN_1954 = _all.get('INDIAN_1954')
    INDIAN_1960 = _all.get('INDIAN_1960')
    INDIAN_1975 = _all.get('INDIAN_1975')
    INDONESIAN_1974 = _all.get('INDONESIAN_1974')

    INTERNATIONAL_1924_ELLIPSOID = _all.get('INTERNATIONAL_1924_ELLIPSOID')
    
    IRELAND_1965 = _all.get('IRELAND_1965')
    ISTS_061_ASTRO_1968 = _all.get('ISTS_061_ASTRO_1968')
    ISTS_073_ASTRO_1969 = _all.get('ISTS_073_ASTRO_1969')
    JAPANESE_GEODETIC_DATUM_2000 = _all.get('JAPANESE_GEODETIC_DATUM_2000')
    JOHNSTON_ISLAND_1961 = _all.get('JOHNSTON_ISLAND_1961')
    KANDAWALA = _all.get('KANDAWALA')
    KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951 = _all.get('KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951')
    KERGUELEN_ISLAND_1949 = _all.get('KERGUELEN_ISLAND_1949')
    KERTAU_1948 = _all.get('KERTAU_1948')
    KOREAN_GEODETIC_SYSTEM_1995 = _all.get('KOREAN_GEODETIC_SYSTEM_1995')

    KRASSOVSKY_1940_ELLIPSOID = _all.get('KRASSOVSKY_1940_ELLIPSOID')
    
    KUSAIE_ASTRO_1951 = _all.get('KUSAIE_ASTRO_1951')
    L_C_5_ASTRO_1961 = _all.get('L_C_5_ASTRO_1961')
    LEIGON = _all.get('LEIGON')
    LEMUTA = _all.get('LEMUTA')
    LIBERIA_1964 = _all.get('LIBERIA_1964')
    LUZON = _all.get('LUZON')
    MAHE_1971 = _all.get('MAHE_1971')
    MASSAWA = _all.get('MASSAWA')
    MERCHICH = _all.get('MERCHICH')
    MIDWAY_ASTRO_1961 = _all.get('MIDWAY_ASTRO_1961')
    MINNA = _all.get('MINNA')

    MODIFIED_AIRY_ELLIPSOID = _all.get('MODIFIED_AIRY_ELLIPSOID')
    MODIFIED_FISCHER_1960_ELLIPSOID = _all.get('MODIFIED_FISCHER_1960_ELLIPSOID')
    
    MONTSERRAT_ISLAND_ASTRO_1958 = _all.get('MONTSERRAT_ISLAND_ASTRO_1958')
    MPORALOKO = _all.get('MPORALOKO')
    NAHRWAN = _all.get('NAHRWAN')
    NAPARIMA_BWI = _all.get('NAPARIMA_BWI')
    NAPARIMA_1972 = _all.get('NAPARIMA_1972')
    NORTH_SAHARA_1959 = _all.get('NORTH_SAHARA_1959')
    OBSERVATORIO_METEOROLOGICO_1939 = _all.get('OBSERVATORIO_METEOROLOGICO_1939')
    OCOTEPEQUE_1935 = _all.get('OCOTEPEQUE_1935')
    OLD_EGYPTIAN_1907 = _all.get('OLD_EGYPTIAN_1907')
    OLD_HAWAIIAN_CLARKE_1866 = _all.get('OLD_HAWAIIAN_CLARKE_1866')
    OLD_HAWAIIAN_INTERNATIONAL_1924 = _all.get('OLD_HAWAIIAN_INTERNATIONAL_1924')
    OLD_TRINIDAD_1903 = _all.get('OLD_TRINIDAD_1903')
    OMAN = _all.get('OMAN')
    ORDNANCE_SURVEY_OF_GREAT_BRITAIN_1936 = _all.get('ORDNANCE_SURVEY_OF_GREAT_BRITAIN_1936')
    PICO_DE_LAS_NIEVES = _all.get('PICO_DE_LAS_NIEVES')
    PITCAIRN_ASTRO_1967 = _all.get('PITCAIRN_ASTRO_1967')
    POINT_58 = _all.get('POINT_58')
    POINT_NOIRE_1958 = _all.get('POINT_NOIRE_1958')
    PORTO_SANTO_1936 = _all.get('PORTO_SANTO_1936')
    PROVISIONAL_SOUTH_AMERICAN_1956 = _all.get('PROVISIONAL_SOUTH_AMERICAN_1956')
    PROVISIONAL_SOUTH_CHILEAN_1963 = _all.get('PROVISIONAL_SOUTH_CHILEAN_1963')
    PUERTO_RICO = _all.get('PUERTO_RICO')
    QATAR_NATIONAL = _all.get('QATAR_NATIONAL')
    QORNOQ = _all.get('QORNOQ')
    REUNION = _all.get('REUNION')
    ROME_1940 = _all.get('ROME_1940')
    S_42_PULKOVO_1942 = _all.get('S_42_PULKOVO_1942')
    SANTO_DOS_1965 = _all.get('SANTO_DOS_1965')
    SAO_BRAZ = _all.get('SAO_BRAZ')
    SAPPER_HILL_1943 = _all.get('SAPPER_HILL_1943')
    SCHWARZECK = _all.get('SCHWARZECK')
    SELVAGEM_GRANDE_1938 = _all.get('SELVAGEM_GRANDE_1938')
    SIERRA_LEONE_1960 = _all.get('SIERRA_LEONE_1960')
    S_JTSK = _all.get('S_JTSK')
    SOUTH_AMERICAN_1969 = _all.get('SOUTH_AMERICAN_1969')
    SIRGAS_SOUTH_AMERICAN_GEOCENTRIC_REFERENCE_SYSTEM = _all.get('SIRGAS_SOUTH_AMERICAN_GEOCENTRIC_REFERENCE_SYSTEM')
    SOUTH_ASIA = _all.get('SOUTH_ASIA')
    TANANARIVE_OBSERVATORY_1925 = _all.get('TANANARIVE_OBSERVATORY_1925')
    TIMBALAI_1948 = _all.get('TIMBALAI_1948')
    TOKYO = _all.get('TOKYO')
    TRISTAN_ASTRO_1968 = _all.get('TRISTAN_ASTRO_1968')
    VITI_LEVU_1916 = _all.get('VITI_LEVU_1916')
    VOIROL_1874 = _all.get('VOIROL_1874')
    VOIROL_1960 = _all.get('VOIROL_1960')
    WAKE_ENIWETOK_1960 = _all.get('WAKE_ENIWETOK_1960')
    WAKE_ISLAND_ASTRO_1952 = _all.get('WAKE_ISLAND_ASTRO_1952')
    WGS66 = _all.get('WGS66')
    WGS72 = _all.get('WGS72')
    YACARE = _all.get('YACARE')
    ZANDERIJ = _all.get('ZANDERIJ')
    USER_DEFINED = _all.get('USER_DEFINED')

    @staticmethod
    def has_id(id):
        return Datum._all.has_key(id)

    @staticmethod
    def ids():
        return Datum._all.keys()

    @staticmethod
    def all():
        return copy.copy(Datum._all)

    @staticmethod
    def get(id):
        return Datum._all.get(id)
    

if __name__ == '__main__':
    print Datum.ids()
    print Datum.has_id('Foo')
    print Datum.has_id('KOREAN_GEODETIC_SYSTEM_1995')
    print Datum.get('KOREAN_GEODETIC_SYSTEM_1995')
    print Datum.all().get('KOREAN_GEODETIC_SYSTEM_1995')
    print Datum.KOREAN_GEODETIC_SYSTEM_1995

    print CoordinateSource.NTS_C_1_TO_50000

    print convert_distance(1000, DistanceUnit.METER, DistanceUnit.KILOMETER)
