#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: time_trace.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月12日 星期三 14时59分26秒
#########################################################
import time
class TimerTrace(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
    def __enter__(self):
        self.start = time.time()
        return self
    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print 'elapsed time: %f ms' % self.msecs
