#!/bin/bash
rm -rf build/
python setup.py build
mv build/lib.linux-x86_64-2.7/spam.so ./
