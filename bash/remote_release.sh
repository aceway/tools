#!/usr/bin/env bash

RED="\033[0;31m"
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[0;33m"
GRAY="\033[0;37m"
LIGHT_RED="\033[1;31m"
LIGHT_YELLOW="\033[1;33m"
LIGHT_GREEN="\033[1;32m"
LIGHT_BLUE="\033[0;34m"
LIGHT_GRAY="\033[1;37m"
END="\033[0;00m"

dt=`date +"%Y %m %d %H %M %S"`
array=($dt)
year=${array[0]}
month=${array[1]}
day=${array[2]}
hour=${array[3]}
minute=${array[4]}
second=${array[5]}

#线上入口服务器用 key 避免交互输入密码
function rsync_for_release() 
{
    echo
    project_name="project_app"
    frm_local=$1
    to_remote=$2
    user=$3
    host=$4
    port=$5
    #key="${HOME}/.ssh/project_app"
    ex_list=$6
    echo -e ${YELLOW}"rsync local ${project_name} to ${RED}${host}${END}:"
    echo -e "\tFROM LOCAL DIR:${frm_local}"
    echo -e "\tTO  REMOTE DIR:${to_remote}"
    cmd="rsync"
    ${cmd} -vr --exclude-from ${ex_list} --progress "-e ssh -p ${port}" ${frm_local} ${user}@${host}:${to_remote}
    #${cmd} -vr --exclude-from ${ex_list} --progress "-e ssh -p ${port} -i ${key} " ${frm_local} ${user}@${host}:${to_remote}
}

##线上服务器内部用 sshpass 解决交互的输入密码， 后继可以考虑用 key 的方式， 并远程自动重启服务
function remote_stop() 
{
    echo
    remote_host="$1"
    remote_path="$2"
    server_ip="$3"
    pname="$4"
    remote_file="${remote_path}/${pname}/bin/lib*.so"
    rpasswd="xxxxxxx"

    user="username"
    passwd="xxxxxxx"
    port="22"
    #key="${HOME}/.ssh/project_app"
    echo -e "IN REMOTE ${remote_host} ${RED} STOP ${YELLOW}${pname}${END} ${RED}${server_ip}${END}:"

    stop_it="~/project_app/${pname}/stop"
    echo -e "${RED}stop${YELLOW} ${pname}${END}"
    #cmd="ssh -p${port} -i ${key} ${user}@${remote_host} sshpass -p ${passwd} ssh ${user}@${server_ip} ${stop_it}"
    cmd="sshpass -p ${rpasswd} ssh -p${port} ${user}@${remote_host} sshpass -p ${passwd} ssh -p${port} ${user}@${server_ip} ${stop_it}"
    ${cmd}
}
##线上服务器内部用 sshpass 解决交互的输入密码， 后继可以考虑用 key 的方式， 并远程自动重启服务
function remote_distribute() 
{
    echo
    remote_host="$1"
    remote_path="$2"
    server_ip="$3"
    pname="$4"
    remote_file="${remote_path}/${pname}/bin/lib*.so"
    dist_path="~/project_app/${pname}/bin/"
    rpasswd="shootao123"

    user="username"
    passwd="xxxxxxx"
    port="22"
    #key="${HOME}/.ssh/project_app"
    echo -e "IN REMOTE ${remote_host} DISTRIBUTE ${YELLOW}${pname}${END} to ${RED}${server_ip} ${dist_path}${END}:"

    #cmd="ssh -p${port} -i ${key} ${user}@${remote_host} sshpass -p ${passwd} scp ${remote_file} ${user}@${server_ip}:${dist_path}"
    cmd="sshpass -p ${rpasswd} ssh -p${port} ${user}@${remote_host} sshpass -p ${passwd} scp -P${port} ${remote_file} ${user}@${server_ip}:${dist_path}"
    ${cmd}


    if [ "${pname}" = "online" ];then
        remote_file="${remote_path}/${pname}/bin/conf/*"
        dist_path="~/project_app/${pname}/bin/conf/"

        user="username"
        passwd="xxxxxxx"
        port="22"
        #key="${HOME}/.ssh/project_app"
        echo -e "IN REMOTE ${remote_host} DISTRIBUTE ${YELLOW}${pname}${END} to ${RED}${server_ip} ${dist_path}${END}:"

        #cmd="ssh -p${port} -i ${key} ${user}@${remote_host} sshpass -p ${passwd} scp -r ${remote_file} ${user}@${server_ip}:${dist_path}"
        cmd="sshpass -p ${rpasswd} ssh -p${port} ${user}@${remote_host} sshpass -p ${passwd} scp -P${port} -r ${remote_file} ${user}@${server_ip}:${dist_path}"
        ${cmd}
    fi
    sleep 1

}
##线上服务器内部用 sshpass 解决交互的输入密码， 后继可以考虑用 key 的方式， 并远程自动重启服务
function remote_start() 
{
    echo
    remote_host="$1"
    remote_path="$2"
    server_ip="$3"
    pname="$4"
    rpasswd="shootao123"
    remote_file="${remote_path}/${pname}/bin/lib*.so"

    user="username"
    passwd="xxxxxxx"
    port="22"
    #key="${HOME}/.ssh/project_app"
    echo -e "IN REMOTE ${remote_host} ${RED} START ${YELLOW}${pname}${END} ${RED}${server_ip}${END}:"

    start_it="~/project_app/${pname}/startup"
    #cmd="ssh -p${port} -i ${key} ${user}@${remote_host} sshpass -p ${passwd} ssh ${user}@${server_ip} ${start_it} "
    cmd="sshpass -p ${rpasswd} ssh -p${port} ${user}@${remote_host} sshpass -p ${passwd} ssh -p${port} ${user}@${server_ip} ${start_it} "
    ${cmd}
    sleep 1
    echo -e "${GREEN}FINISH ${pname}${END}"
}


THE_PATH=`dirname $0`
cd ${THE_PATH}

cd "./project_app/online/bin/"
./update.conf
cd ../../../

#
#注意下面三个路径，local_path 末尾的 / 不可少和 remote_path 末尾的 / 不可有, remote_path 使用绝对路径
#
local_path="./project_app/"
exc_list_file="./exclude.list"

remote_path="/home/username/release-center/project_app/${year}-${month}-${day}-${hour}"
rhost="10.1.1.237"
rport=22
ruser="username"
if [ ! -f ${exc_list_file} ]; then
    touch ${exc_list_file}
fi

# 发布本地程序到 中心服务器上 --- 发布 project_app 目录下的 文件， 要忽略文件在 exclude.list 中添加
rsync_for_release $local_path $remote_path $ruser $rhost $rport $exc_list_file 


#从远程的中心服务器， 停止各个 业务服务器上的程序
pname="app_1"
ip="127.0.0.1"
remote_stop ${rhost} ${remote_path} ${ip} ${pname}

pname="app_2"
ip="127.0.0.1"
remote_stop ${rhost} ${remote_path} ${ip} ${pname}

pname="app_3"
ip="127.0.0.1"
remote_stop ${rhost} ${remote_path} ${ip} ${pname}

pname="app_4"
ip="127.0.0.1"
remote_stop ${rhost} ${remote_path} ${ip} ${pname}

pname="app_5"
ip="127.0.0.1"
remote_stop ${rhost} ${remote_path} ${ip} ${pname}

pname="app_6"
ip="127.0.0.1"
#remote_stop ${rhost} ${remote_path} ${ip} ${pname}


#从远程的中心服务器， 分发程序到各个 业务服务器上  --- 只更新 so 文件
pname="app_1"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}

pname="app_2"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}

pname="app_3"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}

pname="app_4"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}

pname="app_5"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}

pname="app_6"
ip="127.0.0.1"
remote_distribute ${rhost} ${remote_path} ${ip} ${pname}


#从远程的中心服务器， 启动各个 业务服务器上的程序
pname="app_6"
ip="127.0.0.1"
#remote_start ${rhost} ${remote_path} ${ip} ${pname}

pname="app_5"
ip="127.0.0.1"
remote_start ${rhost} ${remote_path} ${ip} ${pname}

pname="app_4"
ip="127.0.0.1"
remote_start ${rhost} ${remote_path} ${ip} ${pname}

pname="app_3"
ip="127.0.0.1"
remote_start ${rhost} ${remote_path} ${ip} ${pname}

pname="app_2"
ip="127.0.0.1"
remote_start ${rhost} ${remote_path} ${ip} ${pname}

pname="app_1"
ip="127.0.0.1"
remote_start ${rhost} ${remote_path} ${ip} ${pname}
