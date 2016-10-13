#!/usr/bin/env python
import amqp
import sys

connection = amqp.connection.Connection(host='localhost')
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(amqp.Message(message, delivery_mode=2),
				      exchange='',
                      routing_key='task_queue')
print " [x] Sent %r" % (message,)
connection.close()
