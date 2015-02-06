#!/usr/bin/env bash
########################################################################
#    File Name: base.sh
# 
#       Author: aceway
#         Mail: aceway@qq.com
# Created Time: Fri 01 Feb 2015 09:44:02
#  Description: 基础功能， 提供给具体实现功能的脚本调用，
#               调用方式: . the_path/base.sh 
#                      或 source the_path/base.sh
#
#               可以根据 sshpass安装、密钥安装情况进行选用
#
########################################################################

#
#定义控制输出终端颜色的代码
#

FG_RED="\033[1;31m"
FG_YELLOW="\033[1;33m"
FG_GREEN="\033[1;32m"
FG_BLUE="\033[0;34m"
FG_GRAY="\033[1;37m"
FG_LIGHT_RED="\033[0;31m"
FG_LIGHT_GREEN="\033[0;32m"
FG_LIGHT_BLUE="\033[0;34m"
FG_LIGHT_YELLOW="\033[0;33m"
FG_LIGHT_GRAY="\033[0;37m"
END="\033[0;00m"

#
#功能说明：
#   通过*密码*的方式使用 scp 或 rsync 将本地某个 目录/文件 复制到远程服务器上
#
#   scp 方式复制数据比较死板,不仅重复拷贝而且是全盘拷贝，会占用更多的带宽； 
#   rsync 可以指定忽略文件，并有对比避免重复传输, 但是 rsync 并非系统默认安装，需要手动安装; 本处 rsync 网络走ssh协议，端口
#   两种方式，都是对目标的覆盖，并未清除目标上原有文件数据， 虽然 rsync 可以自动做到，但此处未启用该功能
#
#参数说明：
#   $1 复制数据的命令， 只支持 scp 和 rsync 两种方式
#   $1 远程服务器的 ip或域名
#   $2 远程服务器的 端口
#   $3 远程服务器的 帐号
#   $4 远程服务器的 密码
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密钥 --- 存在远程服务器上的私钥文件
#
#   $9 要在目标服务器执行的命令
#
function dist_from_local_to_remote_with_pass() 
{
    if [ $# -eq 8 ] && [ "${1}" = "rsync" ];then
        rhost=$2
        rport=$3
        ruser=$4
        rpass=$5
        frm_local=$6
        to_remote=$7
        ex_list=$8
        echo
        sshpass -p${rpass} rsync -vr --exclude-from ${ex_list} --progress "-e ssh -p ${rport}" ${frm_local} ${ruser}@${rhost}:${to_remote}
        echo
    elif [ $# -eq 7 ] && [ "${1}" = "scp" ];then
        rhost=$2
        rport=$3
        ruser=$4
        rpass=$5
        frm_local=$6
        to_remote=$7
        echo
        sshpass -p${rpass} scp -vr -P${rport} ${frm_local} ${ruser}@${rhost}:${to_remote}
        echo
    else
        echo -e "${FG_RED}参数不对,${END}Usage:"
        echo -e "\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN} rsync rhost rport ruser rpass from_local to_remote exclude_list_file${END}"
        echo -e "\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN} scp rhost rport ruser rpass from_local to_remote ${END}"
        echo -e "\t ${FUNCNAME} ${@}"
        echo
    fi
}


#
#功能说明：
#   通过*密钥*的方式使用 scp 或 rsync 将本地某个 目录/文件 复制到远程服务器上
#
#   scp 方式复制数据比较死板,不仅重复拷贝而且是全盘拷贝，会占用更多的带宽； 
#   rsync 可以指定忽略文件，并有对比避免重复传输, 但是 rsync 并非系统默认安装，需要手动安装; 本处 rsync 网络走ssh协议，端口
#   两种方式，都是对目标的覆盖，并未清除目标上原有文件数据， 虽然 rsync 可以自动做到，但此处未启用该功能
#
#参数说明：
#   $1 复制数据的命令， 只支持 scp 和 rsync 两种方式
#   $1 远程服务器的 ip或域名
#   $2 远程服务器的 端口
#   $3 远程服务器的 帐号
#   $4 远程服务器的 密码
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密钥 --- 存在远程服务器上的私钥文件
#
#   $9 要在目标服务器执行的命令
#
function dist_from_local_to_remote_with_key() 
{
    if [ $# -eq 8 ] && [ "${1}" = "rsync" ];then
        rhost=$2
        rport=$3
        ruser=$4
        rkey=$5
        frm_local=$6
        to_remote=$7
        ex_list=$8
        echo
        rsync -vr --exclude-from ${ex_list} --progress "-e ssh -p ${rport} -i ${rkey} " ${frm_local} ${ruser}@${rhost}:${to_remote}
        echo
    elif [ $# -eq 7 ] && [ "${1}" = "scp" ];then
        rhost=$2
        rport=$3
        ruser=$4
        rkey=$5
        frm_local=$6
        to_remote=$7
        echo
        scp -vr -i${rkey} -p${rport} ${frm_local} ${ruser}@${rhost}:${to_remote}
        echo
    else
        echo -e "${FG_RED}参数不对,${END}Usage:"
        echo -e "\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN} rsync rhost rport ruser rkey from_local to_remote exclude_list_file${END}"
        echo -e "\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN} scp rhost rport ruser rkey from_local to_remote${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}


##############################################################################################################

#
#功能说明：
#   通过*密码*的方式自动登录中心服务器，再通过*密码*的方式自动跳转目标服务器， 然后执行 指定命令
#
#   只直接支持一跳
#   本函数需要本地和中心服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 中心服务器的 ip或域名
#   $2 中心服务器的 端口
#   $3 中心服务器的 帐号
#   $4 中心服务器的 密码
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密码
#
#   $9 要在目标服务器执行的命令
#
function exec_on_dest_svr_from_center_svr_with_passwd() 
{
    if [ $# -eq 9 ];then
        chost=$1
        cport=$2
        cuser=$3
        cpass=$4

        dhost=$5
        dport=$6
        duser=$7
        dpass=$8

        dcmd=$9

        lcmd="sshpass -p${cpass} ssh -p${cport} ${cuser}@${chost} sshpass -p ${dpass} ssh -p${dport} ${duser}@${dhost} ${dcmd}"
        echo
        ${lcmd}
        echo
    else
        echo -e "${FG_RED}参数不对,${END}Usage\n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}chost cport cuser cpass dhost dport duser dpass dcmd${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}

#
#功能说明：
#   通过*密钥*的方式自动登录中心服务器，再通过*密钥*的方式自动跳转目标服务器， 然后执行 指定命令
#
#   只直接支持一跳
#
#参数说明：
#   $1 中心服务器的 ip或域名
#   $2 中心服务器的 端口
#   $3 中心服务器的 帐号
#   $4 中心服务器的 密钥 --- 存在本地服务器上的私钥文件
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密钥 --- 存在中心服务器上的私钥文件
#
#   $9 要在目标服务器执行的命令
#
function exec_on_dest_svr_from_center_svr_with_key() 
{
    if [ $# -eq 9 ];then
        chost=$1
        cport=$2
        cuser=$3
        rkey=$4

        dhost=$5
        dport=$6
        duser=$7
        dkey=$8

        dcmd=$9

        lcmd="ssh -i ${rkey} -p${cport} ${cuser}@${chost} ssh -i ${dkey} -p${dport} ${duser}@${dhost} ${dcmd}"
        echo
        ${lcmd}
        echo
    else
        echo -e "${FG_RED}参数不对,${END}Usage:\n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}chost cport cuser rkey dhost dport duser rkey dcmd${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}

#
#功能说明：
#   通过*密钥*的方式自动登录中心服务器，再通过*密码*的方式自动跳转目标服务器， 然后执行 指定命令
#
#   只直接支持一跳
#   本函数需要中心服务器安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 中心服务器的 ip或域名
#   $2 中心服务器的 端口
#   $3 中心服务器的 帐号
#   $4 中心服务器的 密钥 --- 存在本地服务器上的私钥文件
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密码
#
#   $9 要在目标服务器执行的命令
#
function exec_on_dest_svr_from_center_svr_with_key_passwd() 
{
    if [ $# -eq 9 ];then
        chost=$1
        cport=$2
        cuser=$3
        rkey=$4

        dhost=$5
        dport=$6
        duser=$7
        dpass=$8

        dcmd=$9

        lcmd="ssh -i ${rkey} -p${cport} ${cuser}@${chost} sshpass -p ${dpass} ssh -p${dport} ${duser}@${dhost} ${dcmd}"
        echo
        ${lcmd}
        echo
    else
        echo -e "${FG_RED}参数不对:${END}:Usage\n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}chost cport cuser rkey dhost dport duser dpass dcmd${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}

#
#功能说明：
#   通过*密码*的方式自动登录中心服务器，再通过*密钥*的方式自动跳转目标服务器， 然后执行 指定命令
#
#   只直接支持一跳
#   本函数需要本地服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 中心服务器的 ip或域名
#   $2 中心服务器的 端口
#   $3 中心服务器的 帐号
#   $4 中心服务器的 密码
#
#   $5 目标服务器的 ip或域名 
#   $6 目标服务器的 端口
#   $7 目标服务器的 帐号
#   $8 目标服务器的 密钥 --- 存在中心服务器上的私钥文件
#
#   $9 要在目标服务器执行的命令
#
function exec_on_dest_svr_from_center_svr_with_passwd_key() 
{
    if [ $# -eq 9 ];then
        chost=$1
        cport=$2
        cuser=$3
        cpass=$4

        dhost=$5
        dport=$6
        duser=$7
        dkey=$8

        dcmd=$9

        lcmd="sshpass -p ${cpass} ssh -p${cport} ${cuser}@${chost} ssh -i ${dkey} -p${dport} ${duser}@${dhost} ${dcmd}"
        echo
        ${lcmd}
        echo
    else
        echo -e "${FG_RED}参数不对${END},Usage\n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}chost cport cuser cpass dhost dport duser dkey dcmd${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}


##############################################################################################################
##############################################################################################################

#
#功能说明：
#   通过*密码*的方式自动登录中心服务器，再用*密码*的方式通过 scp 或 rsync 将中心服务器上发文件分发到目标服务器
#
#   只直接支持一跳
#   本函数需要本地和中心服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 在目标服务器执行的复制命令, 支持 scp 和 rsync
#   $2 中心服务器的 ip或域名
#   $3 中心服务器的 端口
#   $4 中心服务器的 帐号
#   $5 中心服务器的 密码
#   $6 中心服务器上被复制的数据, 目录或文件
#
#   $7 目标服务器的 ip或域名 
#   $8 目标服务器的 端口
#   $9 目标服务器的 帐号
#   $10 目标服务器的 密码
#   $11 数据被复制到目标服务器的存在的位置
#
#
function dist_on_center_svr_to_dest_svr_with_passwd() 
{
    if [ $# -eq 11 ];then
        cpcmd=$1
        chost=$2
        cport=$3
        cuser=$4
        cpass=$5
        cdata=$6

        dhost=$7
        dport=$8
        duser=$9
        dpass=${10}
        ddata=${11}

        if [ "${cpcmd}" = "scp" ];then
            sshpass -p${cpass} ssh -p${cport} ${cuser}@${chost} sshpass -p${dpass} ${cpcmd} -vr -P${dport} ${cdata} ${duser}@${dhost}:${ddata}
        elif [ "${cpcmd}" = "rsync" ];then
            sshpass -p${cpass} ssh -p${cport} ${cuser}@${chost} sshpass -p${dpass} ${cpcmd} -vr --progress '-e ssh -p ${dport}' ${cdata} ${duser}@${dhost}:${ddata}
        else
            echo -e "\t ${FUNCNAME} 不支持 ${cpcmd}"
        fi
    else
        echo -e "${FG_RED}参数不对,${END}Usage: \n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}cpcmd chost cport cuser cpass cdata dhost dport duser dpass ddata${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}


##############################################################################################################
#
#功能说明：
#   通过*密钥*的方式自动登录中心服务器，再用*密钥*的方式通过 scp 或 rsync 将中心服务器上发文件分发到目标服务器
#
#   只直接支持一跳
#   本函数需要本地和中心服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 在目标服务器执行的复制命令, 支持 scp 和 rsync
#   $2 中心服务器的 ip或域名
#   $3 中心服务器的 端口
#   $4 中心服务器的 帐号
#   $5 中心服务器的 密钥 --- 存储在本地服务器上的密钥文件
#   $6 中心服务器上被复制的数据, 目录或文件
#
#   $7 目标服务器的 ip或域名 
#   $8 目标服务器的 端口
#   $9 目标服务器的 帐号
#   $10 目标服务器的 密钥 --- 存储在中心服务器上的密钥文件
#   $11 数据被复制到目标服务器的存在的位置
#
#
function dist_on_center_svr_to_dest_svr_with_key() 
{
    if [ $# -eq 11 ];then
        cpcmd=$1
        chost=$2
        cport=$3
        cuser=$4
        ckey=$5
        cdata=$6

        dhost=$7
        dport=$8
        duser=$9
        dkey=${10}
        ddata=${11}

        if [ "${cpcmd}" = "scp" ];then
            ssh -p${cport} -i${ckey} ${cuser}@${chost} ${cpcmd} -vr -i${dkey} -P${dport} ${cdata} ${duser}@${dhost}:${ddata}
        elif [ "${cpcmd}" = "rsync" ];then
            ssh -p${cport} -i${ckey} ${cuser}@${chost} ${cpcmd} -vr --progress '-e ssh -p ${dport} -i ${dkey}' ${cdata} ${duser}@${dhost}:${ddata}
        else
            echo -e "\t ${FUNCNAME} 不支持 ${cpcmd}"
        fi
    else
        echo -e "${FG_RED}参数不对,${END}Usage: \n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}cpcmd chost cport cuser ckey cdata dhost dport duser dkey ddata${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}

##############################################################################################################
##############################################################################################################

#
#功能说明：
#   通过*密码*的方式自动登录中心服务器，再用*密钥*的方式通过 scp 或 rsync 将中心服务器上发文件分发到目标服务器
#
#   只直接支持一跳
#   本函数需要本地和中心服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 在目标服务器执行的复制命令, 支持 scp 和 rsync
#   $2 中心服务器的 ip或域名
#   $3 中心服务器的 端口
#   $4 中心服务器的 帐号
#   $5 中心服务器的 密码
#   $6 中心服务器上被复制的数据, 目录或文件
#
#   $7 目标服务器的 ip或域名 
#   $8 目标服务器的 端口
#   $9 目标服务器的 帐号
#   $10 目标服务器的 密钥 --- 存储在中心服务器上的密钥文件
#   $11 数据被复制到目标服务器的存在的位置
#
#
function dist_on_center_svr_to_dest_svr_with_passwd_key() 
{
    if [ $# -eq 11 ];then
        cpcmd=$1
        chost=$2
        cport=$3
        cuser=$4
        cpass=$5
        cdata=$6

        dhost=$7
        dport=$8
        duser=$9
        dkey=${10}
        ddata=${11}

        if [ "${cpcmd}" = "scp" ];then
            sshpass -p${cpass} ssh -p${cport} ${cuser}@${chost} ${cpcmd} -i ${dkey} -vr -P${dport} ${cdata} ${duser}@${dhost}:${ddata}
        elif [ "${cpcmd}" = "rsync" ];then
            sshpass -p${cpass} ssh -p${cport} ${cuser}@${chost} ${cpcmd} -vr --progress '-e ssh -p ${dport} -i ${dkey}' ${cdata} ${duser}@${dhost}:${ddata}
        else
            echo -e "\t ${FUNCNAME} 不支持 ${cpcmd}"
        fi
    else
        echo -e "${FG_RED}参数不对,${END}Usage: \n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}cpcmd chost cport cuser cpass cdata dhost dport duser dkey ddata${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}


##############################################################################################################
#
#功能说明：
#   通过*密钥*的方式自动登录中心服务器，再用*密码*的方式通过 scp 或 rsync 将中心服务器上发文件分发到目标服务器
#
#   只直接支持一跳
#   本函数需要本地和中心服务器都安装 sshpass --- 代替手工输入密码
#
#参数说明：
#   $1 在目标服务器执行的复制命令, 支持 scp 和 rsync
#   $2 中心服务器的 ip或域名
#   $3 中心服务器的 端口
#   $4 中心服务器的 帐号
#   $5 中心服务器的 密钥 --- 存储在本地服务器上的密钥文件
#   $6 中心服务器上被复制的数据, 目录或文件
#
#   $7 目标服务器的 ip或域名 
#   $8 目标服务器的 端口
#   $9 目标服务器的 帐号
#   $10 目标服务器的 密码
#   $11 数据被复制到目标服务器的存在的位置
#
#
function dist_on_center_svr_to_dest_svr_with_key_passwd() 
{
    if [ $# -eq 11 ];then
        cpcmd=$1
        chost=$2
        cport=$3
        cuser=$4
        ckey=$5
        cdata=$6

        dhost=$7
        dport=$8
        duser=$9
        dpass=${10}
        ddata=${11}

        if [ "${cpcmd}" = "scp" ];then
            ssh -p${cport} -i${ckey} ${cuser}@${chost} sshpass -p${dpass} ${cpcmd} -vr -i${dkey} -P${dport} ${cdata} ${duser}@${dhost}:${ddata}
        elif [ "${cpcmd}" = "rsync" ];then
            ssh -p${cport} -i${ckey} ${cuser}@${chost} sshpass -p${dpass} ${cpcmd} -vr --progress '-e ssh -p ${dport}' ${cdata} ${duser}@${dhost}:${ddata}
        else
            echo -e "\t ${FUNCNAME} 不支持 ${cpcmd}"
        fi
    else
        echo -e "${FG_RED}参数不对,${END}Usage: \n\t${FG_YELLOW} ${FUNCNAME} ${FG_GREEN}cpcmd chost cport cuser ckey cdata dhost dport duser dpass ddata${END}"
        echo -e "\t ${FUNCNAME} $@"
        echo
        echo
    fi
}
