# -*-coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render,render_to_response
from models import *
import toolbox
from django.http import HttpResponse
import models
import datetime,copy,time,threading
import requests
import tool
import json,random

def index(req):
    return render(req,'stress_testing/index.html')
#Single interface home page
def single_interface(req):
    return render(req,'stress_testing/testing.html')
#Single interface pressure measurement
def stress_testing(req):
    # type=0
    result_tmp={}
    try:
        #Front-end data acquisition processing.
        thread_count, cycles, delay, control_type, url, type, header, data, response_code, ramup_time, serialnum, name, serviceIp=tool.get_request_data(req)

        try:
            result=tool.thread_config(thread_count, cycles, delay, control_type, url, type, header, data, response_code,ramup_time,serialnum,name,serviceIp)
            result_tmp = tool.dict_to_json(result)

        except:
            print '请求失败'
    except:
        print '首次进入单接口压测页面'



    return HttpResponse(result_tmp)

