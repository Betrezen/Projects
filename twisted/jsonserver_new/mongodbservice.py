import time
from twisted.python import log

import sys
from pymongo import Connection, GEO2D, DESCENDING
from yamlloader import get_env

# Degrees of latitude per meter
DPM = 8.983345800106980e-006

#log.startLogging(open('/var/log/python_server/mongoprocess.log', 'w+')) 
#log.startLogging(sys.stdout)
#log.startLogging(open(get_env().config.get('mainserver',{}).get('logfile','/var/log/python_server/mongoprocess.log'), 'w'))
log.startLogging(sys.stdout)

"""
python -c "import mongodbservice; md = mongodbservice.MongoBDService(); print 'helf_check: %s' % md.helf_check()"
"""

class MongoBDService(object):
    def __init__(self, env=get_env(), host=None, port=None):
        self.host = None
        self.port = None
        self.connection = None
        self.databasename = None
        self.dbConfig = None
        self.db = None
        # if host and port were not defined then let's get it from config
        if not (host and port):
            if env:
                self.dbConfig = env.config.mainserver.mongodbserver
                if self.dbConfig:
                    self.host = env.config.mainserver.mongodbserver.host
                    self.port = env.config.mainserver.mongodbserver.port
                    self.databasename = env.config.mainserver.mongodbserver.dbname
                    #self.searchkeys = env.mainserver.mongodbserver.tables.public_routes.search_data_keys
                    self.default_limit = env.config.mainserver.mongodbserver.default_limit
        # or host and port were provided then just take it
        elif host and port:
            self.host, self.port = host, port
        # OK host and port are defined. Let's make the connections
        if self.host and self.port and self.databasename:
            self.connection = Connection(self.host, self.port)
            self.db = self.connection[self.databasename]
        # O.. No... host and port are not defined and we have to go away
        else:
            return

    def helf_check(self):        
        time.sleep(3)
        #raise ValueError("You used an odd number!")
        if self.db and self.connection:
            return self.db.collection_names() is not None
        return False

    def create(self):
        try:
            if self.db:
                table = self.db['tables']
                table.create_index([("latlon", GEO2D)])
                table.create_index([("unique_stop_id", DESCENDING)])
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
"""
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
    def find_by_unique_id(self, unique_stop_id, lim=self.default_limit):
        return self.table.find({"unique_stop_id": unique_stop_id}).limit(lim)

    def find_all(self, lim=self.default_limit):
        return self.table.find().limit(lim)
        
    # latlon [1,2]; box [latlon latlon]
    def find_by_latlon(self, latlon=None, radius=None, box=None, lim=self.default_limit):
        if radius and latlon:
            radius_per_latlon = DPM * radius
            return self.table.find({"latlon": {"$within": {"$center": [latlon, radius_per_latlon]}}}).limit(lim)
        elif box:
            return self.table.find({"latlon": {"$within": {"$box": box}}}).limit(lim)
        elif latlon:
            return self.table.find({"lotlon": {"near": latlon}}).limit(lim)
        return {}

"""


"""
EXAMPLES
http://api.mongodb.org/python/2.0/tutorial.html
>>> import pymongo
>>> from pymongo import Connection
>>> connection = Connection()
>>> connection = Connection('localhost', 27017)
>>> db = connection.test_database
>>> db = connection['test-database']
>>> collection = db.test_collection
>>> import datetime
>>> post = {"author": "Mike"}
>>> posts = db.posts
>>> posts.insert(post)
ObjectId('5145f2a42d9c83529a000000')
>>> db.collection_names()
[u'posts', u'system.indexes']
>>> collection
Collection(Database(Connection('localhost', 27017), u'test-database'), u'test_collection')
>>> posts.find_one()
{u'_id': ObjectId('5145f2a42d9c83529a000000'), u'author': u'Mike'}
>>> posts.find_one({"author": "Mike"})
{u'_id': ObjectId('5145f2a42d9c83529a000000'), u'author': u'Mike'}
"""