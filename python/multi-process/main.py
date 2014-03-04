#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: main.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 16时02分03秒
#########################################################
import sys, os, time
from framework import run

@profile
def main(root_path=None):
    if not os.path.isdir(root_path): os.makedirs(root_path)
    if not root_path.strip().endswith("/"): root_path = root_path.strip() + "/"
    pid = os.getpid()
    pid_file = "/tmp/daemon-{0}.pid".format(pid)
    log_file = "{0}log/daemon-{1}.log".format(root_path, pid)
    with open(pid_file, "w") as pfile:
        pfile.write(str(pid))
    with open(log_file, "a") as lfile:
        lfile.write('[{0}]:{1}\n'.format(pid, time.ctime(time.time()))) 
        lfile.flush() 
        run(root_path=root_path)

def make_daemon(root_path="/tmp/"):
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) 
    except OSError, e: 
        print >> sys.stderr, "Fork #1 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)
    os.chdir(root_path)
    os.setsid() 
    os.umask(0) 
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) 
    except OSError, e: 
        print >> sys.stderr, "Fork #2 failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

if __name__ == "__main__":
    work_dir = "./"
    if len(sys.argv) > 1:
        make_daemon(root_path=work_dir)
    main(root_path=work_dir) 
