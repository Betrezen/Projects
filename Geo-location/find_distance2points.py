import math
def latLngToDegress(val):
  min, degress = math.modf(val)
  sec, min = math.modf(min * 60)
  sec = sec * 60
  return degress,min,sec
  
#cos(d) = sin(fА)·sin(fB) + cos(fА)·cos(fB)·cos(lА - lB),
#fА и fB — широты, 
#lА, lB — долготы данных пунктов
#d — расстояние между пунктами, измеряемое в радианах длиной дуги большого круга земного шара.
#L = d·R,
#R = 6371 км — средний радиус земного шара.
def distance(point1, point2):
    """ return distance in meters between 2 points """
    EarthRadius = 6371
    lat1, lon1 = point1
    lat2, lon2 = point2
    # need to convert to radian
    lat1, lon1, lat2, lon2 = math.radians(lat1), math.radians(lon1), math.radians(lat2), math.radians(lon2)
    cos_d_rad = math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2)
    print cos_d_rad
    #degrees = 180 * radians / pi
    #radians = pi * degrees / 180
    d = math.acos(cos_d_rad)
    print d
    L = d * EarthRadius * 1000
    return L

distance((64.28, 100.22),(40.71,-74.01))    
  