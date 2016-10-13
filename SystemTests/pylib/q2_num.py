#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import struct
from datetime import date


def unpack_number(source, format, text):
    try:
        number = struct.unpack(format, source)[0]
        print "\t%s:\t\t%s" %(text, number)
        return number
    except struct.error:
        return None

def unpackint(source):
    source = '\0' * (struct.calcsize('>Q') - len(source)) + source
    res =  unpack_number(source, '>Q', "uint")
    if res:
        try:
            print "\tUnixTime:\t%s" % date.fromtimestamp(res)
            print "\tGPSTime:\t%s"  % date.fromtimestamp(res + 315964800.0)
        except:
            pass
    return res

def unpack_gps(source):
    try:
        ts, lat, lon, hed, hvel, hunc, huncang, huncperp = struct.unpack('>LllHHBBB', source)
        deg2latlon = 180./2**25    #180/2**25 degrees, WGS-84 ellipsoid
        print "\tLatitude\t\t%s" % ( lat * deg2latlon )
        print "\tLongitude\t\t%s" % ( lon * deg2latlon )
        print "\tSpeed\t\t%s m/s, %s km/h" % ( hvel*.25, hvel*.25*3.6 )
        return 1
    except struct.error:
        return None

def main(argv=None):
    if len(argv) < 2:
        print 'usage: %s <number>' % argv[0]
        print 'parameters:'
        print '-g\tdecode gps packet'
    else:
        offset = 1
        if '-g' in argv:
            offset = 2
        for string in argv[offset:]:
            string = string.strip("|")

            try:
                decoded = string.decode('base64')
                print "'%s' ->b64 '%s' -> " % (string, decoded)
            except:
                try:
                    decoded = string.replace('\\"', '"').decode('string-escape')
                    print "'%s' ->esc '%s' -> " % (string, decoded)
                except:
                    decoded = string
                    print "'%s' -> " % string

            if '-g' in argv:
                res1 = unpack_gps(decoded)
                res2 = res3 = 1
            else:
                res1 = unpack_number(decoded, '>d', "double")
                res2 = unpack_number(decoded, '>f', "float")
                res3 = unpackint(decoded)
            if (res1 == None) & (res2 == None) | (res3 == None):
                print "\tcan't decode"


if __name__ == '__main__':
    sys.exit(main(sys.argv))
