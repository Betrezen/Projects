import sys
import json
from twisted.internet.protocol import Protocol, ServerFactory
#from twisted.application import service, internet
from twisted.internet import reactor, defer, threads
from twisted.python import log

from mongodbservice import MongoBDService
from yamlloader import get_env

env = get_env()
#log.startLogging(open('/var/log/python_server/mongoprocess.log', 'w')) 
log.startLogging(sys.stdout)

def checkMongoProcessToken(fn):
    def wrapper(self,*args, **kwargs):
        if env.config.get('mainserver',{}).get('mongodbprocess',{}).get('token',None) == self.jsonData.get("token"):
            return fn(self, *args, **kwargs)
        else:
            raise ValueError("token is not valid")
    return wrapper

def envReload(fn):
    def wrapper(self,*args, **kwargs):
        env._reload()
        return fn(self, *args, **kwargs)
    return wrapper

class MongoJsonHandler():
    def __init__(self, inc):
        self.jsonData = {"result":"FALT", "reason":None}
        try:
            self.jsonData = json.loads(inc)
        except Exception as ex:
            log.err('Eroor %s %s'%(self.__class__.__name__,ex.__str__()))
            self.jsonData.update({"reason":"%s"%ex.__str__()})

    @checkMongoProcessToken
    @envReload
    def dataHandler(self, callback, errorback, tread=True):
        if not tread:
            d = defer.Deferred()
            result = MongoBDService(env.config).helf_check()
            d.addCallback(callback)
            d.addErrback(errorback)
            d.callback(result)
        else:
            d = threads.deferToThread(MongoBDService().helf_check)
            d.addCallback(callback)
            d.addErrback(errorback)
        return d


### Protocol Implementation
class MongoJsonProtocol(Protocol):
    #responce = {"protocolversion":"0.9","command":"None","result":"None","data":"None"}
    def connectionMade(self):
        log.msg("Got new client! %s %s"%(self.__class__.__name__,self.transport.getPeer()))
    def connectionLost(self, reason):
        #log.msg("Lost a client! %s reason-%s"%(self.__class__.__name__,reason))
        self.transport.loseConnection() #self.transport.abortConnection()
    def dataReceived(self, data):
        log.msg("Received %s <%s>"%(self.__class__.__name__,repr(data)))
        try:
            self.responce = MongoJsonHandler(data).dataHandler(callback=self.sendResponce,errorback=self.errorResponce)
        except Exception as ex:
            self.errorResponce(ex)
    def sendResponce(self,out):
        self.responce = {"protocolversion":"0.9",
                         "command":"helf_check",
                         "result":"OK",
                         "data":"%s"%out}
        self.transport.write(json.dumps(self.responce))
        log.msg("Sending %s <%s>"%(self.__class__.__name__,repr(self.responce)))        
    def errorResponce(self,failure):
        log.err("Error %s %s"%(self.__class__.__name__,failure))
        self.responce = {"protocolversion":"0.9",
                         "command":"helf_check",
                         "result":"ERROR",
                         "data":"%s"%failure}
        self.transport.write(json.dumps(self.responce))


class MongoJsonFactory(ServerFactory):    
    def __init__(self, callback=None, errback=None):
        self.callback = callback
        self.errback = errback
        self.protocol = MongoJsonProtocol
    def clientConnectionFailed(self, connector, reason):
        log.err('Connection failed: %s %s'%(self.__class__.__name__, reason.getErrorMessage()))
    def clientConnectionLost(self, connector, reason):
        #log.msg('Connection lost %s %s'%(self.__class__.__name__, reason.getErrorMessage()))
        pass

def main():
    factory = MongoJsonFactory()
    port = env.config.get('mainserver',{}).get('mongodbprocess',{}).get('port',6048)
    reactor.listenTCP(port, factory)
    reactor.run()

if __name__ == '__main__':
    main()