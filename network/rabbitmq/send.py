#!/usr/bin/env python
import amqp

connection = amqp.connection.Connection(host='localhost')

channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(amqp.Message('Hello World!'), exchange='', routing_key='hello')
print " [x] Sent 'Hello World!'"
connection.close()
