#!/bin/bash
gcc -shared -o spam.so -fPIC spammodule.c -I/usr/include/python2.7/
