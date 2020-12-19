#!/usr/bin/env bash

if [ $# != 2 ] ; then
  echo "please input TaskName and logName!!!"
  exit 1;
fi

task=$1
out=$2
echo "start to start task: $task ..."
nohup venv/bin/python3 main.py $task -e pro -l > run/$out.log 2>&1 &
echo $! 1> pid/$out.pid