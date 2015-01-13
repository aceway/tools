#!/usr/bin/env python
# -*- coding:utf-8 -*-
########################################################################
#    File Name: worker.py
# 
#         Mail: aceway@qq.com
# Created Time: 2014年11月25日 星期二 10时31分26秒
#  Description: 
#               
########################################################################
import settings as st
from settings import mongo_cfg as mocfg

import os, sys#, time#
import math
import logging
from multiprocessing import cpu_count #Pool

import business_worker as bw
import dispath_worker as dw

try:
    import pymongo as pdb
except:
    print st.color["FG_RED"], u"未找到python的mongodb模块，你可以：\n\tsudo apt-get install python-pymongo\n或者:\n\tsudo pip install pymongo", st.color["END"]


def fork_work_process(work_full_path=None, proc_cnt=10, task_list=None, pid_dict=None):
    """
    递归调用fork出工作进程, 依次从 task_list中取出任务执行
    """
    lg = logging.getLogger('fork_work_process')
    if pid_dict is None: pid_dict={}
    if proc_cnt > 0 and isinstance(task_list, list) and len(task_list) > 0 :
        proc_cnt = proc_cnt - 1
        try:
            pid = os.fork()
            if pid == 0:    #子进程, 开始执行任务
                bw.do_business(work_idx=proc_cnt, work_full_path=work_full_path, task=task_list[proc_cnt-1], log_level=st.log_level)
                sys.exit(0)
            elif pid > 0:   #父进程继续 fork 子进程
                pid_dict[pid] =task_list[proc_cnt-1]
                fork_work_process(work_full_path=work_full_path, proc_cnt=proc_cnt, task_list=task_list, pid_dict=pid_dict)
            else:
                pass
        except OSError, e:
            lg.critical("Fork business_work proccess failed, errorno:{0} - str:{1}".format(e.errno,e.strerror)) 
            sys.exit(1)
    else:
        pass #time.sleep(1)


def cacl_task_list(meta_data_list):
    """
    根据元数据格式计算需要多少个进程执行任务(依赖当前机器CPU个数)
    """
    #lg = logging.getLogger('cacl_task_list')
    if isinstance(meta_data_list, list) and len (meta_data_list) > 0:
        print "meta data list:", meta_data_list
        meta_cnt = len(meta_data_list)
        cpu_cnt  = cpu_count()
        #lg.info( "CPU COUNT:{cc}, META DATA COUNT:{zc}".format(cc= cpu_cnt, zc=meta_cnt) )
        print  "CPU COUNT:{cc}, META DATA COUNT:{zc}".format(cc= cpu_cnt, zc=meta_cnt) 
        
        if isinstance(st.work_proc_cnt, int) and st.work_proc_cnt > 0:
            proc_cnt = st.work_proc_cnt
        else:
            if cpu_cnt > meta_cnt:
                proc_cnt = meta_cnt
            else:
                proc_cnt = int(min(4, meta_cnt/cpu_cnt)) #避免进程过多，进程本身消耗系统资源
        if proc_cnt > meta_cnt: proc_cnt = meta_cnt
        group_meta_list = split_task_for_process_groups(task_list = meta_data_list, group_cnt = proc_cnt)
        #lg.info("PROC COUNT:{pc}".format(pc = proc_cnt))
        print "PROC COUNT:{pc}".format(pc = proc_cnt)
        return proc_cnt, group_meta_list
    else:
        #lg.warning("NO META DATA TO PROCESS, NO WORK, OVER.")
        print st.color["FG_YELLOW"], "NO META DATA TO PROCESS, NO WORK, OVER.", st.color['END']
        return None, None

def split_task_for_process_groups(task_list=None, group_cnt=1):
    """
    根据CPU个数， 计算需要多少个进程
    """
    work_list_group = []
    ln = len(task_list)
    group_cnt = max(1, group_cnt)  #最少1个组
    sub_len   = max(1, int(math.floor(float(ln)/group_cnt)))  #每组最少一个任务
    for idx in range(group_cnt):
        l = task_list[ idx * sub_len : (idx+1) * sub_len ]
        work_list_group.append(l)
    if (idx+1)*sub_len < ln:     #将余下的任务分别不给各个进程
        for i in range((idx+1)*sub_len, ln):
            work_list_group[(idx+1)*sub_len - i].append(task_list[i])
    return work_list_group

def query_table_metas(mongo_db, collection, key):
    """
    从数据库中查询元数据， 用于后面根据元数据分配工作进程
    """
    try:
        if isinstance(collection, basestring) and collection.startswith('t_') :
            metas = mongo_db[collection].distinct( key )
            return metas
        else:
            return []
    except Exception as e:
        print "\n", st.color["FG_RED"], "异常: ", e, st.color["END"], "\n\n"
        return []

def do_work(work_full_path):
    """
    1,从数据库中查询出元数据数量， 用于后面根据数量分配工作进程
    2,根据元数据数量， 机器CPU数，计算工作进程数；
    3,创建工作进程之 计算子进程；同时一个监控进程用于分配下次任务
    """
    mongo_con = None
    log_dir = work_full_path + "log/"
    if not os.path.isdir(log_dir): os.makedirs(log_dir)

    try:

        mongo_con = pdb.Connection(mocfg['host'], mocfg['port'])
        mongo_con[mocfg['auth_db']].authenticate(mocfg['user'], mocfg['passwd'])
        mongo_db  = mongo_con[mocfg['db']]
        
        meta_data_list = query_table_metas(mongo_db, 't_meta_table', 'meta_id')

        mongo_con.close()
        mongo_con = None

        proc_cnt, work_group_list = cacl_task_list(meta_data_list)
        if isinstance(proc_cnt, int) and isinstance(work_group_list, list):
            work_dict = {}
            fork_work_process(work_full_path=work_full_path, proc_cnt=proc_cnt, task_list=work_group_list, pid_dict=work_dict)
            dw.do_dispath(work_full_path=work_full_path, work_dict=work_dict, log_level=st.log_level)
            lg = logging.getLogger('do_work')
            lg.setLevel(st.log_level)
            lg.info("DISPATH WORK OVER PID:{pid}".format(pid=os.getpid()))
        else:
            print st.color['FG_RED'], "Proc count:{pc}, work group list:{wgl}".format(pc=proc_cnt, wgl=work_group_list), st.color['END']
            print st.color['FG_RED'], "SOMTHING WRONG, OVER!", st.color['END']
    #except Exception as e:
    except IOError as e:
        if mongo_con : 
            mongo_con.close()
            mongo_con = None
        lg.error( "[{pid}]异常: {e}".format(pid=os.getpid(), e=e) )
    return True

if __name__ == "__main__":
    import sys
    if len ( sys.argv ) == 1 :
        do_work( os.path.dirname(__file__) )
    elif len ( sys.argv ) == 2 :
        do_work( sys.argv[1] )
    else:
        print "Usage:\n     ", st.color["FG_RED"], sys.argv[0], "[work_path]", st.color["END"]
