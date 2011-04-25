import copy

class LatLng(object):
    def __init__(self, lng, lat):
        self._lng = lng
        self._lat = lat
        
    def getlng(self):
        return self._lng
    lng = property(fget=getlng)

    def getlat(self):
        return self._lat
    lat = property(fget=getlat)

    def valid(self):
        return self.lat >= -90 and self.lat <= 90 \
            and self.lng >= -180 and self.lng <= 180

    def __str__(self):
        return 'Lng=%s, Lat=%s' % (self.lat, self.lng)

class Coordinates(object):
    
    def __init__(self, config):
        self._config = copy.copy(config)
        
    def get_datum(self):
        return self._config.get('datum')
    datum = property(fget=get_datum)
            
    def get_latdir(self):
        return self._config.get('latdir')
    latdir = property(fget=get_latdir)

    def get_lngdir(self):
        return self._config.get('lngdir')
    lngdir = property(fget=get_lngdir)

    def get_point(self):
        return self._config.get('point')
    point = property(fget=get_point)

    def get_source(self):
        return self._config.get('source')
    source = property(fget=get_source)

    def get_system(self):
        return self._config.get('system')
    system = property(fget=get_system)

    def get_unit(self):
        return self._config.get('unit')
    unit = property(fget=get_unit)

        
        

if __name__ == '__main__':
    c = Coordinates({'point': LatLng(1, 2)})
    print c.point

#class Calculator(object):
#    
#    @staticmethod
#    def calculateCoordinatePrecision(Coordinates coordinates):
#        pass
