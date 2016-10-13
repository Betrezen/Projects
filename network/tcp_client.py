import socket
import random

SERVERHOST = "0.0.0.0"
SERVERPORT = 5555
NAME = 'Python Client ' + str(random.randrange(1, 1000, 1))


class TcpClient:

    def __init__(self, host, port, name):
        self.host = host
        self.port = port
        self.name = name

    def run(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = self._sock.connect((self.host, int(self.port)))

        self._sock.send(bytes(self.name))
        self._data = self._sock.recv(1024)

        if self._data is not None:
            print "\tRECEIVE:", self._data
        self._sock.close()


if __name__ == '__main__':
    myclient = TcpClient(SERVERHOST, SERVERPORT, NAME)
    myclient.run()
