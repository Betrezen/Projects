#!/usr/bin/env python
import amqp
import uuid


class FibonacciRpcClient(object):

    def __init__(self):
        self.connection = amqp.connection.Connection(host='localhost')

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.queue

        self.channel.basic_consume(queue=self.callback_queue, no_ack=True, callback=self.on_response)

    def on_response(self, msg):
        if self.corr_id == msg.correlation_id:
            self.response = msg.body

    def call(self, n):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(amqp.Message(str(n),
                                                correlation_id=self.corr_id,
                                                reply_to=self.callback_queue),
                                   exchange='',
                                   routing_key='rpc_queue')
        while self.response is None:
            self.channel.wait()
        return int(self.response)

fibonacci_rpc = FibonacciRpcClient()

print " [x] Requesting fib(30)"
response = fibonacci_rpc.call(30)
print " [.] Got", response
