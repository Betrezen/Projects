#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import json
import sys
from twisted.internet.protocol import Protocol, ClientFactory, ServerFactory, Factory
from twisted.internet.endpoints import TCP4ClientEndpoint
from twisted.application import service, internet
from twisted.internet import reactor, defer, threads
from twisted.python import log, failure
from yamlloader import get_env

env = get_env()
#log.startLogging(open('/var/log/python_server/virtual_guide_serv.log', 'w'))
log.startLogging(sys.stdout)

def checkProtocolVersion(fn):
    def wrapper(self,*args, **kwargs):
        if env.config.mainserver.protocolversion >= self.jsonData.get("protocolversion"):
            return fn(self, *args, **kwargs)
        else:
            raise ValueError("protocolversion is not supported")
    return wrapper

# -------------------  CLIENT ----------------------------------------
class clientProtocol(Protocol):
    def connectionMade(self):
        self.connected = True
        self.factory.clientConnected(self)
    def connectionLost(self, reason):
        self.connected = False
    def sendMessage(self,data):
        self.transport.write(data)
    def dataReceived(self, data):
        self.factory.gotMessage(data)
class clientFactory(ClientFactory):
    protocol = clientProtocol
    def __init__(
            self,
            connect_success_callback,
            connect_fail_callback,
            recv_callback):
        self.connect_success_callback = connect_success_callback
        self.connect_fail_callback = connect_fail_callback
        self.recv_callback = recv_callback
        self.client = None
    def clientConnectionFailed(self, connector, reason):
        self.connect_fail_callback(reason)
    def clientConnected(self, client):
        self.client = client
        self.connect_success_callback()
    def gotMessage(self, msg):
        self.recv_callback(msg)
    def sendMessage(self, msg):
        if self.client:
            self.client.sendMessage(msg)
class Client():
    def __init__(self,reactor,request='Aloha',responceCallback=None,
                host="localhost",port=env.config.get('mainserver',{}).get('mongodbprocess',{}).get('port',6048),lenv=env):
        self.reactor = reactor
        self.responceCallback = responceCallback
        self.host = host
        self.port = port
        self.request = request
        self.responce = None
        self.token = lenv.config.mainserver.mongodbprocess.token
        self.client = clientFactory(
                        self.on_client_connect_success,
                        self.on_client_connect_fail,
                        self.on_client_receive)
        self.connection = self.reactor.connectTCP(self.host, self.port, self.client)
        #point = TCP4ClientEndpoint(reactor, self.host, self.port)
        #d = point.connect(clientFactory())
        #d.addCallback(self.gotConnection)
    def on_client_connect_success(self):
        # we need to prepare DB reqest here like "token" must be added!!!
        self.client.sendMessage(self.request)
    def on_client_connect_fail(self, reason):
        # reason is a twisted.python.failure.Failure  object
        log.err('Connection failed: %s' % reason.getErrorMessage())
        self.responceCallback(reason)
    def on_client_receive(self, msg):
        self.responce = msg
        log.msg('Client reply: %s' % msg)
        log.msg('Disconnecting...')
        self.connection.disconnect()
        self.responceCallback(msg)

# -----------------  SERVER --------------------------
class JsonHandler():
    def __init__(self, inp, callback, errorback, tread=True):
        self.jsonData = None
        self.input  = inp
        self.callback = callback
        self.errorback = errorback
        self.treadflag = tread
        try:
            self.jsonData = json.loads(inp)
            if self.jsonData.get('command') not in env.config.mainserver.commands:
                raise ValueError("command is not supported")
            log.msg("%s json is <%s>"%(self.__class__.__name__,self.jsonData))
        except Exception as ex:
            log.err("Error %s %s"%(self.__class__.__name__,ex.__str__()))
    def dataHandler(self):
        if self.jsonData.get('command') == "search_poi":
            self.searchPOI()
    def searchPOI(self):
        Client(reactor=reactor,request=self.input,responceCallback=self.searchPOICallback)
    def searchPOICallback(self,msg):        
        if isinstance(msg,Exception) or isinstance(msg,failure.Failure):
            self.errorback(msg)
        else:
            jsonmsg = json.loads(msg)
            self.callback(jsonmsg)

### Protocol Implementation
class JsonProtocol(Protocol):
    def connectionMade(self):
        log.msg("Got new client! %s %s"%(self.__class__.__name__,self.transport.getPeer()))
    def connectionLost(self, reason):
        log.msg("Lost a client! %s reason-%s"%(self.__class__.__name__,reason))
        self.transport.loseConnection()
    def dataReceived(self, data):
        log.msg("Received %s <%s>"%(self.__class__.__name__,data))
        try:
            self.responce = JsonHandler(data, callback=self.successResponce,errorback=self.errorResponce).dataHandler()
        except Exception as ex:
            self.errorResponce(ex)
    def successResponce(self,out):
        self.responce = {"protocolversion":"0.9","responce":"OK","data":out}
        log.msg("Sending %s <%s>"%(self.__class__.__name__,repr(self.responce)))
        self.send()

    def errorResponce(self,failure):
        log.err("errorResponce %s %s"%(self.__class__.__name__,failure))
        self.responce = {"protocolversion":"0.9","responce":"ERROR","data":"%s"%failure}
        self.send()

    def send(self):
        self.transport.write(json.dumps(self.responce))

class JsonFactory(ServerFactory):
    def __init__(self, callback=None, errback=None):
        self.callback = callback
        self.errback = errback
        self.protocol = JsonProtocol
    def clientConnectionFailed(self, connector, reason):
        log.err('Connection failed: %s %s'%(self.__class__.__name__,reason.getErrorMessage()))
    def clientConnectionLost(self, connector, reason):
        #log.msg('Connection lost %s <%s>'%(self.__class__.__name__,reason.getErrorMessage()))
        pass

# ----------------- MAIN ----------------------
def main():   
    serverport = env.config.get('mainserver',{}).get('mainprocess',{}).get('port',6047)
    serverfactory = JsonFactory() #callback, errback)    
    reactor.listenTCP(serverport, serverfactory)
    reactor.run()

if __name__ == '__main__':
    main()
