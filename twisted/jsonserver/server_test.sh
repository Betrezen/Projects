#!/bin/bash
date
for i in {1..20}
do
  python jsonclient.py&
done
date
exit 0
