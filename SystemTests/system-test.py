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
python = env.config.mainserver.python
pythonopt = env.config.mainserver.pythonopt
testdir = env.config.mainserver.testdir
logfile = env.config.mainserver.logfile
htmlfile = env.config.mainserver.htmlfile
        
class TestThread(threading.Thread):

    def __init__(self, index, taskqueue, resultqueue):
        self.index = index
        threading.Thread.__init__(self)
        self.taskqueue = taskqueue
        self.resultqueue = resultqueue
        self._logfilename = None
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
        print "%02d>%s" % (self.index, s)

    def process(self, s):
        for x in s.split('\n'):
            self.output(x)
            self.checkline(x)

    def checkline(self, s):
        r_tt = re.search(r"^Ran (\d+) tests in (\d+)", s)
        r_stat = re.search(r"<unittest.runner.TextTestResult run=(\d+) errors=(\d+) failures=(\d+)", s)
        if r_tt:
            r_total_tests = int(r_tt.group(1));
            r_total_time = int(r_tt.group(2));
            self.status = dict(total=r_total_tests, time=r_total_time)            
        elif r_stat:
            total  = int(r_stat.group(1))
            errored= int(r_stat.group(2))
            failed = int(r_stat.group(3))
            passed = int(total-errored-failed)
            status = "PASSED"
            if errored>0 or passed>0:
                status = "FAILED"
            if len(self.status) > 0:
                self.status.update(status=status, errored=errored, failed=failed, passed=passed)

    def run(self):
        try:
            while not self.taskqueue.empty():
                try:
                    self.testname = self.taskqueue.get(False, 0.1)
                except Queue.Empty:
                    break

                self.output("run test: %s, log: %s" % (self.testname, self.logfilename()))
                p = subprocess.Popen([python, pythonopt, os.path.join(testdir, self.testname), '-f', self.logfilename()],
                                     shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p.communicate()
                #print self.taskqueue
                #print p

                f = open(self.logfilename(), 'r')
                for l in f.xreadlines():
                    self.process(l.rstrip())
                f.close()
                print "STATUS:%s\n"%self.status
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

    def parse_command_line(self):
        parser = OptionParser()
        parser.add_option('--email', action="store", help="send result to email", dest="email")
        parser.add_option('-n', action="store", help="number of test workers. By default it cpucount*2", dest="workercount")
        (opt, args) = parser.parse_args()
        global options
        options = opt

    def run(self):
        tests = [f for f in os.listdir(testdir) if f.endswith('.py')]
        testQueue = Queue.Queue(0)
        resultQueue = Queue.Queue(0)
        for t in tests:
            testQueue.put(t)
        total = testQueue.qsize()
        starttime = time.time()
        threads = []
        for i in xrange(0, self.threads_num):
            t = TestThread(i, testQueue, resultQueue)
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
        print self.mk_statistics(res, runtime, self.color)
        self.mk_html_statistics(res, runtime)
        send_report(self.mk_statistics(res, runtime, self.colorless), self.mk_html_statistics(res, runtime))

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

    def mk_statistics(self, res, runtime, color):
        testcount = len(res)
        total, failed, errored, passed, time = 0,0,0,0,0
        lines = []
        lines.append("%30s   Total Failed Errored Passed Time" % ('name'))
        for r in res:
            name, log, status = r
            if status:
                t = status['total']
                f = status['failed']
                e = status['errored']
                p = status['passed']
                tt = status['time']
                total  += t
                failed += f
                errored+= e
                passed += p
                time   += float(tt)
                if f + e == 0:
                    c = color('green')
                else:
                    c = color('red')
                lines.append(c + "%30s  %5d %6d %7d %6d %5ds" % (name[:30], t, f, e, p, int(tt)) + color('reset'))
            else:
                lines.append(color('red') + "%30s" % (name[:30]) + color('reset'))
        lines.append("Tests: %d Total: %d Failed: %d, Errored: %d, Passed: %d, testtime: %s, runtime: %s" % \
               (testcount, total, failed, errored, passed, self.sec2str(time), self.sec2str(runtime)))
        logf = open(logfile,"w+")
        for i in lines:
            logf.write(i)
            logf.write('\n')
        logf.close()
        return "\n".join(lines)

    def mk_html_statistics(self, res, runtime):
        html_header = """
        <html>
            <head>
                <title>system-test report</title>
                <META http-equiv="Content-Style-Type" content="text/css">
            </head>
            <body><center><H1>System-test report</H1></center>
        """
        html_bottom = """</body></html>"""
        html_table = """<table><tr>%s</tr>%s</table>"""
        testcount = len(res)
        total, failed, errored, passed, time = 0,0,0,0,0
        html_table_header = " ".join(["<th>%s</th>" % name for name in ['Name', 'Total', 'Failed', 'Errored', 'Passed', 'Time']])

        rows = []
        for r in res:
            name, log, status = r
            if status:
                t = status['total']
                f = status['failed']
                e = status['errored']
                p = status['passed']
                tt = status['time']
                total  += t
                failed += f
                errored+= e
                passed += p
                time   += tt
                if f + e == 0:
                    font_color = 'green'
                else:
                    font_color = 'red'
                html_table_row = " ".join(["<td>%s</td>" % val for val in [name, t, f, e, p, tt]])
                html_table_row = '<tr style="color: %s; text-align: center">%s</tr>' % (font_color, html_table_row)
            else:
                font_color = 'red'
                html_table_row = '<tr style="color: %s; text-align: center;"><td>%s</td></tr>' % (font_color, name)
            rows.append(html_table_row)
        table = html_table % (html_table_header, "             \n".join(rows))
        total_stat = "<p><b>Test file: %d, Total test case: %d Failed: %d, Errored: %d, Passed: %d, testtime: %s, runtime: %s</b>" % \
                                (testcount, total, failed, errored, passed, self.sec2str(time), self.sec2str(runtime))
        res = [html_header, table, total_stat, html_bottom]
        htmlf = open(htmlfile,"w+")
        htmlf.write("\n".join(res))
        htmlf.close()
        return "\n".join(res)

def main():
    runalltests = BulkRunSystemTests()
    runalltests.parse_command_line()
    runalltests.run()

if __name__ == "__main__":
    sys.exit(main())
