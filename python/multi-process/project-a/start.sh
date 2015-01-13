#!/bin/bash

echo "启动Project a"
cd `dirname $0`
python ./project.py a
sleep 1
./stat.sh
echo
echo
