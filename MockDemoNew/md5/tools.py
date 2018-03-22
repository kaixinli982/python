# -*- coding:utf-8 -*-
# import json
from operator import itemgetter
import json
import hashlib

#json->dict
def json_to_dict(src_json):

    src_json = str(src_json)
    dic = eval(src_json)
    if type(dic)=='dict':
        return dic
    else:
        return False


# json_to_dict(a)

#sorting by Dictionary KEY
def dict_sorted(dic,reverse=False):
    dic_list_order=sorted(dic.iteritems(),key=lambda d:d[0] ,reverse=reverse)
    dic_temp_order=str(dic_list_order)
    dic_order="{"+dic_temp_order[1:len(dic_temp_order)-1]+"}"
    return (dic_order,dic_list_order)

#processe the dictionary value
def dict_value_string(list,s=""):
    for i in range(len(list)):
        s+= str(list[i][1])
    return s

#add sault and  sign
def xxd_md5(src_json,md5type="str",salt=""):

    s = {}
    if md5type=="str":
        src_string=src_json
    elif md5type=="dict":
        src_string=json_to_dict(src_json)
        if src_string!=False:
            src_string=dict_sorted(src_string)[1]
            src_string=dict_value_string(src_string)
        else:
            print "TypeError:请输入正确的类型"
            return {"code":"TypeError","data":"TypeError:请输入正确的类型"}
    else :
        print "TypeError:请输入正确的类型"

        return {"code": "TypeError", "data": "TypeError:请输入正确的类型"}
    length =len(src_string)
    src_string=src_string+salt
    m2 = hashlib.md5()
    m2.update(src_string)
    value=m2.hexdigest()
    s={'md5($salt)':value}
    src_string=src_string[:length]
    for i in range(1,4):
        m2 = hashlib.md5()
        m2.update(src_string)
        src_string= m2.hexdigest()
        key="md5*"+str(i)
        s[key]=src_string
        print type(s)

    return {"code":"000000","data":s}
