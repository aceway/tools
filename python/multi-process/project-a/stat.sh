#!/bin/bash
THE_PATH=`dirname $0`
cd ${THE_PATH}

echo "Project a进程" 
for pid_info in `grep [1-9] *.pid`; do
    fl=`echo "${pid_info}"|cut -f 1 -d ':'` 
    pid=`echo "${pid_info}"|cut -f 2 -d ':'` 
    if [ -z "$pid" ];then
        echo
    else
        echo "Project a进程" $pid "及其子进程:"
        ps -eF|grep ${pid}|grep -v "grep"
    fi
    echo
done 
echo
echo
