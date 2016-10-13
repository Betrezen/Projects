from twisted.internet import reactor, protocol


class FingerClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        self.transport.write("moshez\r\n")

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print "connection lost"
        reactor.stop()


if __name__ == '__main__':
    factory = protocol.ClientFactory()
    factory.protocol = FingerClient
    reactor.connectTCP("localhost", 2079, factory)
    reactor.run()
