#!/usr/bin/env python
import time
import random

import amqp

NAME = 'Worker ' + str(random.randrange(1, 1000, 1))

connection = amqp.connection.Connection(host='localhost')
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print ' [*]',NAME, 'Waiting for messages. To exit press CTRL+C'

def callback(msg):
    print " [x]", NAME, "Received %r" % (msg.body,)
    time.sleep(msg.body.count('.'))
    print " [x] Done"
    channel.basic_ack(delivery_tag=msg.delivery_tag)

channel.basic_qos(prefetch_size=0, prefetch_count=1, a_global=False)
channel.basic_consume(queue='task_queue', callback=callback)

while True:
    try:
        channel.wait()
    except KeyboardInterrupt:
        connection.close()
        break
