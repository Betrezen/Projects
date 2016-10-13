#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import json
from twisted.internet.protocol import ClientFactory
#from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from yamlloader import get_env
env = get_env()


class JsonClient(Protocol):
    data = {
       "token": env.config.get('mainserver',{}).get('mongodbprocess',{}).get('token',None),
       "protocolversion":'0.9',
       "command": "search_poi",
       "latlon": ['56.3264', 
                  '44.0078'],
       "data": {
           "streetAddress": "Moskovskoe st., 101, app.101",
           "city": "Leningrad",
           "postalCode": 101101
       }
    }
    s = json.dumps(data)

    def connectionMade(self):
        self.transport.write(self.s)
    
    def connectionLost(self, reason):
        print "connection lost"
    
    def dataReceived(self, data):
        try:
            print("Client obtain %s "%data)
            j = json.loads(data)
            if j:
                #print j
                self.transport.loseConnection()
        except Exception as what:
            print ('{"Client::error":"%s"}'%what.__str__())
            return

class JsonClientFactory(ClientFactory):
    protocol = JsonClient

    def clientConnectionFailed(self, connector, reason):
        print 'Client:: connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'Client:: connection lost:', reason.getErrorMessage()
        reactor.stop()


def main():    
    factory = JsonClientFactory()
    reactor.connectTCP('localhost', env.config.mainserver.mainprocess.port, factory)
    reactor.run()

if __name__ == '__main__':
    main()
