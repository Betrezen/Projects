from twisted.internet import reactor, protocol


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""

    def connectionMade(self):
        self.transport.write("hello, world!")

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()

    def connectionLost(self, reason):
        print "connection lost"
        reactor.stop()


if __name__ == '__main__':
    factory = protocol.ClientFactory()
    factory.protocol = EchoClient
    reactor.connectTCP("localhost", 8000, factory)
    reactor.run()
