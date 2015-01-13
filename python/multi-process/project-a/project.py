#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: project.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 16时02分03秒
#########################################################
import sys, os
import settings as st
from worker import do_work


def main(work_full_path=None):
    try:
        if not os.path.isdir(work_full_path):
            print "{clr_y}work_full_path is not path:{clr_r}{p}{clr_y}, exit.{clr_e}".format(clr_y=st.color['FG_YELLOW'], p=work_full_path, clr_r=st.color['FG_RED'], clr_e=st.color['END'])
            return
        if not work_full_path.endswith("/"): work_full_path = work_full_path + "/"
        pid = os.getpid()
        pid_file = "{p}daemon-{pid}.pid".format(p=work_full_path, pid=pid)

        with open(pid_file, "w") as pfile:
            pfile.write(str(pid))
        print "Start work, recorded pid file:{p}".format(p=pid_file)

        if st.background:
            make_daemon(work_full_path=work_full_path)
        do_work(work_full_path=work_full_path)
    finally:
        try:
            if os.path.isfile(pid_file):
                os.remove(pid_file)
                print "{clr_g}WORK OVER{clr_e}, clear the pid file:{p}".format( clr_g=st.color['FG_GREEN'], clr_e=st.color['END'], p=pid_file )
        except OSError:
            pass  # file maybe does not exists

def make_daemon(work_full_path="/tmp/"):
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) 
    except OSError, e: 
        print >> sys.stderr, "{clr}Fork #1 process failed: {err} ({desc}).{e}".format(clr=st.color['FG_RED'], err=e.errno, desc=e.strerror, e=st.color['END'] ) 
        sys.exit(1)
    # decouple from parent environment
    os.chdir(work_full_path)
    os.setsid() 
    os.umask(0) 
    try: 
        pid = os.fork() 
        if pid > 0: sys.exit(0) 
    except OSError, e: 
        print >> sys.stderr, "{clr}Fork #2 process failed: {err} ({desc}).{e}".format(clr=st.color['FG_RED'], err=e.errno, desc=e.strerror, e=st.color['END'] ) 
        sys.exit(1) 
    # redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    si = file('/dev/null', 'r')
    so = file('/dev/null', 'a+')
    se = file('/dev/null', 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == "__main__":
    work_dir = st.work_full_path
    main(work_full_path=work_dir)
