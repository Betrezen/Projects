from twisted.internet import defer
    
TARGET = 100000

def largeFibonnaciNumber():
    # create a Deferred object to return:
    d = defer.Deferred()

    # calculate the ten thousandth Fibonnaci number

    first = 0
    second = 1

    for i in xrange(TARGET - 1):
        new = first + second
        first = second
        second = new
        if i % 100 == 0:
            print "Progress: calculating the %dth Fibonnaci number" % i

    # give the Deferred the answer to pass to the callbacks:
    d.callback(second)

    # return the Deferred with the answer:
    return d

import time

timeBefore = time.time()

# call the function and get our Deferred
d = largeFibonnaciNumber()

timeAfter = time.time()

print "Total time taken for largeFibonnaciNumber call: %0.3f seconds" % (timeAfter - timeBefore)

# add a callback to it to print the number

def printNumber(number):
    print "The %dth Fibonacci number is %d" % (TARGET, number)

print "Adding the callback now."

d.addCallback(printNumber)