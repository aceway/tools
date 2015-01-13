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

DIR_NOW=`pwd`
DIR_PROTO="$DIR_NOW/proto/proto_files"
DIR_DB="$DIR_NOW/db_mongo"
DIR_GATE="$DIR_NOW/gateway"
DIR_LOGIN="$DIR_NOW/login"
DIR_NICK="$DIR_NOW/nick"
DIR_ONLINE="$DIR_NOW/online"
DIR_SWITCH="$DIR_NOW/switch"

if [ -d ./.svn ];then
    #
    #从服务器获取svn版本信息
    #
    grep_str="最后修改的版本"
    revision=`svn info |grep "${grep_str}" |awk '{print $2}'`  
    if [ -z ${revision} ];then
        grep_str="Last Changed Rev"
        revision=`svn info |grep "${grep_str}" |awk '{print $4}'`  
    fi
    
    URL=`svn info |grep "URL:" |awk '{print $2}'`  
    grep_str="最后修改的版本"
    svnRevision=`svn info $URL |grep "${grep_str}" |awk '{print $2}'`  
    if [ -z ${svnRevision} ];then
        grep_str="Last Changed Rev"
        svnRevision=`svn info |grep "${grep_str}" |awk '{print $4}'`  
    fi
    
    #
    echo -e "服务器地址:" ${URL}  
    echo -e "本地  版本:" ${YELLOW} ${revision} ${END}
    echo -e "服务器版本:" ${RED} ${svnRevision} ${END}
    echo
    if [[ ${revision} < ${svnRevision} ]] ; then  
        echo -e ${YELLOW} "需要从svn服务器更新"  ${END}
    else  
        echo -e ${GREEN} "不需要svn从服务器更新"  ${END}
    fi 
else
    echo -e ${RED} "当前目录不是svn目录"  ${END}
fi
