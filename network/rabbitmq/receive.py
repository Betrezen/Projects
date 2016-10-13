#!/usr/bin/env python
import amqp

connection = amqp.connection.Connection(host='localhost')
channel = connection.channel()

channel.queue_declare(queue='hello')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(msg):
    print " [x] Received %r" % (msg.body,)

channel.basic_consume(queue='hello', no_ack=True, callback=callback)

channel.wait()  # wait for one message
connection.close()
