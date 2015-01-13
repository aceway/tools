#!/usr/bin/env python
# -*- coding=utf-8 -*-
########################################################################
#    File Name: project_calculator.py
# 
#         Mail: aceway@qq.com
# Created Time: 2014年08月05日 星期一 15时07分26秒
#  Description: ...
#                
########################################################################

import os
import logging
from time import time
from pymongo import DESCENDING, ASCENDING 
import settings as st


def get_source_data(modb, hash_id, fields=[], coll="", skip=0, limit=10000):
    lg = logging.getLogger('get_source_data')
    data = [1,2,3,4,5]
    return data


def update_data_info(chunk_data, hash_id, calc_base, modb, coll="t_d", calc_time=0):
    lg = logging.getLogger('update_data_info')
    for dt in chunk_data:
        if isinstance(dt,dict) and 'userid' in dt and 'lv' in dt:
            uid = long(dt['userid'])
            lv  = dt['lv']
            query = { 'hash_id':hash_id, 'userid':uid }

            old_data = modb[coll].find_one( query, fields=['prev_data', 'new_data'] )
            lg.debug("[{pid}]:hash id:{hid}, user id:{uid}, old data:{ork}".format(pid=os.getpid(), hid=hash_id, uid=uid, ork=old_data) )
            if isinstance(old_data, dict) and 'new_data' in old_data:
                update= {"$set":{'hash_id':hash_id,'userid':uid,'calc_time':calc_time,'prev_data':old_data['new_data'],'new_data':calc_base,'value':long(lv)}}
                modb[coll].find_and_modify( query, update, upsert=True )
            else:
                insert= {'hash_id':hash_id, 'userid':uid, 'calc_time':calc_time, 'prev_data':calc_base, 'new_data':calc_base, 'value':long(lv) }
                modb[coll].insert( insert )
            calc_base += 1
    pass


def project_calculator(modb, hash_id):
    lg = logging.getLogger('project_calculator')
    lg.info("[[{pi}]Calculate for hash id {hid}.".format(pi=os.getpid(), hid=hash_id))

    total_cnt = 0
    skp = 0
    lmt = 1000
    calc_tm = int(time())

    chunk_data = get_source_data(modb, fields=['a', 'b'], coll="t_c", skip=skp, limit=lmt)
    calc_base = 1
    if isinstance(chunk_data, list) and len( chunk_data ) > 0:
        while isinstance(chunk_data, list) and len( chunk_data ) > 0:
            total_cnt += len(chunk_data)
            update_data_info(chunk_data, hash_id, calc_base, modb, coll="t_d", calc_time=calc_tm)
            calc_base += len(chunk_data)
            skp += lmt
            chunk_data = get_source_data(modb, hash_id, fields=['a', 'b'], coll="t_c", skip=skp, limit=lmt)
        lg.info("[[{pi}]Hash id {hid} calcluate total count:{cnt}.".format(pi=os.getpid(), hid=hash_id, cnt=total_cnt))
        return True
    else:
        return False

if __name__ == '__main__':
	pass
