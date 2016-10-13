#
# public_transit_mongodb_layers.py: created 07/25/2001
#
# Copyright (C) 2011 Networks In Motion, Inc. All rights reserved.
#
# The information contained herein is confidential and proprietary to
# Networks In Motion, Inc., and is considered a trade secret as
# defined in section 499C of the California Penal Code. Use of this
# information by anyone other than authorized employees of Networks
# In Motion is granted only under a written non-disclosure agreement
# expressly prescribing the scope and manner of such use.
#

"""Wrapper class to connect and retreive data from public transit PLD."""
__all__ = ['PoitsLayerMongoDB', 'AgencyLayerMongoDB']
__revision__ = '$Id: //depot/nbserver/nim/tesla/voltron5/dev/public_transit/pylib/subr/#1 $'

import csv
import os
import string
from socket import gethostname
from sys import stdout
from pymongo import Connection, GEO2D, DESCENDING

# Degrees of latitude per meter
DPM = 8.983345800106980e-006

class MongoDBConfig(object):
    def __init__(self, filename='./public_transit_feeds.conf'):
        from tesla import envloader
        d = envloader.load_configuration(globals(), filename).get('mongodb')
        object.__setattr__(self,'_selfdict', d)
    def __getattr__(self, name):
        for key, value in  self._selfdict:
            if key == name:
                return self._selfdict[name]               
        return None

mongodb_config = envloader.load_configuration(globals(), './public_transit_feeds.conf').get('mongodb')

from tesla.envconfig import TeslaConfig
class mdbConfig(TeslaConfig):
    def __init__(self):
        TeslaConfig.__init__(self, './public_transit_feeds.conf')


class PoitsLayerMongoDB(object):
    def __init__(self, host=None, port=None):
        if host and port:
            self.host, self.port = host, port
            self.connection = Connection(self.host, self.port)
        else:
            self.connection = Connection()
        self.databasename = str(ptenv.mongodb.databasename)
        self.db = self.connection[self.databasename]
        self.data_keys = ptenv.mongodb.public_transit_tables.transit_points.search_data_keys.keys()
        self.default_limit = ptenv.mongodb.public_transit_tables.transit_points.default_limit

    def create(self):
        try:
            if self.db:
                self.table = self.db[ptenv.mongodb.public_transit_tables.transit_points.name]
                self.table.create_index([("latlon", GEO2D)])
                self.table.create_index([("unique_route_id", DESCENDING)])
                self.table.create_index([("route_type", DESCENDING)])
                self.table.create_index([("unique_route_id", DESCENDING), \
                                         ("shape_id", DESCENDING),\
                                         ("sequence", DESCENDING)])
                return True
            return False
        except:
            return False

    def delete(self):
        try:
            self.table.drop()
            return True
        except:
            return False

    def save(self, values, check_dublicate=True):
        if check_dublicate:
            if isinstance(values, dict):
                res = self.table.find_one({"unique_route_id": values.get('unique_route_id'),\
                                        "shape_id":values.get('shape_id'),\
                                        "sequence":values.get('sequence')})
                if not res:
                    return self.table.insert(values)
                else:
                    return self.table.update(res, values)
            elif isinstance(values, list):
                for i in values:
                    res = self.table.find_one({"unique_route_id": i.get('unique_route_id'),\
                                        "shape_id":i.get('shape_id'),\
                                        "sequence":i.get('sequence')})
                    if not res:
                        return self.table.insert(i)
                    else:
                        return self.table.update(res, i)
        return self.table.insert(values)

    def remove(self, values):
        res = self.table.find_one({"unique_route_id": values.get('unique_route_id'),\
                                        "shape_id":values.get('shape_id'),\
                                        "sequence":values.get('sequence')})
        if res and res.get('ObjectId'):
            self.table.remove(res.get('ObjectId'))
            return True
        return False

    # latlon [1,2]; box [latlon latlon]
    def find_by_latlon(self, latlon=None, radius=None, box=None, lim=1000):
        if radius and latlon:
            radius_per_latlon = DPM * radius
            return self.table.find({"latlon": {"$within": {"$center": [latlon, radius_per_latlon]}}}).limit(lim)
        elif box:
            return self.table.find({"latlon": {"$within": {"$box": box}}}).limit(lim)
        elif latlon:
            return self.table.find({"lotlon": {"near": latlon}}).limit(lim)
        return {}

    def find_by_rid(self, rid, shape_id=None, sequence=None, lim=1000):
        if not sequence:
            return self.table.find({"unique_route_id": rid})
        return self.table.find({"unique_route_id": rid, "shape_id":shape_id, "sequence":sequence,}).limit(lim)

class AgencyLayerMongoDB(object):
    def __init__(self, host=None, port=None):
        if host and port:
            self.host, self.port = host, port
            self.connection = Connection(self.host, self.port)
        else:
            self.connection = Connection()
        self.databasename = str(ptenv.mongodb.databasename)
        self.db = self.connection[self.databasename]
        self.data_keys = ptenv.mongodb.public_transit_tables.transit_agency.data_keys.keys()
        self.default_limit = ptenv.mongodb.public_transit_tables.transit_agency.default_limit

    def create(self):
        try:
            if self.db:
                self.table = self.db[ptenv.mongodb.public_transit_tables.transit_agency.name]
                self.table.create_index([("unique_agency_id", DESCENDING)])
                self.table.create_index([("unique_agency_id", DESCENDING),\
                                         ("agency_id", DESCENDING),\
                                         ("agency_name", DESCENDING)])
                return True
            return False
        except:
            return False

    def delete(self):
        try:
            self.table.drop()
            return True
        except:
            return False

    def save(self, values, check_dublicate=True):
        if check_dublicate:
            if isinstance(values, dict):
                res = self.table.find_one({"unique_agency_id": values.get('unique_agency_id')})
                if not res:
                    return self.table.insert(values)
                else:
                    return self.table.update(res, values)
            elif isinstance(values, list):
                for i in values:
                    res = self.table.find_one({"unique_agency_id": i.get('unique_agency_id')})
                    if not res:
                        return self.table.insert(i)
                    else:
                        return self.table.update(res, i)
        return self.table.insert(values)

    def remove(self, values):
        res = self.table.find_one({"unique_agency_id": values.get('unique_agency_id')})
        if res and res.get('ObjectId'):
            self.table.remove(res.get('ObjectId'))
            return True
        return False

    # latlon [1,2]; box [latlon latlon]
    def find_by_unique_id(self, unique_agency_id, lim=1000):
        return self.table.find({"unique_agency_id": unique_agency_id}).limit(lim)

    def find_all(self, lim=1000):
        return self.table.find().limit(lim)

class StopsLayerMongoDB(object):
    def __init__(self, host=None, port=None):
        if host and port:
            self.host, self.port = host, port
            self.connection = Connection(self.host, self.port)
        else:
            self.connection = Connection()
        self.databasename = str(ptenv.mongodb.databasename)
        self.db = self.connection[self.databasename]
        self.data_keys = ptenv.mongodb.public_transit_tables.transit_stop.data_keys.keys()
        self.default_limit = ptenv.mongodb.public_transit_tables.transit_stop.default_limit

    def create(self):
        try:
            if self.db:
                self.table = self.db[ptenv.mongodb.public_transit_tables.transit_stop.name]
                self.table.create_index([("latlon", GEO2D)])
                self.table.create_index([("unique_stop_id", DESCENDING)])
                return True
            return False
        except:
            return False

    def delete(self):
        try:
            self.table.drop()
            return True
        except:
            return False

    def save(self, values, check_dublicate=True):
        if check_dublicate:
            if isinstance(values, dict):
                res = self.table.find_one({"unique_stop_id": values.get('unique_stop_id')})
                if not res:
                    return self.table.insert(values)
                else:
                    return self.table.update(res, values)
            elif isinstance(values, list):
                for i in values:
                    res = self.table.find_one({"unique_stop_id": i.get('unique_stop_id')})
                    if not res:
                        return self.table.insert(i)
                    else:
                        return self.table.update(res, i)
        return self.table.insert(values)

    def remove(self, values):
        res = self.table.find_one({"unique_stop_id": values.get('unique_stop_id')})
        if res and res.get('ObjectId'):
            self.table.remove(res.get('ObjectId'))
            return True
        return False

    # latlon [1,2]; box [latlon latlon]
    def find_by_unique_id(self, unique_stop_id, lim=1000):
        return self.table.find({"unique_stop_id": unique_stop_id}).limit(lim)

    def find_all(self, lim=1000):
        return self.table.find().limit(lim)
        
    # latlon [1,2]; box [latlon latlon]
    def find_by_latlon(self, latlon=None, radius=None, box=None, lim=1000):
        if radius and latlon:
            radius_per_latlon = DPM * radius
            return self.table.find({"latlon": {"$within": {"$center": [latlon, radius_per_latlon]}}}).limit(lim)
        elif box:
            return self.table.find({"latlon": {"$within": {"$box": box}}}).limit(lim)
        elif latlon:
            return self.table.find({"lotlon": {"near": latlon}}).limit(lim)
        return {}