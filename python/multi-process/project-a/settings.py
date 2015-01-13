# -*- coding:utf-8 -*-
import os

background=False   #background为True，程序将在daemon模式运行
background=True

BASE_DIR    = os.path.dirname(__file__)
if not BASE_DIR.endswith('/'): BASE_DIR += '/'

work_full_path = BASE_DIR       #工作目录，日志，pid文件将在该目录下
work_proc_cnt  = 3              #用于计算的工作进程数， 不配置，或配置0，负数则程序自动根据 CPU数据和区服数据分配
log_level      = "DEBUG"        #CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET

do_business_flag=True           #工作进程是否在计算的标志，用于检测保障一个任务完整的执行完
monitor_detect_interval=5200    #检测进程隔多久检测一次，单位: 秒
calculate_sleep_interval=900    #成功计算一次数据后休眠时常，单位: 秒


mongo_cfg={
    'host'   : "localhost",
    'port'   : 27017,
    'charset': 'utf8',
    'db'     : "DB_PROJECT_APP",
    'auth_db': "admin",
    'user'   : "root",
    'passwd' : "xxxxxx",
}

color={
    "FG_BLAcK": "\033[30m",   # 将字符的显示颜色改为黑色
    "FG_RED"  : "\033[31m",   # 将字符的显示颜色改为红色
    "FG_GREEN": "\033[32m",   # 将字符的显示颜色改为绿色
    "FG_YELLOW": "\033[33m",  # 将字符的显示颜色改为黄色
    "FG_BLUE" : "\033[34m",   # 将字符的显示颜色改为蓝色
    "FG_PINK" : "\033[35m",   # 将字符的显示颜色改为紫色
    "FG_LIGHT_BLUE": "\033[36m",   # 将字符的显示颜色改为淡蓝色
    "FG_WHITE": "\033[37m",   # 将字符的显示颜色改为灰色

    "BG_BLACK" : "\033[40m",   # 将背景色设置为黑色
    "BG_RED"   : "\033[41m",   # 将背景色设置为红色
    "BG_GREEN" : "\033[42m",   # 将背景色设置为绿色
    "BG_YELLOW": "\033[43m",   # 将背景色设置为黄色
    "BG_BLUE"  : "\033[44m",   # 将背景色设置为蓝色
    "BG_PINK"  : "\033[45m",   # 将背景色设置为紫色
    "BG_LIGHT_BLUE": "\033[46m",   # 将背景色设置为淡蓝色
    "BG_WHITE" : "\033[47m",   # 将背景色设置为灰色 
    "END"      :"\033[0;00m",
}
