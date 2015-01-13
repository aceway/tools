#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: business_worker.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月13日 星期四 17时17分29秒
#########################################################
import os
import signal
import datetime
import time
import logging
import logging.handlers
import settings as st
from settings import mongo_cfg as mocfg

import pymongo as pdb
from project_calculator import project_calculator


def init_business_root_log(log_full_path=None, filename=__name__, level="INFO", max_bytes=1024*1024*50, backup_count=20):
    log_full_filename = "{p}/{f}.log".format(p=log_full_path, f=filename)
    root_log = logging.getLogger()
    root_log.propagate = False
    root_log.setLevel(level)

    handler = logging.handlers.RotatingFileHandler(log_full_filename, maxBytes=max_bytes, backupCount=backup_count)
    handler.propagate = False
    handler.setLevel(level)

    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(name)s]:%(message)s')
    handler.setFormatter(formatter)
    root_log.addHandler(handler)

    console = logging.StreamHandler()
    console.propagate = False
    console.setLevel(level)
    formatter = logging.Formatter('[%(levelname)s][%(name)s]:%(message)s')
    console.setFormatter(formatter)
    root_log.addHandler(console)

def business_signal_handler(num, stack):  
    lg = logging.getLogger('business_signal_handler')
    lg.warning('BUSINESS PROCESS[{pid}] RECEIVED SIGNAL {n}.'.format(pid=os.getpid(), n=num))
    st.do_business_flag=False


def do_business(work_idx=None, work_full_path=None, task=None, log_level="INFO"):

    signal.signal(signal.SIGTERM, business_signal_handler)
    signal.signal(signal.SIGINT, business_signal_handler)

    log_filename = "%(filename)s_idx%(idx)02d" %{'filename':__name__, 'idx':work_idx}
    init_business_root_log(log_full_path = work_full_path + "log/", filename=log_filename, level=log_level) #, max_bytes=200)

    lg = logging.getLogger('do_business')
    lg.info("[{wi}][{pi}]START BUSINESS WORKING AT [{wp}]".format(wi=work_idx, pi=os.getpid(), wp=work_full_path))
    lg.info("[{wi}][{pi}]TASK LIST:{t}.".format(wi=work_idx, pi=os.getpid(), t=task))

    mongo_con = None
    try:
        mongo_con = pdb.Connection(mocfg['host'], mocfg['port'])
        mongo_con[mocfg['auth_db']].authenticate(mocfg['user'], mocfg['passwd'])
        mongo_db  = mongo_con[mocfg['db']]

        st.do_business_flag = True
        if isinstance(task, list) and len(task) > 0:
            while st.do_business_flag:
                flag = False
                for tk in task:
                    if project_calculator(mongo_db, tk) : flag = True
                if flag:
                    time.sleep( st.calculate_sleep_interval )
                else:
                    lg.info('[{pid}], meta:{mid}, does not has any data,sleep longer.'.format(pid=os.getpid(), mid=task))
                    time.sleep(60)

        else:
            lg.info('[{pid}], META:{mid}, DOES NOT HAS ANY META ID.'.format(pid=os.getpid(), mid=task))
        mongo_con.close()
        mongo_con = None
        lg.info("[{wi}]BUSINESS WORK OVER PID:{pid}".format(wi=work_idx, pid=os.getpid()))
    #except Exception as e:
    except IOError as e:
        if mongo_con : 
            mongo_con.close()
            mongo_con = None
        lg.error( "[{pid}]异常: {e}".format(pid=os.getpid(), e=e) )
