class Coordinates(object):
    
    class Builder(object):
        def __init__(self):
            self._lat = None
            self._lng = None
        
        def lat(self, val):
            self._lat = val
            return self

        def lng(self, val):
            self._lng = val
            return self
        
        def build(self):
            return Coordinates(self)

    def __init__(self, builder):
        self._lat = builder._lat
        self._lng = builder._lng
    

#class Calculator(object):
#    
#    @staticmethod
#    def calculateCoordinatePrecision(Coordinates coordinates):
#        pass
