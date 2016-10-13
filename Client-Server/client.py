import socket, string
import random 

SERVERHOST = "192.168.120.12"                 
SERVERPORT = 8888
NAME = 'Python Client' + str(random.randrange(1,1000,1))

class MyClient:
   _host = SERVERHOST
   _port = SERVERPORT;
   _name = NAME

   def __init__(self, host, port, name):
       if host is not None:
           self._host = host
       if port is not None:
           self._port = port
       if name is not None:
           self._name = name
       print "MyClient::__init__", self._host, self._port, self._name;
   
   def run(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self._sock.connect((self._host, int(self._port)))        
        self._sock.send(bytes(NAME))  
        self._data = self._sock.recv(1024)
        if self._data is not None:
            print "\tRECEIVE:", self._data
        self._sock.close()
        
myclient = MyClient(SERVERHOST, SERVERPORT, NAME)
myclient.run()
#myclient.stop()
        