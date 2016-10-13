import socket, string, json
import random 

#SERVERHOST = "ec2-54-200-187-137.us-west-2.compute.amazonaws.com"
SERVERHOST = "localhost"
SERVERPORT = 7777
NAME = 'Python Client' + str(random.randrange(1,1000,1))
JSON = json.dumps({"c": 0, "b": 0, "a": 0}, sort_keys=True)
XML = """<?xml version="1.0" encoding="utf-8"?><request><requestType g='sss' k='bbb'>NBI_ISMS_MDN_VERIFICATION_REQUEST</requestType><mdn>9494219858</mdn><language>en-US<l1 hh='90'>l1</l1><l2>l2</l2></language><udid g='10' m='100'>777</udid><udid k='11'>888</udid></request>"""

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
        self.send_something('json')
        self.send_something('xml')
        self.send_something('txt')

    def send_something(self, datatype):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self._sock.connect((self._host, int(self._port)))        

        if datatype == 'json':
            self._sock.send(bytes(JSON))
        elif datatype == 'xml':
            self._sock.send(bytes(XML))
        else:
            self._sock.send(bytes(NAME))
        self._data = self._sock.recv(1000000)
        if self._data is not None:
            if datatype == 'json':
                print "\tRECEIVE JSON:", self._data
            elif datatype == 'xml':
                print "\tRECEIVE XML:", self._data
            else:
                print "\tRECEIVE TXT:", self._data
        self._sock.close()
        return 0

myclient = MyClient(SERVERHOST, SERVERPORT, NAME)
myclient.run()
#myclient.stop()
        