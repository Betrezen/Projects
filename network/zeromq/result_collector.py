import time
import zmq
import pprint


def result_collector():
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://127.0.0.1:5558")
    while True:
        collecter_data = {}
        for x in xrange(5000):
            result = results_receiver.recv_json()
            if collecter_data.has_key(result['consumer']):
                collecter_data[result['consumer']] = collecter_data[result['consumer']] + 1
            else:
                collecter_data[result['consumer']] = 1
        pprint.pprint(collecter_data)  # print results


result_collector()
