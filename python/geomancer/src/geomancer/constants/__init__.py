class DatumSpec(object):    
    def __init__(self, key, name, ellipsoidName, flatting, axis):
        self._key = key
        self._name = name
        self._ellipsoidName = ellipsoidName
        self._flattening = flatting
        self._axis = axis

    def get_key(self):
        return self._key
    key = property(get_key)

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
   

class Datum(object):
    set = {}
    ANNA_1_ASTRO_1965 = DatumSpec("ANNA_1_ASTRO_1965", "Anna 1 Astro 1965", "Australian National", 298.250000, 6378160.000000)
    set[ANNA_1_ASTRO_1965._key] = ANNA_1_ASTRO_1965
    
    @staticmethod
    def get_set():
        return Datum.set
