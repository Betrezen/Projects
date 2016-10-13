#!/bin/bash
python -m cProfile -o output.pstats ./main.py arg1 arg2
./gprof2dot.py -f pstats output.pstats | dot -Tpng -o output.png