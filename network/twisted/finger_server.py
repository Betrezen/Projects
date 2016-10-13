# Read username, output from non-empty factory, drop connections
# Use deferreds, to minimize synchronicity assumptions
# Write application. Save in 'finger.tpy'

from twisted.application import internet, service
from twisted.internet import protocol, reactor, defer
from twisted.protocols import basic


class FingerProtocol(basic.LineReceiver):

    def lineReceived(self, user):
        print 'Requested user:', user
        d = self.factory.get_user(user)

        def onError(err):
            return 'Internal error in server'
        d.addErrback(onError)

        def writeResponse(message):
            self.transport.write(message + '\r\n')
            self.transport.loseConnection()
        d.addCallback(writeResponse)


class FingerFactory(protocol.ServerFactory):

    protocol = FingerProtocol

    def __init__(self, **kwargs):
        self.users = kwargs

    def get_user(self, user):
        return defer.succeed(self.users.get(user, "No such user"))

    def get_user_dalayed(self, user):
        d = defer.Deferred()
        reactor.callLater(1, d.callback, self.users.get(user, "No such user"))
        return d

if __name__ == '__main__':
    reactor.listenTCP(2079, FingerFactory(moshez='Happy and well'))
    reactor.run()
