import threading
import socket
import time

HOST = "0.0.0.0"
PORT = 5555
NAMESERVER = "ECHO SERVER"


class ClientThread(threading.Thread):

    # Override Thread's __init__ method to accept the parameters needed:
    def __init__(self, socket, address):
        self._socket = socket
        self._address = address
        threading.Thread.__init__(self)

    def run(self):
        print "Connect from address", self._address
        # receive
        self._data = self._socket.recv(1024)
        if self._data is not None:
            print "\tRECEIVE:", self._data
        # send
        if self._data is not None:
            self._socket.send(self._data)
        # close connection
        self._socket.close()
        print "Closed connection:", self._address


class TcpServer(object):

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name

    def run(self):
        self._srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._srv.bind((self.host, int(self.port)))
        self._srv.listen(5)  # the maximum number of queued connections
        self._timestart = time.time()
        self._state = 0  # start

        print "Server is up"
        while self._state == 0:
            self._sock, self._addr = self._srv.accept()
            ClientThread(self._sock, self._addr).start()

    def stop(self):
        self._state = 1  # stop
        self._sock.close()
        self._srv.close()
        print "Server is down"


if __name__ == '__main__':
    myserver = TcpServer(HOST, PORT, NAMESERVER)
    myserver.run()
