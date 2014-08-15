#!/usr/bin/env python
# coding=utf-8
import json as simplejson
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer

def trans_data_from_proto_to_json(protoObj, attrs, jsonObj):
    u'''
    *从protobuf对象提取数据，转换成json格式数据。*

    - Args:
        - protoObj:  protobuf对象；
        - attrs: 是一个tuple, 内部为protoobj的属性名称罗列.  []表示内部属性repeated, {k:v}内表示嵌套
        - jsonObj: 转换结果存储到的json对象

    - Returns:
        - 无
    '''
    if isinstance(attrs, tuple) and len(attrs) > 0 :
        for attr in attrs:
            if isinstance(attr, basestring):
            #直接值('a', 'b', 'c')
                val = getattr(protoObj, attr)
                jsonObj[attr] = val
            elif isinstance(attr, dict) and len(attr.items()) == 1:
            #嵌套一个对象({'a':('x', 'y', 'z')}, )
                k,v = attr.items()[0]
                if isinstance(v, tuple):
                    val = getattr(protoObj, k)
                    jsonObj[k] = {}
                    trans_data_from_proto_to_json(val, v, jsonObj[k]) 
            elif isinstance(attr, list) and len(attr) == 1:
            #嵌套反复值/对象 ([ ], )
                info = attr[0]
                if isinstance(info, basestring) and len(info) > 0:
                #被反复嵌套的对象是直接值 (['a'], )
                    val = getattr(protoObj, info)
                    jsonObj[info] = [ v for v in val ]
                elif isinstance(info, dict) and len(info.items()) == 1:
                #被反复嵌套的对象是一个protobuf对象 ( [ { } ],)
                    k, v = info.items()[0]
                    val  = getattr(protoObj, k)
                    jsonObj[k] = []
                    if isinstance(v, basestring): #([{'a':"xxx"}],)
                        jsonObj[k] = []
                        for dt in val:
                            tmpJson = {}
                            trans_data_from_proto_to_json(dt, (v,), tmpJson )
                            jsonObj[k].append(tmpJson)
                    elif isinstance(v, tuple): #([{'a':('x', 'y', 'z') }],)
                        for dt in val:
                            tmpJson = {}
                            trans_data_from_proto_to_json(dt, v, tmpJson)
                            jsonObj[k].append(tmpJson)

def trans_data_from_dict_to_proto(protoObj, attrsIn, dictObj):
    u'''
    *根据指定的字段属性将数据打包进protobuf对象*

    - Args:
        - protoObj: protobuf对象，从dictObj中解析出的数据将被打包进该对象；
        - attrsIn: 必须是一个tuple, 内部为protoObj的属性名称罗列, []表示内部属性repeated, {k:v}内表示嵌套，
            - string,int,long,float,bool类型的repeat, 在attr名字前分别加s,i,l,f,b表示,其value用逗号分割
            - ('name', )
            - ('msg_id', 'errcode')
            - (['stask_ids'], )  #task_ids前的s表示 string
            - ( [{'suser_ids'}], )
            - ([{ 'prises':( 'prise_name', [{'data': ('time', 'count') }] ) }], )
            - ( [{'roles':('uid',  'reg_time', 'channel_id', 'server_id', 'name', 'role_type', 'lv', 'last_login_tm') }], )
            - 注：RepeatedScalarFieldContainer 类型未找到动态获取对象的基础类型，故类型信息放在对应字段名的第一个字符，配置时需要注意
        - dictObj: 字典，存储请求的条件信息，将被pack进protoObj，可用request.GET，requst.POST

    - Returns:
        - 构造出的proto对象
    '''
    if isinstance(attrsIn, tuple):
        for attr in attrsIn:
            if isinstance(attr, basestring) and len(attr)>0 and hasattr(protoObj, attr):
            #直接基础类型数据
                v = dictObj.get(attr, None)
                if v is not None:
                    attr_type = type( getattr(protoObj, attr) )
                    setattr( protoObj, attr, attr_type(v) )
            elif isinstance(attr, dict) and len(attr.items()) == 1:
            #直接一个protobuf对象
                pattr, subattr = attr.items()[0]
                if isinstance(pattr, basestring) and len(pattr)>0 and hasattr(protoObj, pattr) and pattr in dictObj: 
                    if isinstance(subattr, tuple):    
                    #对象非repeated
                        trans_data_from_dict_to_proto(getattr(protoObj, pattr), subattr, dictObj.get(pattr, None))
                    elif isinstance(subattr, list) and len(subattr)==1 and isinstance(subattr[0], tuple):
                    #对象repeated
                        values = simplejson.loads( dictObj.get(pattr) )
                        if len(values) > 0 and type(getattr(protoObj, pattr)) == RepeatedCompositeFieldContainer :
                            for value in values:
                                adder = getattr(protoObj, pattr).add()
                                trans_data_from_dict_to_proto(adder, subattr, value)
                else:
                    pass#配置格式错误
            elif isinstance(attr, list) and len(attr) == 1: #and hasattr(protoObj, attr[0]):
            #repeated一个基础类型/protobuf对象
                if isinstance(attr[0], basestring) and len(attr[0]) > 1 and hasattr(protoObj, attr[0][1:]):
                #被repeated的是基础类型(char,int,long...)对象
                    #RepeatedScalarFieldContainer 数据类型的获取方式？  #暂时用hack方式在v的值上实现s,i,l,f,b分贝表示string,int,long,float,bool类型
                    values = dictObj.get(attr[0], None)
                    type_dict = {'b':bool, 's':str, 'i':int, 'l':long, 'f':float}
                    type_char = attr[0][0]
                    attr_type = type_dict[type_char]
                    attr = attr[0][1:]
                    att = getattr(protoObj, attr)
                    if att is not None and type(att) == RepeatedScalarFieldContainer and isinstance(values, basestring):
                        vlist = values.strip(', ').split(',')
                        for v in vlist:
                            att.append( attr_type(v) )
                    else:
                        pass #数据格式有误
                elif isinstance(attr[0], dict) and len(attr[0].items()) == 1:
                #被repeated的是protobuf对象
                    pattr, subattr = attr[0].items()[0]
                    if isinstance(pattr, basestring) and len(pattr)>0 and hasattr(protoObj, pattr) and pattr in dictObj: 
                        if isinstance(subattr, tuple):
                        #对象内部成员是protobuf对象类型
                            dt = dictObj.get(pattr)
                            if isinstance(dt ,basestring):
                                values = simplejson.loads( dt )
                            else:
                                values = dt
                            if len(values) > 0 and type(getattr(protoObj, pattr)) == RepeatedCompositeFieldContainer :
                                for value in values:
                                    adder = getattr(protoObj, pattr).add()
                                    trans_data_from_dict_to_proto(adder, subattr, value)
                            else:
                                pass #数据格式错误
                        else:
                            pass #数据格式错误
                    else:
                        pass #数据格式有误
    return protoObj
