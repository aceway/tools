#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: framework.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 16时38分02秒
#########################################################
import os, sys, time
import settings as st
import business_worker as bw
import dispath_worker as dw

def fork_work_process(proc_cnt=10, pid_list=None, root_path=None):
    if pid_list is None: pid_list=[]
    if proc_cnt > 0:
        proc_cnt = proc_cnt - 1
        try:
            pid = os.fork()
            if pid == 0: 
                bw.do_business(work_idx=proc_cnt, root_path=root_path)
                sys.exit(0)
            elif pid > 0:
                pid_list.append(pid)
                fork_work_process(proc_cnt, pid_list, root_path=root_path)
            else:
                pass
        except OSError, e:
            print >>sys.stderr,"Fork business_work proccess failed:%d(%s)" %(e.errno,e.strerror) 
            sys.exit(1)
    else:
        time.sleep(1)
        dw.do_dispath(work_list=pid_list, root_path=root_path)

def run(root_path=None):
    print "Work process count: ", st.work_proc_cnt
    work_ids=[]
    fork_work_process(st.work_proc_cnt, work_ids, root_path=root_path)
