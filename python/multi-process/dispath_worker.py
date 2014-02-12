#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: dispath_worker.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 17时50分04秒
#########################################################
import os#,sys

def do_dispath(work_list=None, root_path=None):
    print "Start dispath working at [{0}, pid:{1}".format(root_path, os.getpid())
    print "Business work pid list: ", work_list
    #while True:
        #pass
    print "Dispath work over pid:{0}".format(os.getpid())
