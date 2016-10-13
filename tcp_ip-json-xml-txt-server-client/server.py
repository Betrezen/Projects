import sys, os, getopt, time
#import daemon
#from daemon import runner

import threading
import socket, string, json

import logging
logging.basicConfig(filename='/tmp/python_server.log',filemode = 'w', level=logging.DEBUG, format = '%(asctime)s %(levelname)s %(message)s')

import xmlprocessor
import xml

#HOST = "109.184.55.159"            # localhost
#HOST = "ec2-54-200-187-137.us-west-2.compute.amazonaws.com"
HOST = "localhost"
PORT = 7777
NAMESERVER = "SIMPLE SERVER"

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

class ClientThread(threading.Thread):
    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, socket, address):
        self._socket = socket
        self._address = address
        threading.Thread.__init__(self)

    def run(self):
      logging.info ("Connect from address %s"%str(self._address))
      #receive
      BLOK=1000000 #1MB
      self._data = self._socket.recv(BLOK)
      self._datatype = 'txt'
      self._inputdata = None
      if self._data is not None:
          #logging.info ("\tRECEIVE: %s"%self._data)
          try:
            self._inputdata = json.loads(self._data)
            self._datatype = 'json'
            logging.info ("\tRECEIVE JSON: %s" % self._inputdata)
          except ValueError:
            logging.info ("\t-- CANNOT BE INTERPRETTED AS JSON. SORRY...")
            try:
              self._inputdata = xmlprocessor.XML2DICT.xmltodict(self._data)
              self._datatype = 'xml'
              logging.info ("\tRECEIVE XML: and transformed to dict = %s" % self._inputdata)
              dom = xml.dom.minidom.parseString(self._data)
              logging.info ("\tRECEIVE XML: without transformation= %s" % dom.toxml())
            except:
            #except xmlprocessor.FormatError:
                logging.info ("\t-- CANNOT BE INTERPRETTED AS XML. SORRY...")
                self._inputdata = self._data
                logging.info ("\tRECEIVE TXT:  %s" % self._inputdata)
      #send
      if self._data is not None:
          if self._datatype == 'json':
            self._socket.send(json.dumps(self._inputdata))
          elif self._datatype == 'xml':
            self._socket.send(xmlprocessor.XML2DICT.dicttoxml(self._inputdata))
          else:
            self._socket.send(self._inputdata)
      #close connection
      self._socket.close()
      logging.info ("Closed connection: %s"%str(self._address))

    def json_reply(self, request):
        jdata = json.loads(request)
        return jdata
    
class MyServer:
  _host = HOST
  _port = PORT;
  _name = NAMESERVER
  _pid = os.getpid()
  def __init__(self, host=HOST, port=PORT, name=NAMESERVER, pid=os.getpid(), daemon=0):
    if daemon:
        self.stdin_path = '/dev/null'
        self.stdout_path = '/tmp/python_server_daemon.log'
        self.stderr_path = '/tmp/python_server_daemon.log'
        self.pidfile_path =  '/tmp/python_server_daemon.pid'
        self.pidfile_timeout = 5
    if host is not None:
        self._host = host
    if port is not None:
        self._port = port
    if name is not None:
        self._name = name
    if pid is not None:
        self._pid = pid
    logging.info ("MyServer::__init__   HOST=%s  PORT=%s  NAME=%s  PID=%s"%(self._host, self._port, self._name, str(self._pid)))

  def run(self):
    self._srv  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._srv.bind((self._host, int(self._port)))
    self._srv.listen(5)
    self._timestart = time.time()
    self._state = 0 #start    
    while True:
      logging.info ("Server is up")
      self._sock, self._addr = self._srv.accept()
      ClientThread(self._sock, self._addr).start()

  def stop(self):
    self._state = 1 #stop
    self._sock.close()
    self._srv.close()
    logging.info ("Server is down")
 
if __name__ == "__main__":
    app = MyServer(HOST, PORT, NAMESERVER)
    app.run()    
    
    '''
    logger = logging.getLogger('')
    hdlr = logging.FileHandler('/tmp/python_server.log','w')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    context = daemon.DaemonContext(files_preserve = [hdlr.stream,],)
    context.open()
    with context:
        app.run(pid=os.getpid())
    '''
    
    #daemon_runner = runner.DaemonRunner(app)
    #daemon_runner.filesPreserve = [hdlr]
    #daemon_runner.do_action()
    
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            #daemon_runner.start()
            pass
        elif 'stop' == sys.argv[1]:
            #daemon_runner.stop()
            pass
        elif 'restart' == sys.argv[1]:
            #daemon_runner.restart()
            pass
        else:
            logging.info ("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        logging.info ("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
