import threading
import socket, string
import sys
import getopt
#from datetime import time
import time

HOST = "109.184.55.159"                 # localhost
#HOST = "localhost"
PORT = 8888
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
      print "Connect from address", self._address
      #receive
      self._data = self._socket.recv(1024)
      if self._data is not None:
          print "\tRECEIVE:", self._data      
      #send
      if self._data is not None:
          self._socket.send(self._data)
      #close connection
      self._socket.close()
      print "Closed connection:", self._address

class MyServer:
  _host = HOST
  _port = PORT;
  _name = NAMESERVER

  def __init__(self, host, port, name):
    if host is not None:
        self._host = host
    if port is not None:
        self._port = port
    if name is not None:
        self._name = name
    print "MyServer::__init__", self._host, self._port, self._name;
    
  def run(self):
    self._srv  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._srv.bind((self._host, int(self._port)))
    self._srv.listen(5)
    self._timestart = time.time()
    self._state = 0 #start
    
    while (self._state == 0):
      #print "Server is up "
      self._sock, self._addr = self._srv.accept()
      ClientThread(self._sock, self._addr).start()
            
  def stop(self):
    self._state = 1 #stop
    self._sock.close()
    self._srv.close()
    #print "Server is down"

 
myserver = MyServer(HOST, PORT, NAMESERVER)
myserver.run()
myserver.stop()


