import zmq
import sys
import random

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

NAME = 'Client ' + str(random.randrange(1, 1000, 1))

context = zmq.Context()
print "Connecting to server..."
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect("tcp://localhost:%s" % port1)

#  Do 10 requests, waiting each time for a response
for request in range (1, 10):
    print "Sending request ", request, "..."
    socket.send("Hello from " + NAME)  # Can do only one request, then need to get a reply befor sending a new request
    # Get the reply.
    message = socket.recv()
    print "Received reply ", request, "[", message, "]"
