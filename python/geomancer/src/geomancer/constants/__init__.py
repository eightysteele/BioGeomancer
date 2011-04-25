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
      def FOOT():
          return 'foot'
      def KILOMETER():
          return 'kilometer'
      def METER():
          return 'meter'
      def MILE():
          return 'mile'
      def YARD():
          return 'yard'

DistanceUnit = _DistanceUnit()

# ==============================================================================
# DistanceConversion

class _DistanceConversion(object):
    @constant
    def FEET_PER_KILOMETER():
        return 3280.8399
    @constant
    def KILOMETER_PER_FEET():
        return 1 / 3280.8399
    @constant
    def FEET_PER_METER():
        return 3.2808399
    @constant
    def METER_PER_FEET():
        return 1 / 3.2808399
    @constant
    def FEET_PER_MILE():
        return 5280
    @constant
    def MILE_PER_FEET():
        return 1 / 5280
    @constant
    def FEET_PER_YARD():
        return 3
    @constant
    def YARD_PER_FEET():
        return 1 / 3
    @constant
    def METER_PER_KILOMETER():
        return 1000
    @constant
    def KILOMETER_PER_METER():
        return 1 / 1000
    @constant
    def METER_PER_MILE():
        return 1609.344
    @constant
    def MILE_PER_METER():
        return 1 / 1609.344
    @constant
    def METER_PER_YARD():
        return 0.9144
    @constant
    def YARD_PER_METER():
        return 1 / 0.9144
    @constant
    def YARD_PER_KILOMETER():
        return 1093.6133
    @constant
    def KILOMETER_PER_YARD():
        return 1 / 1093.6133
    @constant
    def YARD_PER_MILE():
        return 1760
    @constant
    def MILE_PER_YARD():
        return 1 / 1760
    @constant
    def MILE_PER_KILOMETER():
        return 0.621371192
    @constant
    def KILOMETER_PER_MILE():
        return 1 / 0.621371192

DistanceConversion = _DistanceConversion()

# ==============================================================================
# Conversion calculator

class _Conversion(object):
    def __init__(self, du_from, du_to, factor):
        self.du_from = du_from
        self.du_to = du_to
        self.factor = factor

_conversions = [
    _Conversion(DistanceUnit.FOOT, DistanceUnit.KILOMETER, DistanceConversion.FEET_PER_KILOMETER),
    _Conversion(DistanceUnit.FOOT, DistanceUnit.METER, DistanceConversion.FEET_PER_METER),
    _Conversion(DistanceUnit.FOOT, DistanceUnit.MILE, DistanceConversion.FEET_PER_MILE),
    _Conversion(DistanceUnit.FOOT, DistanceUnit.YARD, DistanceConversion.FEET_PER_YARD),
    _Conversion(DistanceUnit.KILOMETER, DistanceUnit.FOOT, DistanceConversion.KILOMETER_PER_FEET),
    _Conversion(DistanceUnit.KILOMETER, DistanceUnit.MILE, DistanceConversion.KILOMETER_PER_MILE),
    _Conversion(DistanceUnit.KILOMETER, DistanceUnit.YARD, DistanceConversion.KILOMETER_PER_YARD),
    _Conversion(DistanceUnit.KILOMETER, DistanceUnit.METER, DistanceConversion.KILOMETER_PER_METER),
    _Conversion(DistanceUnit.METER, DistanceUnit.FOOT, DistanceConversion.METER_PER_FEET),
    _Conversion(DistanceUnit.METER, DistanceUnit.KILOMETER, DistanceConversion.METER_PER_KILOMETER),
    _Conversion(DistanceUnit.METER, DistanceUnit.YARD, DistanceConversion.METER_PER_YARD),
    _Conversion(DistanceUnit.METER, DistanceUnit.MILE, DistanceConversion.METER_PER_MILE),
    _Conversion(DistanceUnit.MILE, DistanceUnit.FOOT, DistanceConversion.MILE_PER_FEET),
    _Conversion(DistanceUnit.MILE, DistanceUnit.KILOMETER, DistanceConversion.MILE_PER_KILOMETER),
    _Conversion(DistanceUnit.MILE, DistanceUnit.METER, DistanceConversion.MILE_PER_METER),
    _Conversion(DistanceUnit.MILE, DistanceUnit.YARD, DistanceConversion.MILE_PER_YARD),
    _Conversion(DistanceUnit.YARD, DistanceUnit.FOOT, DistanceConversion.YARD_PER_FEET),
    _Conversion(DistanceUnit.YARD, DistanceUnit.MILE, DistanceConversion.YARD_PER_MILE),
    _Conversion(DistanceUnit.YARD, DistanceUnit.KILOMETER, DistanceConversion.YARD_PER_KILOMETER),
    _Conversion(DistanceUnit.YARD, DistanceUnit.METER, DistanceConversion.YARD_PER_METER)
]

_conversion_map = {}
for unit in [DistanceUnit.FOOT, DistanceUnit.KILOMETER, DistanceUnit.METER,
             DistanceUnit.MILE, DistanceUnit.YARD]:
    _conversion_map[unit] = {}
for c in _conversions:
    _conversion_map.get(c.du_from)[c.du_to] = c

def convert_distance(value, dufrom, duto):
    if dufrom == duto:
        return value
    return value / _conversion_map.get(dufrom).get(duto).factor

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
# CoordiateSource

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
    _all['ANNA_1_ASTRO_1965'] = _Datum("Anna 1 Astro 1965", "Australian National", 298.250000, 6378160.000000)
    _all['AUSTRALIAN_GEODETIC_1966'] = _Datum("Australian Geodetic 1966", "Australian National", 298.250000, 6378160.000000)
    _all['AUSTRALIAN_GEODETIC_1984'] = _Datum("Australian Geodetic 1984", "Australian National", 298.250000, 6378160.000000)
    _all['NAD27_NORTH_AMERICAN_1927'] = _Datum("(NAD27) North American 1927", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['AMERICAN_SAMOA_1962'] = _Datum("American Samoa 1962", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['BERMUDA_1957'] = _Datum("Bermuda 1957", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['CAPE_CANAVERAL'] = _Datum("Cape Canaveral", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['GUAM_1963'] = _Datum("Guam 1963", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['L_C_5_ASTRO_1961'] = _Datum("L. C. 5 Astro 1961", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['LUZON'] = _Datum("Luzon", "Clarke 1866 (NAD27)", 294.978698, 6378206.400000)
    _all['ADINDAN'] = _Datum("Adindan", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ANTIGUA_ISLAND_ASTRO_1943'] = _Datum("Antigua Island Astro 1943", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ARC_1950'] = _Datum("Arc 1950", "Clarke 1880", 293.465000, 6378249.145000)
    _all['ARC_1960'] = _Datum("Arc 1960", "Clarke 1880", 293.465000, 6378249.145000)
    _all['AYABELLE_LIGHTHOUSE'] = _Datum("Ayabelle Lighthouse", "Clarke 1880", 293.465000, 6378249.145000)
    _all['BEKAA_VALLEY_1920_IGN'] = _Datum("Bekaa Valley 1920 (IGN)", "Clarke 1880", 293.465000, 6378249.145000)
    _all['CAPE'] = _Datum("Cape", "Clarke 1880", 293.465000, 6378249.145000)
    _all['CARTHAGE'] = _Datum("Carthage", "Clarke 1880", 293.465000, 6378249.145000)
    _all['DABOLA'] = _Datum("Dabola", "Clarke 1880", 293.465000, 6378249.145000)
    _all['DECEPTION_ISLAND'] = _Datum("Deception Island", "Clarke 1880", 293.465000, 6378249.145000)
    _all['FORT_THOMAS_1955'] = _Datum("Fort Thomas 1955", "Clarke 1880", 293.465000, 6378249.145000)
    _all['LEIGON'] = _Datum("Leigon", "Clarke 1880", 293.465000, 6378249.145000)
    _all['LIBERIA_1964'] = _Datum("Liberia 1964", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MPORKALOKO'] = _Datum("M'Porkaloko", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MAHE_1971'] = _Datum("Mahe 1971", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MERCHICH'] = _Datum("Merchich", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MINNA'] = _Datum("Minna", "Clarke 1880", 293.465000, 6378249.145000)
    _all['MONTSERRAT_ISLAND_ASTRO_1958'] = _Datum("Montserrat Island Astro 1958", "Clarke 1880", 293.465000, 6378249.145000)
    _all['NAHRWAN'] = _Datum("Nahrwan", "Clarke 1880", 293.465000, 6378249.145000)
    _all['INDIAN_1954'] = _Datum("Indian 1954", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDIAN_1960'] = _Datum("Indian 1960", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDIAN_1975'] = _Datum("Indian 1975", "Everest India 1830", 300.801700, 6377276.345000)
    _all['KANDAWALA'] = _Datum("Kandawala", "Everest India 1830", 300.801700, 6377276.345000)
    _all['INDIAN'] = _Datum("Indian", "Everest India 1956", 300.801700, 6377301.243000)
    _all['KERTAU_1948'] = _Datum("Kertau 1948", "Everest W. Malaysia and Singapore 1948", 300.801700, 6377304.063000)
    _all['NAD83_NORTH_AMERICAN_1983'] = _Datum("(NAD83) North American 1983", "GRS80 (NAD83)", 298.257222, 6378137.000000)
    _all['JAPANESE_GEODETIC_DATUM_2000'] = _Datum("Japanese Geodetic Datum 2000", "GRS80 (NAD83)", 298.257222, 6378137.000000)
    _all['INDONESIAN_1974'] = _Datum("Indonesian 1974", "Indonesian 1974", 298.247000, 6378160.000000)
    _all['AIN_EL_ABD_1970'] = _Datum("Ain el Abd 1970", "International 1924", 297.000000, 6378388.000000)
    _all['ASCENSION_ISLAND_1958'] = _Datum("Ascension Island 1958", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_BEACON'] = _Datum("Astro Beacon", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_DOS_71_4'] = _Datum("Astro DOS 71/4", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRO_TERN_ISLAND_FRIG_1961'] = _Datum("Astro Tern Island (FRIG) 1961", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_NO_1_1951'] = _Datum("Astronomic Station No. 1 1951", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND'] = _Datum("Astronomic Station No. 2 1951 (Truk Island)", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMIC_STATION_PONAPE_1951'] = _Datum("Astronomic Station Ponape 1951", "International 1924", 297.000000, 6378388.000000)
    _all['ASTRONOMICAL_STATION_1952'] = _Datum("Astronomical Station 1952", "International 1924", 297.000000, 6378388.000000)
    _all['BELLEVUE_IGN'] = _Datum("Bellevue (IGN)", "International 1924", 297.000000, 6378388.000000)
    _all['BISSAU'] = _Datum("Bissau", "International 1924", 297.000000, 6378388.000000)
    _all['BOGOTA_OBSERVATORY'] = _Datum("Bogota Observatory", "International 1924", 297.000000, 6378388.000000)
    _all['CAMPO_INCHAUSPE'] = _Datum("Campo Inchauspe", "International 1924", 297.000000, 6378388.000000)
    _all['CANTON_ASTRO_1966'] = _Datum("Canton Astro 1966", "International 1924", 297.000000, 6378388.000000)
    _all['CHATHAM_ISLAND_ASTRO_1971'] = _Datum("Chatham Island Astro 1971", "International 1924", 297.000000, 6378388.000000)
    _all['CHUA_ASTRO'] = _Datum("Chua Astro", "International 1924", 297.000000, 6378388.000000)
    _all['CORREGO_ALEGRE'] = _Datum("Corrego Alegre", "International 1924", 297.000000, 6378388.000000)
    _all['DOS_1968'] = _Datum("DOS 1968", "International 1924", 297.000000, 6378388.000000)
    _all['EASTER_ISLAND_1967'] = _Datum("Easter Island 1967", "International 1924", 297.000000, 6378388.000000)
    _all['EUROPEAN_1950'] = _Datum("European 1950", "International 1924", 297.000000, 6378388.000000)
    _all['EUROPEAN_1979'] = _Datum("European 1979", "International 1924", 297.000000, 6378388.000000)
    _all['GUX_1_ASTRO'] = _Datum("GUX 1 Astro", "International 1924", 297.000000, 6378388.000000)
    _all['GAN_1970'] = _Datum("Gan 1970", "International 1924", 297.000000, 6378388.000000)
    _all['GEODETIC_DATUM_1949'] = _Datum("Geodetic Datum 1949", "International 1924", 297.000000, 6378388.000000)
    _all['GRACIOSA_BASE_SW_1948'] = _Datum("Graciosa Base SW 1948", "International 1924", 297.000000, 6378388.000000)
    _all['HJORSEY_1955'] = _Datum("Hjorsey 1955", "International 1924", 297.000000, 6378388.000000)
    _all['HONG_KONG_1963'] = _Datum("Hong Kong 1963", "International 1924", 297.000000, 6378388.000000)
    _all['HU_TZU_SHAN'] = _Datum("Hu-Tzu-Shan", "International 1924", 297.000000, 6378388.000000)
    _all['ISTS_061_ASTRO_1968'] = _Datum("ISTS 061 Astro 1968", "International 1924", 297.000000, 6378388.000000)
    _all['ISTS_073_ASTRO_1969'] = _Datum("ISTS 073 Astro 1969", "International 1924", 297.000000, 6378388.000000)
    _all['JOHNSTON_ISLAND_1961'] = _Datum("Johnston Island 1961", "International 1924", 297.000000, 6378388.000000)
    _all['KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951'] = _Datum("Kapingamarangi Astronomic Station No. 3 1951", "International 1924", 297.000000, 6378388.000000)
    _all['KERGUELEN_ISLAND_1949'] = _Datum("Kerguelen Island 1949", "International 1924", 297.000000, 6378388.000000)
    _all['KUSAIE_ASTRO_1951'] = _Datum("Kusaie Astro 1951", "International 1924", 297.000000, 6378388.000000)
    _all['LEMUTA'] = _Datum("Lemuta", "International 1924", 297.000000, 6378388.000000)
    _all['MIDWAY_ASTRO_1961'] = _Datum("Midway Astro 1961", "International 1924", 297.000000, 6378388.000000)
    _all['NOT_RECORDED'] = _Datum("Not Recorded (Will assume WGS84)", "WGS84", 298.257224, 6378137.000000)
    _all['AFGOOYE'] = _Datum("Afgooye", "Krassovsky 1940", 298.300000, 6378245.000000)
    _all['IRELAND_1965'] = _Datum("Ireland 1965", "Modified Airy", 299.324965, 6377340.189000)
    _all['WGS84_WORLD_GEODETIC_SYSTEM_1984'] = _Datum("(WGS84) World Geodetic System 1984", "WGS84", 298.257224, 6378137.000000)
    _all['KOREAN_GEODETIC_SYSTEM_1995'] = _Datum("Korean Geodetic System 1995", "WGS84", 298.257224, 6378137.000000)
    _all['USER_DEFINED'] = _Datum("", "WGS84", 298.257224, 6378137.000000)

    ANNA_1_ASTRO_1965 = _all.get('ANNA_1_ASTRO_1965')
    AUSTRALIAN_GEODETIC_1966 = _all.get('AUSTRALIAN_GEODETIC_1966')
    AUSTRALIAN_GEODETIC_1984 = _all.get('AUSTRALIAN_GEODETIC_1984')
    NAD27_NORTH_AMERICAN_1927 = _all.get('NAD27_NORTH_AMERICAN_1927')
    AMERICAN_SAMOA_1962 = _all.get('AMERICAN_SAMOA_1962')
    BERMUDA_1957 = _all.get('BERMUDA_1957')
    CAPE_CANAVERAL = _all.get('CAPE_CANAVERAL')
    GUAM_1963 = _all.get('GUAM_1963')
    L_C_5_ASTRO_1961 = _all.get('L_C_5_ASTRO_1961')
    LUZON = _all.get('LUZON')
    ADINDAN = _all.get('ADINDAN')
    ANTIGUA_ISLAND_ASTRO_1943 = _all.get('ANTIGUA_ISLAND_ASTRO_1943')
    ARC_1950 = _all.get('ARC_1950')
    ARC_1960 = _all.get('ARC_1960')
    AYABELLE_LIGHTHOUSE = _all.get('AYABELLE_LIGHTHOUSE')
    BEKAA_VALLEY_1920_IGN = _all.get('BEKAA_VALLEY_1920_IGN')
    CAPE = _all.get('CAPE')
    CARTHAGE = _all.get('CARTHAGE')
    DABOLA = _all.get('DABOLA')
    DECEPTION_ISLAND = _all.get('DECEPTION_ISLAND')
    FORT_THOMAS_1955 = _all.get('FORT_THOMAS_1955')
    LEIGON = _all.get('LEIGON')
    LIBERIA_1964 = _all.get('LIBERIA_1964')
    MPORKALOKO = _all.get('MPORKALOKO')
    MAHE_1971 = _all.get('MAHE_1971')
    MERCHICH = _all.get('MERCHICH')
    MINNA = _all.get('MINNA')
    MONTSERRAT_ISLAND_ASTRO_1958 = _all.get('MONTSERRAT_ISLAND_ASTRO_1958')
    NAHRWAN = _all.get('NAHRWAN')
    INDIAN_1954 = _all.get('INDIAN_1954')
    INDIAN_1960 = _all.get('INDIAN_1960')
    INDIAN_1975 = _all.get('INDIAN_1975')
    KANDAWALA = _all.get('KANDAWALA')
    INDIAN = _all.get('INDIAN')
    KERTAU_1948 = _all.get('KERTAU_1948')
    NAD83_NORTH_AMERICAN_1983 = _all.get('NAD83_NORTH_AMERICAN_1983')
    JAPANESE_GEODETIC_DATUM_2000 = _all.get('JAPANESE_GEODETIC_DATUM_2000')
    INDONESIAN_1974 = _all.get('INDONESIAN_1974')
    AIN_EL_ABD_1970 = _all.get('AIN_EL_ABD_1970')
    ASCENSION_ISLAND_1958 = _all.get('ASCENSION_ISLAND_1958')
    ASTRO_BEACON = _all.get('ASTRO_BEACON')
    ASTRO_DOS_71_4 = _all.get('ASTRO_DOS_71_4')
    ASTRO_TERN_ISLAND_FRIG_1961 = _all.get('ASTRO_TERN_ISLAND_FRIG_1961')
    ASTRONOMIC_STATION_NO_1_1951 = _all.get('ASTRONOMIC_STATION_NO_1_1951')
    ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND = _all.get('ASTRONOMIC_STATION_NO_2_1951_TRUK_ISLAND')
    ASTRONOMIC_STATION_PONAPE_1951 = _all.get('ASTRONOMIC_STATION_PONAPE_1951')
    ASTRONOMICAL_STATION_1952 = _all.get('ASTRONOMICAL_STATION_1952')
    BELLEVUE_IGN = _all.get('BELLEVUE_IGN')
    BISSAU = _all.get('BISSAU')
    BOGOTA_OBSERVATORY = _all.get('BOGOTA_OBSERVATORY')
    CAMPO_INCHAUSPE = _all.get('CAMPO_INCHAUSPE')
    CANTON_ASTRO_1966 = _all.get('CANTON_ASTRO_1966')
    CHATHAM_ISLAND_ASTRO_1971 = _all.get('CHATHAM_ISLAND_ASTRO_1971')
    CHUA_ASTRO = _all.get('CHUA_ASTRO')
    CORREGO_ALEGRE = _all.get('CORREGO_ALEGRE')
    DOS_1968 = _all.get('DOS_1968')
    EASTER_ISLAND_1967 = _all.get('EASTER_ISLAND_1967')
    EUROPEAN_1950 = _all.get('EUROPEAN_1950')
    EUROPEAN_1979 = _all.get('EUROPEAN_1979')
    GUX_1_ASTRO = _all.get('GUX_1_ASTRO')
    GEODETIC_DATUM_1949 = _all.get('GEODETIC_DATUM_1949')
    GRACIOSA_BASE_SW_1948 = _all.get('GRACIOSA_BASE_SW_1948')
    HJORSEY_1955 = _all.get('HJORSEY_1955')
    HONG_KONG_1963 = _all.get('HONG_KONG_1963')
    HU_TZU_SHAN = _all.get('HU_TZU_SHAN')
    ISTS_061_ASTRO_1968 = _all.get('ISTS_061_ASTRO_1968')
    ISTS_073_ASTRO_1969 = _all.get('ISTS_073_ASTRO_1969')
    JOHNSTON_ISLAND_1961 = _all.get('JOHNSTON_ISLAND_1961')
    KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951 = _all.get('KAPINGAMARANGI_ASTRONOMIC_STATION_NO_3_1951')
    KERGUELEN_ISLAND_1949 = _all.get('KERGUELEN_ISLAND_1949')
    KUSAIE_ASTRO_1951 = _all.get('KUSAIE_ASTRO_1951')
    LEMUTA = _all.get('LEMUTA')
    MIDWAY_ASTRO_1961 = _all.get('MIDWAY_ASTRO_1961')
    NOT_RECORDED = _all.get('NOT_RECORDED')
    AFGOOYE = _all.get('AFGOOYE')
    IRELAND_1965 = _all.get('IRELAND_1965')
    WGS84_WORLD_GEODETIC_SYSTEM_1984 = _all.get('WGS84_WORLD_GEODETIC_SYSTEM_1984')
    KOREAN_GEODETIC_SYSTEM_1995 = _all.get('KOREAN_GEODETIC_SYSTEM_1995')
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
