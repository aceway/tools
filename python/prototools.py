#!/usr/bin/env python                        
# -*- coding=utf-8 -*-                       
########################################################################
#    File Name: prototools.py                
#                                            
#       Author: aceway                       
#         Mail: aceway@qq.com                
# Created Time: 2014年08月25日 星期一 21时55分33秒
#  Description: ...                          
#                                            
########################################################################
import json
try:                                         
    from google.protobuf.internal.containers import RepeatedCompositeFieldContainer, RepeatedScalarFieldContainer
except:                                      
    print "请为python安装google的protobuf模块"  

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

def trans_data_from_json_to_proto(protoObj, attrsIn, jsonObj):
    u'''
    *根据指定的字段属性将数据打包进protobuf对象---主要是直接的json数据

    - Args:
        - protoObj: protobuf对象，从jsonObj中解析出的数据将被打包进该对象；
        - attrsIn: 必须是一个tuple, 内部为protoObj的属性名称罗列, []表示内部属性repeated, {k:v}内表示嵌套，
            - Example:
                - ( 'msg_id', 'name')
                - ( {'roles':('uid',  'reg_time', 'channel_id', 'server_id', 'name', 'role_type', 'lv', 'last_login_tm') }, )
                - ( ['task_ids'], )
                - ( [{'roles':('uid',  'reg_time', 'channel_id', 'server_id', 'name', 'role_type', 'lv', 'last_login_tm') }], )
                - ( [{ 'prises':( 'prise_name', [{'data': ('time', 'count') }] ) }], )
    - Returns:
        - 构造出的proto对象
    '''
    if isinstance(attrsIn, tuple):
        for attr in attrsIn:
            if isinstance(attr, basestring) and len(attr)>0 and hasattr(protoObj, attr) and attr in jsonObj:
            #直接基础类型数据(char,int,long...)对象
                v = jsonObj.get(attr, None)
                if v is not None:
                    attr_type = type( getattr(protoObj, attr) )
                    setattr( protoObj, attr, attr_type(v) )
            elif isinstance(attr, dict) and len(attr.items()) == 1:
            #直接一个protobuf对象
                pattr, subattr = attr.items()[0]
                if isinstance(pattr, basestring) and len(pattr)>0 and hasattr(protoObj, pattr) and pattr in jsonObj: 
                    if isinstance(subattr, tuple):    
                    #对象非repeated
                        trans_data_from_dict_to_proto(getattr(protoObj, pattr), subattr, jsonObj.get(pattr, None))
                    else:
                        pass#配置格式错误
                else:
                    pass    #配置格式错误
            elif isinstance(attr, list) and len(attr) == 1: #and hasattr(protoObj, attr[0]):
            #repeated类型
                if isinstance(attr[0], basestring) and len(attr[0]) > 1 and hasattr(protoObj, attr[0][1:]):
                #被repeated的是基础类型(char,int,long...)对象
                    #RepeatedScalarFieldContainer 数据类型的获取方式？  #暂时用hack方式在v的值上实现s,i,l,f,b分贝表示string,int,long,float,bool类型
                    values = jsonObj.get(attr[0], None)
                    type_dict = {'b':bool, 's':str, 'i':int, 'l':long, 'f':float, }
                    type_char = attr[0][0]
                    attr_type = type_dict.get(type_char, str)
                    attr = attr[0][1:]
                    att = getattr(protoObj, attr)
                    if att is not None and type(att) == RepeatedScalarFieldContainer and isinstance(values, list):
                        for v in values:
                            att.append( attr_type(v) )
                    else:
                        pass #数据格式有误
                elif isinstance(attr[0], dict) and len(attr[0].items()) == 1:
                #被repeated的是protobuf对象
                    pattr, subattr = attr[0].items()[0]
                    if isinstance(pattr, basestring) and len(pattr)>0 and hasattr(protoObj, pattr) and pattr in jsonObj: 
                        if isinstance(subattr, tuple):
                        #对象内部成员是protobuf对象类型
                            values = jsonObj.get(pattr, None)
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


def trans_data_from_dict_to_proto(protoObj, attrsIn, dictObj):
    u'''
    *根据指定的字段属性将数据打包进protobuf对象---主要是直接从HTTP的GET, POST中取数据打包进protoObj*

    - Args:
        - protoObj: protobuf对象，从dictObj中解析出的数据将被打包进该对象；
        - attrsIn: 必须是一个tuple, 内部为protoObj的属性名称罗列, []表示内部属性repeated, {k:v}内表示嵌套，
            - string,int,long,float,bool类型的repeat, 在attr名字前分别加s,i,l,f,b表示,其value用逗号分割
            - Example:
                - ('name', )
                - ('msg_id', 'errcode')
                - (['stask_ids'], )  #task_ids前的s表示 string
                - ( [{'suser_ids'}], )
                - ([{ 'prises':( 'prise_name', [{'data': ('time', 'count') }] ) }], )
                - ( [{'roles':('uid',  'reg_time', 'channel_id', 'server_id', 'name', 'role_type', 'lv', 'last_login_tm') }], )
            - 注：RepeatedScalarFieldContainer 类型未找到动态获取对象的基础类型，故类型信息放在对应字段名的第一个字符，配置时需要注意
        - dictObj: 字典，存储请求的条件信息，将被pack进protoObj，可直接用request.GET，requst.POST作为该参数

    - Returns:
        - 构造出的proto对象
    '''
    if isinstance(attrsIn, tuple):
        for attr in attrsIn:
            if isinstance(attr, basestring) and len(attr)>0 and hasattr(protoObj, attr):
            #直接基础类型数据(char,int,long...)对象
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
                        values = json.loads( dictObj.get(pattr) )
                        if len(values) > 0 and type(getattr(protoObj, pattr)) == RepeatedCompositeFieldContainer :
                            for value in values:
                                adder = getattr(protoObj, pattr).add()
                                trans_data_from_dict_to_proto(adder, subattr, value)
                else:
                    pass#配置格式错误
            elif isinstance(attr, list) and len(attr) == 1: #and hasattr(protoObj, attr[0]):
            #repeated类型
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
                                values = json.loads( dt )
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


def get_proto_file_lines(proto_file, proto_lines_data=None, verbose=False):
    u"""
    将proto协议文件转换从一行---去除注释, 方便从中搜索，匹配，查找某一proto协议
    """
    if proto_lines_data is None:
        import re
        re_rpl = re.compile(r"\s+")
        if os.path.isfile( proto_file ):
            with open(proto_file) as pf:
                bContinue = False
                lines = []
                for line in pf:
                    line = line.strip(' \t\r\n')
                    if len(line) == 0: continue
                    if line.startswith('/*') and line.endswith('*/'): continue
                    if line.startswith('/*'):
                        bContinue = True
                        continue
                    if line.endswith('*/'):
                        bContinue = False
                        continue
                    if bContinue: continue
                    if line.startswith('//'): continue
                    line = line.split("//")[0]
                    if len( line.strip() ) > 0:
                        lines.append(line.strip(' \t\r\n').replace("\t", " "))
                lines_data = "".join(lines)
                proto_lines_data, number = re_rpl.subn(" ", lines_data)
                if verbose: print "re match times: ", number
            return proto_lines_data
        else:
            return None
    else:
        return proto_lines_data


def extrace_proto_define_from_line(line_proto_data, verbose=False):
    u"""
    从行proto协议里提取所有 message xxxx_in的定义，返回：[ (name, attr), ]
    """
    proto_list = []
    max_pos = len(line_proto_data)

    end_tag   ="_in{"
    begin_tag ="}message"
    end_pos   = line_proto_data.find(end_tag)
    begin_pos = line_proto_data.rfind(begin_tag, 0, end_pos)
    while begin_pos >= 0 and end_pos >= 0:
        msg_name = line_proto_data[ begin_pos+len(begin_tag) : end_pos ]
        if verbose: print msg_name
        idx = end_pos
        flags = 0
        while idx < max_pos:
            if line_proto_data[idx] == "{":
                flags += 1
            elif line_proto_data[idx] == "}":
                flags -= 1
                if flags == 0: break;
            idx += 1
        msg_define = line_proto_data[ end_pos + len(end_tag) -1 : idx +1 ]
        proto_list.append( ( msg_name.strip(),  msg_define.strip() ) )

        line_proto_data = line_proto_data[ end_pos + len(end_tag) : ]
        end_pos   = line_proto_data.find(end_tag)
        begin_pos = line_proto_data.rfind(begin_tag, 0, end_pos)

    return proto_list


def get_message_define_info(line_proto_data, msg_type, verbose=False):
    u"""
    从行proto协议里提取指定message的定义---用在message引用其它message定义
    
    """
    max_pos = len(line_proto_data)
    find_str = "message " + msg_type + "{"
    start_pos = line_proto_data.find( find_str )
    if start_pos >= 0:
        idx = start_pos + 1
        flags = 0
        while idx < max_pos:
            if line_proto_data[idx] == "{":
                flags += 1
            elif line_proto_data[idx] == "}":
                flags -= 1
                if flags == 0:break;
            idx += 1
        msg_define = line_proto_data[ start_pos + len(find_str) -1 : idx + 1 ]
        if verbose: print "enbedded message define: ", msg_define
        return msg_define
    else:
        return None

def pack_attr_value_with_proto_define(proto_define_text, proto_line_data, verbose=False):
    ptxt = proto_define_text.strip("{};")
    define_info = ptxt.split(";");
    define_info = [ d.strip() for d in define_info if len(d.strip())>0 ]
    av = {}
    attr_list = []
    for dinfo in define_info:
        attr_info = dinfo.strip().split(" ")
        attr_info = [ a.strip() for a in attr_info if len(a.strip())>0 ]
        at_type = attr_info[1]
        at_name = attr_info[2]
        if verbose: print "type:", at_type, ", name:", at_name
        
        if attr_info[0] in [ "required", "optional" ]:
            if   at_type in [ "int32", "int64" ]:
                attr_list.append(at_name)
                av[ at_name ] = pcv.get(at_name, -1)
            elif at_type in [ "uint32", "uint64" ]:
                attr_list.append(at_name)
                av[ at_name ] =  pcv.get(at_name, 123456)
            elif "string"== at_type:
                attr_list.append(at_name)
                av[ at_name ] = pcv.get(at_name, "test-str")
            elif "bytes" == at_type:
                attr_list.append(at_name)
                av[ at_name ] = pcv.get(at_name, "test-byte")
            elif "bool" == at_type:
                attr_list.append(at_name)
                av[ at_name ] = pcv.get(at_name, True)
            else:
                em_define = get_message_define_info(proto_line_data, at_type, verbose)
                em_info = pack_attr_value_with_proto_define( em_define, proto_line_data, verbose=verbose )
                attr_list.append( { at_name: em_info[0]})
                av[ at_name ] = em_info[1]
        elif attr_info[0] == "repeated":
            if at_type in [ "int32" ]:
                attr_list.append( ["i"+at_name] )
                av[ at_name ] = [ pcv.get(at_name, -1), pcv.get(at_name, -2)]
            elif   at_type in [ "int64" ]:
                attr_list.append( ["l"+at_name] )
                av[ at_name ] = [ pcv.get(at_name, -1) ,pcv.get(at_name, -2)]
            elif at_type in [ "uint32" ]:
                attr_list.append( ["i"+at_name] )
                av[ at_name ] = [pcv.get(at_name, 123), pcv.get(at_name, 456)]
            elif at_type in [ "uint64" ]:
                attr_list.append( ["l"+at_name] )
                av[ at_name ] = [pcv.get(at_name, 123), pcv.get(at_name, 456)]
            elif at_type in [ "string", "byte" ]:
                attr_list.append( ["s"+at_name] )
                av[ at_name ] = [pcv.get(at_name, "test1"), pcv.get(at_name, "test2"), pcv.get(at_name, "test3")]
            elif at_type in [ "bool" ]:
                attr_list.append( ["b"+at_name] )
                av[ at_name ] = [pcv.get(at_name, True), pcv.get(at_name, False)]
            else:
                em_define = get_message_define_info(proto_line_data, at_type, verbose)
                em_info = pack_attr_value_with_proto_define( em_define, proto_line_data, verbose=verbose )
                attr_list.append([ { at_name: [ em_info[0] ] } ])
                av[ at_name ] = em_info[1]
        else:
            continue
    return tuple(attr_list), av

def has_out_in_proto_file(line_proto_data, msg_name, verbose=False):
    if not msg_name.endswith('_out'):
        if msg_name.endswith('_'):
            msg_name += "out"
        else:
            msg_name += "_out"
    find_str = "message " + msg_name + "{"
    start_pos = line_proto_data.find( find_str )
    if start_pos >= 0:
        return True
    else:
        return False

def gen_test_data_with_proto_file(proto_file, out_file, verbose=False):
    u"""
    遍历proto文件里的 _in消息，搜索定义 attr, 填充出value, 写入文件
    """
    if verbose: print "Generation info:\n\tproto file:{p}\n\tout file:{o}".format(p=proto_file,o=out_file)
    if os.path.isfile(proto_file):
        with open(proto_file, 'r') as pfile:
            with open(out_file, 'w') as ofile:
                proto_lines = get_proto_file_lines(proto_file, verbose=verbose)
                proto_list = extrace_proto_define_from_line(proto_lines, verbose=verbose)

                file_name = out_file[ out_file.rfind('/') + 1: ]
                dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ofile.write( out_file_header.format( fname = file_name, tm=dt ) )

                ofile.write( "test_data_list=[\n" )
                for (name, attr) in proto_list:
                    attr = attr.strip("{};")
                    av = pack_attr_value_with_proto_define(attr, proto_lines, verbose=verbose)
                    out = has_out_in_proto_file(proto_lines, name)
                    av_line = "(%r, %r, %r)"%(name, av, out)
                    #print av_line
                    ofile.write( "\t" )
                    ofile.write( av_line )
                    #ofile.write( str((name, av)) )
                    ofile.write( ",\n\n" )
                ofile.write( "]" )
        return True
    else:
        print "It's not a file: ", proto_file
        return False

