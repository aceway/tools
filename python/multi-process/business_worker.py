#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: business_worker.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 17时09分45秒
#########################################################
import os, time#,sys

def do_business(work_idx=None, root_path=None):
    print "[{0}]Start business working at [{1}]... pid:{2}".format(work_idx, root_path, os.getpid())
    #while True:
        #pass
    time.sleep(3)
    print "[{0}]Business work over pid:{1}".format(work_idx, os.getpid())
