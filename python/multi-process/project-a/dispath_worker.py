#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: dispath_worker.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月13日 星期四 17时18分06秒
#########################################################
import os, signal, time, sys
import logging
import settings as st

g_work_dict={}
g_do_dispatch_flag=True

def init_dispath_root_log(log_full_path=None, filename=__name__, level="INFO", max_bytes=1024*1024*5, backup_count=5):
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

def do_dispath(work_full_path=None, work_dict=None, log_level="INFO"):
    """
    TODO: 监控分发任务的
    """
    init_dispath_root_log(log_full_path = work_full_path + "log/", filename=__name__, level=log_level) #, max_bytes=200)
    lg = logging.getLogger('do_dispath')

    lg.info("START DISPATH WORKING AT [{pth}, PID:{pid}]".format(pth=work_full_path, pid=os.getpid()))
    lg.info("HAS DISPATHED BUSINESS WORK DICT LEN={ln}.".format(ln=len(work_dict)))

    for (k, v) in work_dict.items():
        lg.info("BUSINESS WORK PROCESS [{idx}]-len={ln}:{li}".format(idx=k, ln=len(v), li=v))

    signal.signal(signal.SIGTERM, dispatch_signal_handler)
    signal.signal(signal.SIGINT, dispatch_signal_handler)

    global g_work_dict, g_do_dispatch_flag
    g_work_dict = work_dict

    while g_do_dispatch_flag:
        lg.info('GET WORK DICT IS {dct}.'.format(dct=work_dict))
        lg.info("[{pid}]RELOADING FOR DISPACH TO BUSINESS PROCESS...".format(pid=os.getpid()))
        time.sleep( st.monitor_detect_interval )

def dispatch_signal_handler(num, stack):
    lg = logging.getLogger('dispatch_signal_handler')
    lg.warning('DISPATCH PROCESS[{pid}] RECEIVED SIGNAL {n}'.format(pid=os.getpid(), n=num))
    lg.warning('STOP BUSINESS WORK PROCESS(len={ln}):{dct}.'.format(ln=len(g_work_dict), dct=g_work_dict))
    for k in g_work_dict.keys():
        lg.warning('KILL BUSINESS PROCESS [{k}]-LEN={ln}:{dct}'.format(k=k, ln=len(g_work_dict[k]), dct=g_work_dict[k]))
        os.kill(k, num)
    time.sleep(1)
    global g_do_dispatch_flag
    g_do_dispatch_flag = False
