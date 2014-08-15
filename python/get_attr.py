#!/usr/bin/env python
# coding=utf-8
#########################################################
#     File Name: get_attr.py
#     Author: aceway.doogga.com
#     Mail: aceway@doogga.com 
#     Created Time: 2014年06月24日 星期二 13时09分55秒
#     Description: 
#########################################################

def get_obj_attr(obj):
    return [(attr, type(getattr(obj, str(attr)))) for attr in obj.__dict__ if not attr.startswith('_')]
