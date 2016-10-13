#SystemCurlTests$ python system-test.py

import Queue
import threading
import time
import random
import os
import re
import sys
import subprocess
import tempfile
from optparse import OptionParser
from pylib.yamlloader import get_env
from pylib.sendemail import send_report

env=get_env('server.conf')
testdir = env.config.mainserver.testdir
logfile = env.config.mainserver.logfile
htmlfile = env.config.mainserver.htmlfile
curl_http_v = env.config.mainserver.curl.curl_http_v
curl_cookie_save = env.config.mainserver.curl.cookie_save
curl_cookie_use = env.config.mainserver.curl.cookie_use
curl_content_type = env.config.mainserver.curl.content_type
curl_request_type = env.config.mainserver.curl.request_type
curl_url = env.config.mainserver.curl.server_url
        
class TestCurlThread(threading.Thread):
    def __init__(self, index, taskqueue, resultqueue, curl_options=None):
        self.index = index
        threading.Thread.__init__(self)
        self.taskqueue = taskqueue
        self.resultqueue = resultqueue
        self._logfilename = None
        if curl_options:
            self.curl_http_v = curl_options.get("http-v","--http1.0")        
            self.curl_cookie_save = curl_options.get("cookie_save","-c cookie.txt")
            self.curl_cookie_use = curl_options.get("cookie_use","-d cookie.txt")
            self.culr_content_type = curl_options.get("content_type","-H 'Content-Type: application/xml'")
            self.culr_request_type = curl_options.get("request_type","-X POST")
            self.culr_url = curl_options.get("url", None)
        else:
            self.curl_http_v = curl_http_v
            self.curl_cookie_save = curl_cookie_save
            self.curl_cookie_use = curl_cookie_use
            self.culr_content_type = curl_content_type
            self.culr_request_type = curl_request_type
            self.culr_url = curl_url
        self.curl_cookiesave = "curl %s %s %s %s %s "% (self.curl_http_v,self.curl_cookie_save,self.culr_content_type,self.culr_request_type,self.culr_url)
        self.curl_request = "curl %s %s %s %s %s " % (self.curl_http_v,self.curl_cookie_use,self.culr_content_type,self.culr_request_type,self.culr_url)
        self.cleanup()

    def logfilename(self):
        if self._logfilename is None:
            t = tempfile.mkstemp(prefix = 'tmp_system_' + self.testname)
            os.close(t[0])
            self._logfilename = t[1]
        return self._logfilename

    def cleanup(self):
        if self._logfilename:
            os.remove(self._logfilename)
            self._logfilename = None
        self.testname = None
        self.failedtests = []
        self.status = dict()

    def output(self, s):
        f = open(logfile,'a+')
        f.write(s+'\n')
        print "%02d>%s" % (self.index, s)

    def process(self, s):
        for x in s.split('\n'):
            self.output(x)
            #self.checkline(x)

    def checkline(self, s):
        pass

    def run(self):
        try:            
            while not self.taskqueue.empty():
                try:
                    self.testname = self.taskqueue.get(False, 0.1)
                except Queue.Empty:
                    break
                xml_file = open(testdir+'/'+self.testname,'r')
                xml_text = ""
                for line in xml_file:
                    xml_text += line.strip('\n')
                xml_request = "%s -d '%s'"%(self.curl_request,xml_text)
                p = subprocess.check_output(xml_request, shell=True)
                self.output("TEST: %s, log: %s" % (self.testname, self.logfilename()))                                                
                self.output("INPUT:%s \n" % (xml_request))
                self.output("OUTPUT:%s \n====================================================================\n" % (p))
                f = open(self.logfilename(), 'r')
                for l in f.xreadlines():
                    self.process(l.rstrip())
                f.close()
                self.resultqueue.put((self.testname, self.logfilename(), self.status))
                #self.cleanup()
        except KeyboardInterrupt:
            self.output("!! KeyboardInterrupt")
            sys.exit(1)

class BulkRunSystemTests(object):
    def __init__(self):
        cpu_count = os.sysconf('SC_NPROCESSORS_ONLN')
        self.threads_num = cpu_count*4
        self.options = None
        self._colors = dict(black=0, red=1, green=2, yellow=3, blue=4, Magenta=5, cyan=6, white=7)
        self.test_run = False
        self.env=get_env('server.conf')

    def color(self,name):
        if name == 'reset' or name == 'end':
            return '\033[0m'
        return '\033[%dm' % (self._colors[name] + 30)

    def colorless(self,name):
        return ""

    def run(self):
        tests = [f for f in os.listdir(testdir) if f.endswith('.xml')]
        testQueue = Queue.Queue(0)
        resultQueue = Queue.Queue(0)
        for t in tests:
            testQueue.put(t)
        total = testQueue.qsize()
        starttime = time.time()
        threads = []
        for i in xrange(0, self.threads_num):
            t = TestCurlThread(i, testQueue, resultQueue)
            threads.append(t)
            t.start()

        completed = False
        timestamp = time.time()
        while not completed:
            completed = True
            tasks = []
            for t in threads:
                if t.isAlive():
                    completed = False
                    tt = t.testname
                    if tt:
                        tasks.append(t.testname)
            time.sleep(0.5)
            if time.time() - timestamp > 10:
                print self.color('green'), "progress: %d/%d. active tests: %s" % (resultQueue.qsize(), total, ','.join(tasks)), self.color('end')
                timestamp = time.time()
        runtime = time.time() - starttime
        res = []
        while not resultQueue.empty():
            res.append(resultQueue.get())
        res.sort()

    def sec2str(self,sec):
        sec = int(sec)
        m = sec / 60
        h = m / 60
        sec = sec % 60
        res = ''
        if h:
            res = res + "%dh" % h
        if h or m:
            res = res + "%dm" % m
        return res + "%ds" % sec

def main():
    runalltests = BulkRunSystemTests()
    runalltests.run()

if __name__ == "__main__":
    sys.exit(main())
