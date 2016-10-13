#!/usr/bin/env python
import amqp

connection = amqp.connection.Connection(host='localhost')

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

def on_request(msg):
    n = int(msg.body)

    print " [.] fib(%s)"  % (n,)
    response = fib(n)

    channel.basic_publish(amqp.Message(str(response), correlation_id=msg.correlation_id),
                          exchange='',
                          routing_key=msg.reply_to)
    channel.basic_ack(delivery_tag=msg.delivery_tag)

channel.basic_qos(prefetch_size=0, prefetch_count=1, a_global=False)
channel.basic_consume(queue='rpc_queue', callback=on_request)

print " [x] Awaiting RPC requests"

while True:
    try:
        channel.wait()
    except KeyboardInterrupt:
        connection.close()
        break
