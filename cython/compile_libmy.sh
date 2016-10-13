#!/bin/bash
gcc -shared -o libmy.so -fPIC libmy.c
sudo cp libmy.so /usr/lib/
