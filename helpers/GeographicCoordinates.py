import math

class GeographicCoordinates:

    def __init__(self, origin = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }):
        self.SetOrigin(origin)

    def SetOrigin(self, origin):

        self.origin = origin
        
        self.isotropic = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        self.ltp = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        self.ellipsoid = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        self.eccentricity = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }

        self.DEGS_PER_RAD = 90.0 / math.atan2(1.0, 0.0) # Degrees per radian
        self.ISOTROPIC_EXTENT = 0.005 # size of ISOTROPIC sweet-spot (degrees)

        self.ellipsoid['x'] = 6378137.0 # WGS84 ellipsoid.
        self.flattening = 1.0 / 298.257223563

        self.eccentricity['x'] = self.flattening * (2 - self.flattening) # First eccentricity (squared).
        self.eccentricity['y'] = 1 / (1 - self.eccentricity['x']) - 1    # Second eccentricity (squared).
        self.ellipsoid['y'] = self.ellipsoid['x'] * (1 - self.flattening)   # Ellipsoid semi-minor axis.

        orgLat = origin['y'] / self.DEGS_PER_RAD
        orgLon = origin['x'] / self.DEGS_PER_RAD
        cosLat = math.cos(orgLat)
        cosLon = math.cos(orgLon)
        sinLat = math.sin(orgLat)
        sinLon = math.sin(orgLon)
        local = { 'x': origin['x'], 'y': origin['y'], 'z': 0.0 }
        unitX = local.copy()
        unitY = local.copy()

        self.dcm0 = { 'x': -sinLon, 'y': cosLon, 'z': 0 }
        self.dcm1 = { 'x': -sinLat * cosLon, 'y': -sinLat * sinLon, 'z': cosLat }
        self.dcm2 = { 'x': cosLat * cosLon, 'y': cosLat * sinLon, 'z': sinLat }

        unitX['x'] += self.ISOTROPIC_EXTENT
        unitY['y'] += self.ISOTROPIC_EXTENT

        local = self.Geo2ecef(local)
        local = self.Ecef2ltp(local)
        
        unitX = self.Geo2ecef(unitX)
        unitX = self.Ecef2ltp(unitX)
    
        unitY = self.Geo2ecef(unitY)
        unitY = self.Ecef2ltp(unitY)

        self.ltp = local.copy()
        
        unitX['x'] = unitX['x'] - local['x']
        unitX['y'] = unitX['y'] - local['y']
        unitX['z'] = unitX['z'] - local['z']
        
        unitY['x'] = unitY['x'] - local['x']
        unitY['y'] = unitY['y'] - local['y']
        unitY['z'] = unitY['z'] - local['z']

        self.isotropic['x'] = math.sqrt(unitX['x'] * unitX['x'] + unitX['y'] * unitX['y'] + unitX['z'] * unitX['z']) / self.ISOTROPIC_EXTENT
        self.isotropic['y'] = math.sqrt(unitY['x'] * unitY['x'] + unitY['y'] * unitY['y'] + unitX['z'] * unitX['z']) / self.ISOTROPIC_EXTENT

    # Refer http://en.wikipedia.org/wiki/Geodetic_system#From_geodetic_to_ECEF_coordinates
    # See also http://www.soi.wide.ad.jp/class/20050026/slides/01/50.html
    def Geo2ecef(self, point):
        longitude = point['x'] / self.DEGS_PER_RAD
        latitude = point['y'] / self.DEGS_PER_RAD
        cosLon = math.cos(longitude)
        cosLat = math.cos(latitude)
        sinLon = math.sin(longitude)
        sinLat = math.sin(latitude)
        sin2Lat = sinLat * sinLat
        radius = self.ellipsoid['x'] / math.sqrt(1.0 - self.eccentricity['x'] * sin2Lat)

        ret = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        ret['x'] = (radius + point['z']) * cosLat * cosLon
        ret['y'] = (radius + point['z']) * cosLat * sinLon
        ret['z'] = ((1.0 - self.eccentricity['x']) * radius + point['z']) * sinLat
        return ret

    def Ecef2ltp(self, point):
        temp = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        temp['x'] = point['x'] * self.dcm0['x'] + point['y'] * self.dcm0['y'] + point['z'] * self.dcm0['z']
        temp['y'] = point['x'] * self.dcm1['x'] + point['y'] * self.dcm1['y'] + point['z'] * self.dcm1['z']
        temp['z'] = point['x'] * self.dcm2['x'] + point['y'] * self.dcm2['y'] + point['z'] * self.dcm2['z']

        ret = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        ret['x'] = temp['x'] - self.ltp['x']
        ret['y'] = temp['y'] - self.ltp['y']
        ret['z'] = temp['z'] - self.ltp['z']
        return ret

    def Geo2Iso(self, point):
        ret = { 'x': 0.0, 'y': 0.0, 'z': 0.0 }
        ret['x'] = (point['x'] - self.origin['x']) * self.isotropic['x'];
        ret['y'] = (point['y'] - self.origin['y']) * self.isotropic['y'];
        return ret
    
    def Degrees2DecimalDegrees(self, ddmm):
        dd = math.floor(ddmm / 100.0);
        if ddmm < 0:
            dd = math.ceil(ddmm / 100.0);
        return ((ddmm - dd * 100.0) / 60.0) + dd;

#origin = { 'x': -27.889721333333334, 'y': 153.31460316666667, 'z': 0.0 }
#print ("origin (lat,lon)", origin)

#geo = GeographicCoordinates(origin)

#loc = geo.Geo2Iso(origin)
#print ("origin (metres)", loc)

#new = { 'x': -28.889721333333334, 'y': 153.31460316666667, 'z': 0.0 }
#loc = geo.Geo2Iso(new)
#print ("metres from origin", loc)
