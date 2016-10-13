__author__ = 'krozin'

import Queue
from multiprocessing import Process, Lock, cpu_count
import os
import requests
from pylib.yamlloader import get_env

class Resource(object):
    def __init__(self, env):
        self.env = env

class HttpResource(Resource):
    def do(self):
        url = self.env.url
        r = requests.get(url)
        return r.text

class Loader(object):
    def __init__(self,filename):
        self.env = get_env(filename)
        self.resourceQueue = []#Queue.Queue(0)
        self.resultQueue = []#Queue.Queue(0)
        print self.env.config.resources.keys()
        for i in self.env.config.resources.keys():
            if self.env.config.resources[i].rtype == "http":
                self.resourceQueue.append(HttpResource(self.env.config.resources[i]))

def f(l, i, mloader):
    l.acquire()
    while len(mloader.resourceQueue)>0:
        try:
            resource = mloader.resourceQueue.pop()
            res = resource.do()
            print "num=%d"%i, "pid=%d"%os.getpid(), "cpu-count=%d"%cpu_count(), "res len =%s"%len(res)
        except Queue.Empty:
            break
    l.release()

if __name__ == '__main__':
    lock = Lock()
    mloader = Loader("resources.conf")
    for num in range(10):
        Process(target=f, args=(lock, num, mloader)).start()