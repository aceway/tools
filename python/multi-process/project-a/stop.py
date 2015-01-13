#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: stop.py
#     Author: aceway
#     Mail: aceway@qq.com 
#     Created Time: 2014年02月11日 星期二 16时02分03秒
#########################################################
import os
import signal
import fnmatch
import time
import settings as st

def stop_the_process(the_pid):
    print "{clr_y}Stop the proccess:{clr_r}{pid}{clr_e}.".format( clr_y=st.color['FG_YELLOW'], pid=the_pid, clr_r=st.color['FG_RED'], clr_e=st.color['END'] )
    try:
        os.kill(int(the_pid), signal.SIGTERM)
        time.sleep(1)
        os.kill(int(the_pid), 0)
        return True
    except OSError as ex:
        print ex, the_pid
        return False

def main(work_full_path=None):
    if not os.path.isdir(work_full_path):
        print "{clr_y}work_full_path is not path:{clr_r}{p}.{clr_e}".format(clr_y=st.color['FG_YELLOW'], clr_r=st.color['FG_RED'], clr_e=st.color['END'], p= work_full_path)
        return False
    bKilled =False
    if not work_full_path.endswith("/"): work_full_path = work_full_path + "/"
    for pfile in os.listdir(work_full_path):
        if fnmatch.fnmatch(pfile, '*.pid'):
            if(len(pfile.split('.')[0].split('-'))==2):
                pid = pfile.split('.')[0].split('-')[1]
                if(stop_the_process(pid)):
                    print st.color['FG_GREEN'], "OK", st.color['END']
                else:
                    print st.color['FG_RED'], "FAILED", st.color['END']
                    #os.remove(work_full_path + pfile)
                bKilled = True
    return bKilled

if __name__ == "__main__":
    work_dir = st.work_full_path
    if(main(work_full_path=work_dir)):
        pass
    else:
        print st.color['FG_YELLOW'], "No pid file in work dir:", st.color['FG_RED'], work_dir, st.color['END']
