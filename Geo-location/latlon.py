'''
Маленька библиотека которая находит сегменты полилинии входящие и пересекающие тайл.
Это применимо для карт maps.google.com

Кратко:
Карты выдаются маленькими кусочками, те тайлами где каждый тайл индентифицируется XYZ где
X = число по вертикали и зависит от zoom level
Y = число по вертикали и также зависит от zom level
Z = zoom level
Полилиния представлена набором точек каждая из которых представлена LAT/LON координатами (сферическими координатами).
Необходимо найти тайлы на которых данная полилиния должна быть отрисована.
def optimizatin() возвращает для указанного zoom level набор тайлов и сегментов описывающих часть полилинии для каждого тайла.

В итоге можно легко нарисовать отдельным леером полилинию на карте.

А что это за линия тока вам и известно… путь домой…. любимые тропки парка и тд…

Примеры:
import latlon
polyline =
print latlon.optimizatin(polyline, 13)
print latlon.optimizatin(polyline, 20)

Удачи…
'''
#!/usr/bin/env python
# __author__ = "Kirill Rozin"
# __copyright__ = "Copyright 2011."
# __license__ = "GPL"
# __version__ = "0.0.1"
# __email__ = "krozin@google.com"
# __status__ = "Testing"

import math
import sys
import re

#def toRad(x): return x/180.0*math.pi OR return math.radians(x)
#def toDeg(x): return x/math.pi*180.0 OR return math.degrees(x)
 
# Degrees of latitude per meter
DPM = 8.983345800106980e-006
# Radius of the Earth in meters
RADIUS_EARTH_METERS = 6366197.7236758134307553505349006
MinLatitude = -85.05112878
MaxLatitude = 85.05112878
MinLongitude = -180
MaxLongitude = 180

########################################   OPTIMIZATION  ####################################
def optimization_by_route (polyline, zoom):
    res={}
    for segment in get_segment(polyline):
        bound = get_bbox_from_points(segment, zoom)
        if bound[0] == bound[2] and bound[1] == bound[3]:
            x = bound[0]
            y = bound[1]
            key="%s_%s_%s"%(zoom,x,y)
            if not res.get(key):
                res[key] = []
            res[key].append(segment)            
        else:
            for x in xrange(bound[0], bound[2]+1):
                for y in xrange(bound[1], bound[3]+1):
                    position = segment_tile_position(segment, x, y, zoom)
                    if position[0] == 'IN' or position[0] == 'CROSS':
                        key="%s_%s_%s"%(zoom,x,y)
                        if not res.get(key):
                            res[key] = []
                        res[key].append(segment)
    return res

def optimization_by_box (polyline, zoom):
    res={}
    bound = get_bbox_from_points(polyline, zoom)
    # one tile
    if bound[0] == bound[2] and bound[1] == bound[3]:
        x = bound[0]
        y = bound[1]
        for segment in get_segment(polyline):
            position = segment_tile_position(segment, x, y, zoom)
            if position[0] == 'IN' or position[0] == 'CROSS':
                key="%s_%s_%s"%(zoom,x,y)
                if not res.get(key):
                    res[key] = []
                res[key].append(segment)
    else:
        for x in xrange(bound[0], bound[2]+1):
            for y in xrange(bound[1], bound[3]+1):
                for segment in get_segment(polyline):
                    position = segment_tile_position(segment, x, y, zoom)
                    if position[0] == 'IN' or position[0] == 'CROSS':
                        key="%s_%s_%s"%(zoom,x,y)
                        if not res.get(key):
                            res[key] = []
                        res[key].append(segment)
    return res

def get_segment(polyline):
    segment = None
    last_point=None
    for i in polyline:
        if not last_point:
            last_point = i
            continue
        else:
            segment = [last_point,i]
            yield segment
            last_point = i

################################  GEOM  ####################################################
def angle_delta(alfa, betta):
    """ minimum angle between a & b where a & b defined in degrees """
    x = (alfa - betta) % 360
    if x > 180:
        return (x-360)
    return x

# cos(d) = sin(fA)*sin(fB) + cos(fA)*cos(fB)*cos(lA - lB)
# fA, fB is latitude
# lA, lB is lontitude
# d is distance between points shown as measured in radians, arc length of a great circle of the globe
# L = d*R
# R = 6371 km is midle radius of Earth
def distance(point1, point2):
    """ return distance in meters between 2 points """
    lat1, lon1 = point1
    lat2, lon2 = point2
    # need to convert to radian
    lat1, lon1, lat2, lon2 = math.radians(lat1), math.radians(lon1), math.radians(lat2), math.radians(lon2)
    cos_d_rad = math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(lon1-lon2)
    #print cos_d_rad
    #degrees = 180 * radians / pi
    #radians = pi * degrees / 180
    d = math.acos(cos_d_rad)
    #print d
    L = d * RADIUS_EARTH_METERS
    return L

def move_LatLon(lat, lon, distance_in_meter, angle):
    """ This procedure calculates new point which is moved from the passed point
    to distance d and angle"""
    RADIUS_EARTH_METERS = 6366197.7236758134307553505349006
    lat = math.radians(lat)
    lon = math.radians(lon)
    d = distance_in_meter/RADIUS_EARTH_METERS
    angle = math.radians(angle)
    def mod(x,y):
        return y - x*math.floor(y/x)
    lat_rad = math.asin(math.sin(lat)*math.cos(d)+math.cos(lat)*math.sin(d)*math.cos(angle))
    if math.cos(lat_rad) == 0:
        lon_rad = lon
    else:
        lon_rad=mod(2*math.pi, lon-math.asin(math.sin(angle)*math.sin(d)/math.cos(lat_rad))+math.pi)-math.pi
    return (math.degrees(lat_rad),math.degrees(lon_rad))

def bbox_center(point1, point2):
    """ Return the center of a box. box is defined by top-left/bottom-right or top-right/bottom-left corners. """
    return (point1[0] + point1[1])/2, (point2[0] + point2[1])/2

def get_sortedbox(box):
    """ MATH SYSTEM """
    dbox = {}
    for i in box:
        key="%s_%s"%(i[0],i[1])
        dbox.update({key:(i[0],i[1])})
    print dbox
    x1 = box[0][0]
    y1 = box[0][1]
    x2 = box[1][0]
    y2 = box[1][1]
    x3 = box[2][0]
    y3 = box[2][1]
    x4 = box[3][0]
    y4 = box[3][1]
    xright = max(x1,x2,x3,x4)
    ytop = max(y1,y2,y3,y4)
    xleft = min(x1,x2,x3,x4)
    ybottom = min(y1,y2,y3,y4)
    
    print xright, ytop, xleft, ybottom
    top_right = dbox.get('%s_%s'%(xright,ytop))
    bottom_left = dbox.get('%s_%s'%(xleft,ybottom))
    top_left = dbox.get('%s_%s'%(xleft,ytop))
    bottom_right = dbox.get('%s_%s'%(xright, ybottom))
    return top_left, top_right, bottom_right, bottom_left

def convert_llbox_to_mercatorbox(box):
    mbox=[]
    for i in box:
        x,y = mercatorForward(i[0],i[1])
        mbox.append((x,y))
    return mbox

def point_in_box(point, box):
    top_left, top_right, bottom_right, bottom_left = convert_llbox_to_mercatorbox(box)
    mpoint = mercatorForward(point[0], point[1])
    if top_left and top_right and bottom_right and bottom_left:
        if top_left[0] <= mpoint[0] <= top_right[0] and (bottom_left[1] <= mpoint[1] <= top_left[1] or bottom_right[1] <= mpoint[1] <= top_right[1]):
            return True
    return False

def segment_inside_box(segment, box):
    """ MERCATOR SYSTEM """
    if point_in_box(segment[0], box) and point_in_box(segment[1], box):
        return True       
    return False

def get_bbox_from_points (points, zoom):
    pointList = []
    for point in points:
        x, y = LatLonToxyz(point[0], point[1], zoom)
        pointList.append((x, y))
    maxx = pointList[0][0]
    minx = pointList[0][0]
    maxy = pointList[0][1]
    miny = pointList[0][1]
    for nPoint in pointList:
        if (maxx < nPoint[0]):
            maxx = nPoint[0]
        if (maxy < nPoint[1]):
            maxy = nPoint[1]
        if (minx > nPoint[0]):
            minx = nPoint[0]
        if (miny > nPoint[1]):
            miny = nPoint[1]
    return minx, miny, maxx, maxy

# x,y,z where x,y are center of tile!!!
def get_LLbbox(x,y,z):
    """ Return the bound box segments of a tile. x,y - center of tile for corresponding zoom level """
    lat, lon, width = xyzToLatLon(x,y,z)
    c = (width/2)*math.sqrt(2)    
    top_left_lat, top_left_lon = move_LatLon(lat, lon, c, 45)
    bottom_left_lat, bottom_left_lon = move_LatLon(lat, lon, c, 135)
    bottom_right_lat, bottom_right_lon = move_LatLon(lat, lon, c, 225)
    top_right_lat, top_right_lon = move_LatLon(lat, lon, c, 315)
    return [(top_left_lat, top_left_lon), (top_right_lat, top_right_lon), (bottom_right_lat, bottom_right_lon), (bottom_left_lat, bottom_left_lon)]

def find_intersection(segment,x,y,z):
    """ Return the intersection point of a segment to any segments of box of tile """
    LSegment = LineSegment(segment[0][0], segment[0][1], segment[1][0], segment[1][1])
    box=get_LLbbox(x,y,z)
    top = LineSegment(box[0][0], box[0][1], box[1][0], box[1][1])
    right = LineSegment(box[1][0], box[1][1], box[2][0], box[2][1])
    bottom = LineSegment(box[2][0], box[2][1], box[3][0], box[3][1])
    left = LineSegment(box[3][0], box[3][1], box[0][0], box[0][1])
    bbox_segments = [top, right, bottom, left]
    for box_segment in bbox_segments:
        res = MercatorFindLLIntersection(LSegment, box_segment)
        if res[0] == 'INTERESECTING':
            return res
        elif res[0] == 'COINCIDENT':
            return res
        elif res[0] == 'PARALLEL':
            continue
        elif res[0] == 'NOT_INTERESECTING':
            continue
    return None, None, None

def segment_tile_position(segment, x,y,z):
    box = get_LLbbox(x,y,z)
    if segment_inside_box(segment, box):
        return 'IN', []
    else:
        res = find_intersection(segment, x,y,z)
        if res[0] == 'INTERESECTING' or res[0] == 'COINCIDENT':
            return 'CROSS', res[1]
    return 'OUT', []

#####################################  MAP INFO  ##################################
class Point:
    def __init__(self, lat, lon):
        self.x = float(lat)
        self.y = float(lon)

class LineSegment:
    def __init__(self, p1_x, p1_y, p2_x, p2_y):
        self.p1 = Point(p1_x, p1_y)
        self.p2 = Point(p2_x, p2_y)

def ZoomInfo(zoomlevel, tilesize_in_pixel=256, lat=33.9305):
    mapsize_in_tiles = (2**zoomlevel)
    mapsize_in_pixel = (2**zoomlevel)*tilesize_in_pixel
    # it depend on lat. Please, be careful
    map_resolution = GroundResolution(lat, zoomlevel, tilesize_in_pixel)
    map_scale = MapScale(lat, zoomlevel, tilesize_in_pixel, screenDpi=96)
    return 'FOR zoomlevel=%s and lat=%s'%(zoomlevel,lat), \
           'mapsize_in_tiles=%s'%mapsize_in_tiles, \
           'mapsize_in_pixel=%s'%mapsize_in_pixel, \
           'map_resolution where %s meters per 1 pixel'%map_resolution, \
           'map_scale=%s'%map_scale

""" Clips a number to the specified minimum and maximum values.
    n The number to clip.
    minValueMinimum allowable value.
    maxValueMaximum allowable value.
    returns: The clipped value."""
def Clip(n, minValue, maxValue):
    return min(max(n, minValue), maxValue)

""" Determines the map width and height (in pixels) at a specified level of detail.
    zoomlevelLevel of detail, from 1 (lowest detail) to 23 (highest detail).
    returns: The map width and height in pixels."""
def MapSize(zoomlevel, tilesize_in_pixel=256):
    return (2**zoomlevel)*tilesize_in_pixel

""" Determines the ground resolution (in meters per pixel)
    at a specified latitude and level of detail.
    latitudeLatitude (in degrees) at which to measure the ground resolution.
    zoomlevelLevel of detail, from 1 (lowest detail) to 23 (highest detail).
    returns: The ground resolution, in meters per pixel."""
def GroundResolution(latitude, zoomlevel, tilesize_in_pixel=256):
    latitude = Clip(latitude, MinLatitude, MaxLatitude)
    return (math.cos(latitude * math.pi/180) * 2 * math.pi * RADIUS_EARTH_METERS)/((2**zoomlevel)*tilesize_in_pixel)

""" Determines the map scale at a specified latitude, level of detail, and screen resolution.
    latitudeLatitude (in degrees) at which to measure the map scale.
    zoomlevelLevel of detail, from 1 (lowest detail) to 23 (highest detail).
    screenDpiResolution of the screen, in dots per inch.
    returns: The map scale, expressed as the denominator N of the ratio 1 : N."""
def MapScale(latitude, zoomlevel, tilesize_in_pixel=256, screenDpi=96):
    return GroundResolution(latitude, zoomlevel, tilesize_in_pixel) * screenDpi / 0.0254

################################  TRANSFORMATION  ##################################
def toseconds(l):
    sign = ''
    if l < 0:
        l = -l
        sign = '-'
    degrees = int(l)
    l = (l - degrees)*60
    minutes = int(l)
    seconds = (l - minutes)*60
    return "%s%d %02d'%02d''" % (sign, degrees, minutes, seconds)

def mercatorReverse(x, y):
    def boundMercator(x):
        return min(max(x, -math.pi), math.pi)
    lon = math.degrees(boundMercator(x))
    lat = math.degrees(math.atan(math.sinh(boundMercator(y))))
    return lat, lon

def mercatorForward(lat, lon):
    def boundPi(l):
        while l < -math.pi:
            l += math.pi * 2
        while l > math.pi:
            l -= math.pi * 2
        return l
    def boundLat(lat):
        LAT_BOUND = math.radians(89)
        return min(max(boundPi(lat), -LAT_BOUND), LAT_BOUND)
    x = boundPi(float(math.radians(lon)))
    lat = boundLat(math.radians(lat))
    y = math.log(math.tan(lat) + 1.0 / math.cos(lat))
    return x, y

def latLngToDegress(val):
    min, degress = math.modf(val)
    sec, min = math.modf(min * 60)
    sec = sec * 60
    return degress,min,sec

def xyzToLatLon(x, y, z):
    RADIUS_EARTH_METERS = 6366197.7236758134307553505349006
    q  = 2*math.pi / math.pow(2, z+1)
    cx = (q * (2*x+1)) - math.pi
    cy = math.pi - (q * (2*y+1))
    lat, lon = mercatorReverse(cx, cy)
    width = (2*math.pi * RADIUS_EARTH_METERS * math.cos(math.radians(lat))) / math.pow(2.0,z);
    return (lat, lon, width)

def LatLonToxyz(lat, lon, z, expect_int=True):
    rotate = 0
    fs = math.sin(math.radians(-rotate))
    fc = math.cos(math.radians(-rotate))
    cos_lat = math.cos(math.radians(lat))
    x, y = mercatorForward(lat, lon)
    q = 2*math.pi / math.pow(2, z+1)
    xx = ((x+math.pi)/q - 1)/2
    yy = ((math.pi-y)/q - 1)/2
    if expect_int:
        return int(round(xx)), int(round(yy))
    return xx, yy

def xyztoQuadkey(x, y, z):
    s = ""
    for i in xrange(0, z):
        d = 48
        ii = z - i
        mask = 1 << (ii - 1)
        if x & mask:
            d = d + 1
        if y & mask:
            d = d + 2
        s = s + chr(d)
    return s

""" Converts a point from latitude/longitude WGS-84 coordinates (in degrees) 
    into pixel XY coordinates at a specified level of detail.
    latitudeLatitude of the point, in degrees.
    longitudeLongitude of the point, in degrees.
    zoomlevelLevel of detail, from 1 (lowest detail) to 23 (highest detail).
    pixelXOutput parameter receiving the X coordinate in pixels.
    pixelYOutput parameter receiving the Y coordinate in pixels."""
def LatLongToPixelXY(latitude, longitude, zoomlevel, tilesize_in_pixel=256):
    latitude = Clip(latitude, MinLatitude, MaxLatitude)
    longitude = Clip(longitude, MinLongitude, MaxLongitude)
    x = (longitude + 180) / 360
    sinLatitude = math.sin(latitude * math.pi/180)
    y = 0.5 - math.log((1 + sinLatitude) /(1 - sinLatitude))/(4 * math.pi)
    mapSize = MapSize(zoomlevel, tilesize_in_pixel)
    pixelX = Clip(x * mapSize + 0.5, 0, mapSize - 1)
    pixelY = Clip(y * mapSize + 0.5, 0, mapSize - 1)
    return pixelX, pixelY

""" Converts a pixel from pixel XY coordinates at a specified 
    level of detail into latitude/longitude WGS-84 coordinates (in degrees).
    pixelXX coordinate of the point, in pixels.
    pixelYY coordinates of the point, in pixels.
    levelOfDetailLevel of detail, from 1 (lowest detail) to 23 (highest detail).
    latitudeOutput parameter receiving the latitude in degrees.
    longitudeOutput parameter receiving the longitude in degrees."""
def PixelXYToLatLong(pixelX, pixelY, zoomlevel, tilesize_in_pixel=256):
    mapSize = MapSize(zoomlevel, tilesize_in_pixel)
    x = (Clip(pixelX, 0, mapSize - 1) / mapSize) - 0.5
    y = 0.5 - (Clip(pixelY, 0, mapSize - 1) / mapSize)
    latitude = 90 - (360*math.atan(math.exp(-y * 2 * math.pi))/math.pi)
    longitude = 360 * x
    return latitude, longitude

""" Converts pixel XY coordinates into tile XY coordinates 
    of the tile containing the specified pixel.
    pixelXPixel X coordinate.
    pixelYPixel Y coordinate.
    tileXOutput parameter receiving the tile X coordinate.
    tileYOutput parameter receiving the tile Y coordinate."""
def PixelXYToTileXY(pixelX, pixelY, tilesize_in_pixel=256):
    tileX = pixelX / tilesize_in_pixel
    tileY = pixelY / tilesize_in_pixel
    return tileX, tileY

""" Converts tile XY coordinates into pixel XY coordinates of the upper-left pixel of the specified tile.
    tileXTile X coordinate.
    tileYTile Y coordinate.
    pixelXOutput parameter receiving the pixel X coordinate.
    pixelYOutput parameter receiving the pixel Y coordinate."""
def TileXYToPixelXY(tileX, tileY, tilesize_in_pixel=256):
    pixelX = tileX * tilesize_in_pixel
    pixelY = tileY * tilesize_in_pixel
    return pixelX, pixelY


###################################   INTERSECTION  ##########################################
""" searching crossing segments or coincident/parallel segments.
    Please, paid on attansion that it is math system.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MathFindIntersection(segment1, segment2):
    denom =  ((segment2.p2.y - segment2.p1.y)*(segment1.p2.x - segment1.p1.x))- \
             ((segment2.p2.x - segment2.p1.x)*(segment1.p2.y - segment1.p1.y))
    nume_a = ((segment2.p2.x - segment2.p1.x)*(segment1.p1.y - segment2.p1.y)) - \
             ((segment2.p2.y - segment2.p1.y)*(segment1.p1.x - segment2.p1.x))
    nume_b = ((segment1.p2.x - segment1.p1.x)*(segment1.p1.y - segment2.p1.y)) - \
             ((segment1.p2.y - segment1.p1.y)*(segment1.p1.x - segment2.p1.x))
    if denom == 0.0:
        if nume_a == 0.0 and nume_b == 0.0:
            coincident_x1 = None
            coincident_y1 = None
            coincident_x2 = None
            coincident_y2 = None
            # coincident_y1
            if segment1.p1.y < segment1.p2.y:
                if segment1.p1.y <= segment2.p1.y <= segment1.p2.y:
                    coincident_y1 = segment2.p1.y
                elif segment1.p1.y <= segment2.p2.y <= segment1.p2.y:
                    coincident_y1 = segment2.p2.y
            else:
                if segment1.p2.y <= segment2.p1.y <= segment1.p1.y:
                    coincident_y1 = segment2.p1.y
                elif segment1.p2.y <= segment2.p2.y <= segment1.p1.y:
                    coincident_y1 = segment2.p2.y
            # coincident_y2
            if segment2.p1.y < segment2.p2.y:
                if segment2.p1.y <= segment1.p1.y <= segment2.p2.y:
                    coincident_y2 = segment1.p1.y
                elif segment2.p1.y <= segment1.p2.y <= segment2.p2.y:
                    coincident_y2 = segment1.p2.y
            else:
                if segment2.p2.y <= segment1.p1.y <= segment2.p1.y:
                    coincident_y2 = segment1.p1.y
                elif segment2.p2.y <= segment1.p2.y <= segment2.p1.y:
                    coincident_y2 = segment1.p2.y
            # coincident_x1
            if segment1.p1.x < segment1.p2.x:
                if segment1.p1.x <= segment2.p1.x <= segment1.p2.x:
                    coincident_x1 = segment2.p1.x
                elif segment1.p1.x <= segment2.p2.x <= segment1.p2.x:
                    coincident_x1 = segment2.p2.x
            else:
                if segment1.p2.x <= segment2.p1.x <= segment1.p1.x:
                    coincident_x1 = segment2.p1.x
                elif segment1.p2.x <= segment2.p2.x <= segment1.p1.x:
                    coincident_x1 = segment2.p2.x
            # coincident_x2
            if segment2.p1.x < segment2.p2.x:
                if segment2.p1.x <= segment1.p1.x <= segment2.p2.x:
                    coincident_x2 = segment1.p1.x
                elif segment2.p1.x <= segment1.p2.x <= segment2.p2.x:
                    coincident_x2 = segment1.p2.x
            else:
                if segment2.p2.x <= segment1.p1.x <= segment2.p1.x:
                    coincident_x2 = segment1.p1.x
                elif segment2.p2.x <= segment1.p2.x <= segment2.p1.x:
                    coincident_x2 = segment1.p2.x
            return 'COINCIDENT', (coincident_x1, coincident_y1, coincident_x2, coincident_y2)
        return 'PARALLEL', (None, None)
    ua = (nume_a / denom)
    ub = (nume_b / denom)
    if ua >= 0.0 and ua <= 1.0 and ub >= 0.0 and ub <= 1.0:
        intersection_x = segment1.p1.x + ua*(segment1.p2.x - segment1.p1.x)
        intersection_y = segment1.p1.y + ua*(segment1.p2.y - segment1.p1.y)
        return 'INTERESECTING', (intersection_x, intersection_y)
    return 'NOT_INTERESECTING', (None, None)

""" searching crossing segments or coincident/parallel segments.
    Please, paid on attansion that it is MERCATOR system.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MercatorFindLLIntersection(segment1, segment2):
    x11, y11 = mercatorForward(float(segment1.p1.x), float(segment1.p1.y))
    x12, y12 = mercatorForward(float(segment1.p2.x), float(segment1.p2.y))
    x21, y21 = mercatorForward(float(segment2.p1.x), float(segment2.p1.y))
    x22, y22 = mercatorForward(float(segment2.p2.x), float(segment2.p2.y))
    segment_a = LineSegment(x11,y11,x12,y12)
    segment_b = LineSegment(x21,y21,x22,y22)
    result, xy = MathFindIntersection(segment_a, segment_b)
    if result == 'INTERESECTING':
        ll_x, ll_y = mercatorReverse(xy[0], xy[1])
        return result, (ll_x, ll_y)
    if result == 'COINCIDENT':
        if None not in xy:
            ll_x1, ll_y1 = mercatorReverse(float(xy[0]), float(xy[1]))
            ll_x2, ll_y2 = mercatorReverse(float(xy[2]), float(xy[3]))
            return result, (ll_x1, ll_y1, ll_x2, ll_y2)
        return 'None', None
    # just for comments
    #elif result == 'PARALLEL':
    #elif result == 'NOT_INTERESECTING':
    return MathFindIntersection(segment_a, segment_b)

""" searching crossing segments or coincident/parallel segments.
    Please, paid on attansion that it is MERCATOR system.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def PixelFindIntersection(segment1, segment2, zoomlevel=15, tilesize_in_pixel=256):
    p1 = LatLongToPixelXY(segment1.p1.x, segment1.p1.y, zoomlevel, tilesize_in_pixel)
    p2 = LatLongToPixelXY(segment1.p2.x, segment1.p2.y, zoomlevel, tilesize_in_pixel)
    p3 = LatLongToPixelXY(segment2.p1.x, segment2.p1.y, zoomlevel, tilesize_in_pixel)
    p4 = LatLongToPixelXY(segment2.p2.x, segment2.p2.y, zoomlevel, tilesize_in_pixel)
    s1 = LineSegment(int(p1[0]),int(p1[1]), int(p2[0]), int(p2[1]))
    s2 = LineSegment(int(p3[0]),int(p3[1]), int(p4[0]), int(p4[1]))
    return MathFindIntersection(s1, s2)

######################################   SHIFTING   ######################################
""" We try to shift segment2 against segment1 to right or up.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MakeMathShifting(segment, side='right', shift=1):
    # y = kx+b; k = (y2-y1)/(x2-x1); b = (y1*x2-y2*x1)/(x2-x1)
    # along OX. Move segment to up
    if side == 'up':
        nlat1, nlon1 = segment.p1.x, segment.p1.y+shift
        nlat2, nlon2 = segment.p2.x, segment.p2.y+shift
    #elif side == 'right':
    # along OY or k!=0 Move segment2 to right
    else:
        nlat1, nlon1 = segment.p1.x+shift, segment.p1.y
        nlat2, nlon2 = segment.p2.x+shift, segment.p2.y
    return nlat1,nlon1,nlat2,nlon2

""" We try to shift segment2 against segment1 to right or up depend on distance in meters.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MakeLLShifting(segment, side='right', shift=10, angle=0):
    # shift - in meters
    lat1 = float(segment.p1.x)
    lon1 = float(segment.p1.y)
    lat2 = float(segment.p2.x)
    lon2 = float(segment.p2.y)
    if side == 'up':
        nlat1, nlon1 = move(float(lat1), float(lon1), shift, 0)
        nlat2, nlon2 = move(float(lat2), float(lon2), shift, 0)
    elif side == 'right':
        nlat1, nlon1 = move(float(lat1), float(lon1), shift, 270)
        nlat2, nlon2 = move(float(lat2), float(lon2), shift, 270)
    else:
        nlat1, nlon1 = move(float(lat1), float(lon1), shift, angle)
        nlat2, nlon2 = move(float(lat2), float(lon2), shift, angle)
    return nlat1,nlon1,nlat2,nlon2

""" We try to shift point to right or up depend on distance in meters.
    params: (lat,lon)
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MakePointLLShifting(point, side='right', shift=30, angle=0):
    # shift in meters
    lat1 = float(point[0])
    lon1 = float(point[1])
    if side == 'up':
        nlat1, nlon1 = move(lat1, lon1, shift, 0)
    elif side == 'right':
        nlat1, nlon1 = move(lat1, lon1, shift, 270)
    else:
        nlat1, nlon1 = move(lat1, lon1, shift, angle)
    return nlat1,nlon1

""" We try to shift segment2 against segment1 to right or up depend on distance in pixels.
    params: segment1 and segment2
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MakePixelsShifting(segment, side='right', shift=2, zoomlevel=15, tilesize_in_pixel=256):
    # due to OX_OY different in pixel system where 0,0 -> top_left; x,y ->bottom_right
    # shift in pixels
    lat1 = float(segment.p1.x)
    lon1 = float(segment.p1.y)
    lat2 = float(segment.p2.x)
    lon2 = float(segment.p2.y)
    if side == 'up':
        px1, py1 = LatLongToPixelXY(lat1, lon1, zoomlevel, tilesize_in_pixel) #lat/lon
        px2, py2 = LatLongToPixelXY(lat2, lon2, zoomlevel, tilesize_in_pixel) #lat/lon
        py1 = py1 - shift
        py2 = py2 - shift
        nlat1, nlon1 = PixelXYToLatLong(px1, py1, zoomlevel, tilesize_in_pixel)
        nlat2, nlon2 = PixelXYToLatLong(px2, py2, zoomlevel, tilesize_in_pixel)
    #elif side == 'right':
    else:
        px1, py1 = LatLongToPixelXY(lat1, lon1, zoomlevel, tilesize_in_pixel) #lat/lon
        px2, py2 = LatLongToPixelXY(lat2, lon2, zoomlevel, tilesize_in_pixel) #lat/lon
        px1 = px1 + shift
        px2 = px2 + shift
        nlat1, nlon1 = PixelXYToLatLong(px1, py1, zoomlevel, tilesize_in_pixel)
        nlat2, nlon2 = PixelXYToLatLong(px2, py2, zoomlevel, tilesize_in_pixel)
    return nlat1,nlon1,nlat2,nlon2

""" We try to shift point to right or up depend on distance in pixels and zoomlevel.
    params: (lat,lon)
    return: INTERESECTING/NOT_INTERESECTING/COINCIDENT/PARALLEL and + some additional info."""
def MakeOnePixelShifting(point, side='right', shift=2, zoomlevel=15):
    # due to OX_OY different in pixel system where 0,0 -> top_left; x,y ->bottom_right
    # shift in pixels
    lat1 = point[0] #lat
    lon1 = point[1] #lon
    if side == 'up':
        px1, py1 = LatLongToPixelXY(lat1, lon1, zoomlevel) #lat/lon
        py1 = py1 - shift
        nlat1, nlon1 = PixelXYToLatLong(px1, py1, zoomlevel)
    #elif side == 'right':
    else:
        px1, py1 = LatLongToPixelXY(lat1, lon1, zoomlevel) #lat/lon
        px1 = px1 + shift
        nlat1, nlon1 = PixelXYToLatLong(px1, py1, zoomlevel)
    return nlat1,nlon1

######################################  MAIN  ############################################
def help():
    print """
       latlon.py -f x y z     # convert xyz to lat/lon/width
       latlon.py -f 'x=XXX&y=YYY&z=ZZZ'
       latlon.py -r lat lon z # return x and y for zoom"""

def main():
    if len(sys.argv) < 2:
        help()
        return
    if sys.argv[1] == '-f':
        r = None
        if len(sys.argv)==5:
            params = [int(x) for x in sys.argv[2:5]]
            r = xyzToLatLon(params[0], params[1], params[2])
        elif len(sys.argv)==3:
            m = re.search('x=(\d+).*y=(\d+).*z=(\d+)', sys.argv[2], re.IGNORECASE)
            if m:
                params = [int(x) for x in m.group(1,2,3)]
                r = xyzToLatLon(params[0], params[1], params[2])
        if not r:
            help()
            return
        print "lat/lon: %f %f   width: %f" % (r[0], r[1], r[2])
        print "lat/log: %s, %s" % (toseconds(r[0]), toseconds(r[1]))
        return

    if sys.argv[1] == '-r':
        params = [float(x) for x in sys.argv[2:5]]
        print LatLonToxyz(params[0], params[1], int(params[2]))
        return
    help()


def test():
    for z in range(4,11):
        m = (1 << z) - 1
        print z, m*m
        for x in range(0, m):
            for y in range(0, m):
                lat, lon, width = xyzToLatLon(x,y,z)
                r = LatLonToxyz(lat, lon, z)
                if x != r[0] or y != r[1]:
                    print x,y,z,lat,lon,r[0],r[1]

def test1():
    import get_route
    routeid=get_route.get_routeid([33.931326,-118.384084,33.931575,-118.363227]).encode('base64').strip('\n')
    points=get_route.get_polyline_points(routeid)
    routeid=get_route.get_routeid([33.931575,-118.363227, 33.938465,-118.36799]).encode('base64').strip('\n')
    points.extend(get_route.get_polyline_points(routeid))
    routeid=get_route.get_routeid([33.938465,-118.36799, 33.930542, -118.3755]).encode('base64').strip('\n')
    points.extend(get_route.get_polyline_points(routeid))
    zoom=16
    bbox = latlon.get_bbox_from_points(points,zoom)
    res = latlon.get_points_for_each_tile(points,zoom)
    print bbox
    print res
    for k,v in res.items():
        for i in xrange(bbox[0],bbox[2]):
            for j in xrange(bbox[1],bbox[3]):
                if k == "%s_%s"%(i,j):
                    print k,v


if __name__ == "__main__":
    main()
#    test()


###############################  XLAM ##############################################
def get_points_for_each_tile(points,zoom):
    res={}
    previous_tile_point = None
    previous_point = None
    previous_key = ''
    for point in enumerate(points):
        x, y = LatLonToxyz(point[1][0], point[1][1], zoom)
        key="%s_%s"%(x,y)
        if not res.get(key):
            res[key] = []
            if previous_point:
                res[key].append([previous_point[1]])
                res[key][0].append(point[1])
            else:
                res[key].append([point[1]])
        else:
            if previous_key == key:
                list_index = len(res[key]) - 1
                if (point[0] - previous_point[0]) == 1:
                    res[key][list_index].append(point[1])
            else: # change happens
                # create new list. add to new.
                list_index = len(res[key]) - 1
                res[key].append([previous_point[1]])
                res[key][list_index+1].append(point[1])
                if res.get(previous_key):
                    list_index = len(res[previous_key]) - 1
                    res[previous_key][list_index].append(point[1])
        previous_point = point
        if previous_key != key:
            previous_key = key
    return res
    #print "%s"%(get_points_for_each_tile(points,15))

#polyline = [(33.55946124, -117.72948682), (33.55935931, -117.72943318), (33.55897307, -117.72910058), (33.55875313, -117.72877872), (33.55860293, -117.72840858), (33.55853319, -117.72815108), (33.55850101, -117.72757173), (33.55856001, -117.72716939)]
#latlon.optimization_by_route(polyline,22) == latlon.optimization_by_box(polyline,22)