from libc.stdlib cimport system as c_system
from libmy cimport my_method


class SpamError(Exception):
    pass


def system(char* command):

    cdef int status_code
    status_code = c_system(command)

    if status_code < 0:
        raise SpamError("System command failed")

    return status_code


def libmy_my_method(int a, int b):
    return my_method(a, b)
