#!/usr/bin/env python
# -*- coding=utf-8 -*-

def choose_tips(select_items=['YES', 'NO', 'Y', 'N'], tips="Yes/No?(No):", default="No", try_times=3):
    condition = True
    if isinstance(try_times, (int,long)) and try_times > 0:
        condition = try_times
    elif isinstance(try_times, (int,long)) and try_times <= 0:
        condition = True
    else:
        raise TypeError("参数错误，try_times 必须为整数.")
    idx = 1
    choose = None
    while(condition):
        full_tips = "[{idx}] {t}".format(idx=idx, t=tips)
        ret = raw_input(full_tips)
        if ret.strip().upper() in select_items:
            choose = ret.strip().upper()
            break;
        if ret.strip().upper() == "":
            choose = default
            break;
        if not isinstance(condition, bool):
            print "输入的选择非法，请重新输入"
            condition -= 1
        idx += 1
    if choose is None: choose = default
    return choose


if __name__ == '__main__':
	pass
