#!/usr/bin/env python
import amqp
import sys

connection = amqp.connection.Connection(host='localhost')
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

message = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(amqp.Message(message),
					  exchange='logs',
                      routing_key='')
print " [x] Sent %r" % (message,)
connection.close()
