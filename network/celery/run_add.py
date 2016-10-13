from celery import group, chain, chord

from add_task import add, mul, xsum, broken_task, on_task_error, print_task, on_task_success


result = add.delay(1, 1)  # async call, equivalent to add.apply_async((1, 1))
print result.state
print result.get(timeout=3)  # wait for result and print it
print result.state

print add(1, 1)  # synchronous call, without worker

print group(add.s(i, i) for i in xrange(10))().get()  # run group of tasks

print chain(add.s(4, 4) | mul.s(8))().get()  # result of first task used as argument for next

print chord(group(add.s(i, i) for i in xrange(10)), xsum.s())().get()  # resoult of group will be passed to xsum

broken_task.apply_async(link_error=on_task_error.s('broken_task'))

print_task.apply_async(('something', ), link=on_task_success.s('print_task'))
