#!/usr/bin/env python
import random

import amqp


NAME = 'Logger ' + str(random.randrange(1, 1000, 1))

connection = amqp.connection.Connection(host='localhost')
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print ' [*] Waiting for logs. To exit press CTRL+C'

def callback(msg):
    print " [x]", NAME, "%r" % (msg.body,)

channel.basic_consume(queue_name, no_ack=True, callback=callback)

while True:
    try:
        channel.wait()
    except KeyboardInterrupt:
        connection.close()
        break
