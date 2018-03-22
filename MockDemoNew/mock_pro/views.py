# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import json

from django.shortcuts import render,render_to_response
from models import *
import toolbox
from django.http import HttpResponse
import datetime,copy,time,threading
import requests

import urllib2,urllib,hashlib
# Create your views here.

def index(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/index.html',context)

def indexPost(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexPost.html',context)
def indexPatch(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexPatch.html',context)
def indexPut(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexPut.html',context)
def indexDelete(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexDelete.html',context)

def indexXXD(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexXXD.html',context)

def indexGet(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexGet.html',context)

def indexGetBatch(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexGetBatch.html',context)

def indexPostBatch(req):
    Request_List = Request.objects.all()
    context = {'Request_List':Request_List}
    return render(req,'mock_pro/indexPostBatch.html',context)

#post
def post_ready(req,mock_pro_id):
    # print "开始调用post_ready接口req：",req,"mock_pro_id",mock_pro_id
    prc = Request.objects.get(id=mock_pro_id)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    unite = Request_Unite.objects.filter(f_key=mock_pro_id)
    unite = toolbox.uniteDict(toolbox.requestDict(unite))
    print "_____________"

    data = toolbox.requestDict(temp)
    print "_____________"
    #Determine if there are pass-through fields
    try:
        backup = req.GET['backup']
        response = req.GET['text']
        print 'backup',backup
        data=toolbox.data_trans(data,backup,response)
    except:
        print "不是联调方式"
    print "请求数据data:::::",req,mock_pro_id,prc.type
    text=""
    data_src=""
    try:
        text, data_src = xxd_request(req, mock_pro_id, prc.type)
    except:
        print "接口请求 solo"
    print "_____________"

    context = {'url':prc.url,'data':data,'name':prc.name,'unite':unite,"text": str(text), "data_src": str(data_src)}
    #return render(req,'mock_pro/post_sub.html',context)
    return render(req,'mock_pro/post_sub_new.html',context)

def post_batch_ready(req,mock_pro_id):
    prc = Request.objects.get(id=mock_pro_id)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    data = toolbox.requestDict(temp,"batch")#不进行数据预处理
    context = {'url':prc.url,'data':data,'name':prc.name}
    return render(req,'mock_pro/post_batch_sub.html',context)

def post_ok_old(req,mock_pro_id):
    data_src=toolbox.reqGETDict(req.GET)[0]
    header_src =toolbox.reqGETDict(req.GET)[1]
    # print toolbox.reqGETDict(req.GET)
    print str(header_src)
    data = urllib.urlencode(data_src)
    start = time.time()
    url2 = urllib2.Request(req.GET['url'],data)
    for i in header_src: #头文件更改
        url2.add_header(i,header_src[i])
    response = urllib2.urlopen(url2)
    apicontent = response.read()
    print "data_src!"+str(data_src)
    toolbox.logInsert(req.GET['url'],data_src,'POST',
               Request.objects.get(id=mock_pro_id).name,apicontent,
               Request.objects.get(id=mock_pro_id),str(time.time()-start),str(len(apicontent)))
    return HttpResponse(apicontent)

@toolbox.reqLog("POST")
def post_ok(req,mock_pro_id):
    data_src,header_src=toolbox.reqGETDict(req.GET)
    data_src =str(data_src)
    data_src = data_src.replace("u'","\"")
    data_src = data_src.replace("'", "\"")
    payload=str({"data":str(data_src)})
    response = requests.request("POST", req.GET['url'], data=payload, headers=header_src)
    return response.text,data_src

def xxd_request_ready(req,mock_pro_id):
    prc = Request.objects.get(id=mock_pro_id)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    unite = Request_Unite.objects.filter(f_key=mock_pro_id)
    data = toolbox.requestDict(temp)
    context = {'url': prc.url, 'data': data, 'name': prc.name}
    return render(req, 'mock_pro/post_sub_new.html', context)


# @toolbox.xxd_reqLog("2")
@toolbox.xxd_reqLog("")
def xxd_request2(req,mock_pro_id,req_type):
    print "开始调用xxd_request2接口",req.GET['url']
    data_src, header_src = toolbox.reqGETDict(req.GET)
    payload = toolbox.xxdData(data_src)
    payload=toolbox.str_dic(payload)
    print "data_src::", data_src,'payload',payload
    print type(payload),header_src,type(req.GET['url']),'_____________________'
    response = requests.get(url=req.GET['url'], params=payload['data'],headers=header_src)
    print response.text
    return response.text,data_src,req_type


def xxd_request_delete(req,mock_pro_id,req_type):
    prc = Request.objects.get(id=mock_pro_id)
    print '开始调用xxd_request_delete'
    data_src, header_src = toolbox.reqGETDict(req.GET)
    print data_src,header_src
    payload = toolbox.xxdData(data_src)
    payload = toolbox.str_dic(payload)
    print 'url组装开始',payload['data']
    url=toolbox.delete_url(payload['data'],req.GET['url'])
    response=requests.delete(url,headers=header_src)
    print response.text,url,'_______________'
    return  response.text,url

@toolbox.xxd_reqLog("")
def xxd_request(req,mock_pro_id,req_type):
    print "开始调用xxd_request接口:",
    print req.GET
    data_src, header_src ,file_src = toolbox.reqGETDict(req.GET)
    # data_src=toolbox.data_nest(data_src)
    # print 'header_src$$$$$$$$$$$$$$$$$',header_src,type(header_src)
    payload = toolbox.xxdData(data_src)
    print "%%%%%%%",file_src,len(file_src),header_src
    if len(file_src)==0:
        response = requests.request(req_type, req.GET['url'], data=payload, headers=header_src)
    else:
        # file_src=toolbox.xxdFile(file_src)
        print file_src
        print type(payload),type(file_src),type(header_src)
        response = requests.request(req_type, req.GET['url'],files=file_src, headers=header_src)
    return response.text,data_src,req_type

#The interface calls the container, which calls the request.
def xxd_request_vessel(req,mock_pro_id,req_type):
    text,data_src = xxd_request(req,mock_pro_id,req_type)
    context = {"text": str(text), "data_src": str(data_src)}
    return render(req,'mock_pro/requestShow.html', context)


#入参为多条请求组合的LIST， return 正确，失败，总长度，时间LIST


#Send a bunch of POST
def post_batch_ok(req,mock_pro_id):
    data_src=toolbox.reqGETDict(req.GET,"no normal")[0]#页面内容转为字典，直接DICT会造成u''的问题 后面的参数是为了暂缓进行加签
    TimesOfRepetition = int(req.GET['TimesOfRepetition']) #获取次数
    VUserNum = int(req.GET['VUserNum'])
    start = time.time()
    data_list=[]
    res_list=[0,0,0,threading.Lock()]
    for i in range(TimesOfRepetition):
        data = toolbox.requestDict(data_src,"dict") #进行数据整理 !.!类型数据生成
        # data = toolbox.signCreater(data,{'sign':req.GET['sign']}) #进行加签操作
        data = urllib.urlencode(data)#GET拼接
        data_list.append(data)
    threads = []
    if VUserNum==1:#单一用户就发一组
        toolbox.post_more(req.GET['url'],data_list,1,res_list)
    else:#发N组
        for i in range(VUserNum):
            exec "t%d = threading.Thread(target=toolbox.post_more,args=(req.GET['url'],data_list,1,res_list))"%i
            exec "threads.append(t%d)"%i
        for t in threads:
            t.setDaemon(True)
            t.start()
            t.join()
        time.sleep(1)#有可能丢包，再说
    end = time.time()-start
    #以下内容是通过pylab生成image后，再显示到页面
    #绘图
    # nowtime = datetime.datetime.now().strftime("%Y-%m-%d%H%M%S")
    # res = toolbox.drawDateReady(res_list[4:])
    # toolbox.drawChart_Xs(res[0],res[2],res[3],'static/png/'+nowtime+'Result')
    # toolbox.drawChart_X(res[1],res[2],res[4],'static/png/'+nowtime+'Amountofdata')
    #
    #记LOG
    # toolbox.logInsert(req.GET['url'],res_list[4:],'POST', #URL，DATA,TYPE
    #                   Request.objects.get(id=mock_pro_id).name,str(res_list[2]), #NAME
    #                   Request.objects.get(id=mock_pro_id),str(end),str("pass:"+str(res_list[0])+" error:"+str(res_list[1])))#RESPONSE,LEN,TIME
    # #return HttpResponse("pass:"+str(res_list[0])+" error:"+str(res_list[1]),'1')#"pass:"+str(ok)+" error:"+str(error)
    # context={'res':"pass:"+str(res_list[0])+" error:"+str(res_list[1]),'imgs':['/static/png/'+nowtime+'Result.png','/static/png/'+nowtime+'Amountofdata.png']}
    # return render(req,'mock_pro/showBatchRes.html',context)
    #这里是通过highchar生成动态图表
    Requset_list = toolbox.drawDateReady(res_list[4:])
    Requset_list = toolbox.hcharDateReady(Requset_list)
    context = {'pass_list':Requset_list[0],'error_list':Requset_list[1],'data_list':Requset_list[2],'rang_1':Requset_list[3],'rang_2':Requset_list[4]}
    return render(req,'mock_pro/showBatchRes.html',context)

#get
def get_ready(req,mock_pro_id):
    print "开始调用get_ready",req
    mock_pro_id=mock_pro_id
    prc = Request.objects.get(id=mock_pro_id)
    print 'prc.url',prc.url,type(prc.url)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    temp = toolbox.requestDict(temp)
    prc.url=toolbox.get_url_pro(prc.url,temp)
    # data = temp[0]
    # header = temp[1]
    text=""
    data_src=""
    try:
        text, data_src = xxd_request2(req, mock_pro_id, prc.type)
    except:
        print "GET SOLO"
    context = {'url':prc.url,'data':temp,'name':prc.name,'text':str(text),'data_src':str(data_src)}
    print '开始调用get_ready的context',context
    return render(req,'mock_pro/post_sub.html',context)

#delete
def delete_ready(req,mock_pro_id):
    print "开始调用delete_ready",req,req.GET
    mock_pro_id=mock_pro_id
    prc = Request.objects.get(id=mock_pro_id)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    temp = toolbox.requestDict(temp)
    print 'temp',temp,prc.url
    data_src, header_src = toolbox.reqGETDict(req.GET)
    # prc.url=toolbox.delete_url(data_src,prc.url)
    text=""
    url=""
    try:
        text ,url= xxd_request_delete(req, mock_pro_id, prc.type)

    except:
        print "GET SOLO"
    context = {'url': prc.url, 'data': temp, 'name': prc.name, 'text': str(text), 'data_src': 'data_src'}
    print '开始调用get_ready的context',context
    return render(req,'mock_pro/post_sub.html',context)
def get_batch_ready(req,mock_pro_id):
    prc = Request.objects.get(id=mock_pro_id)
    temp = Request_Data.objects.filter(f_key=mock_pro_id)
    data = toolbox.requestDict(temp,"batch")#不进行数据预处理
    context = {'url':prc.url,'data':data,'name':prc.name}
    return render(req,'mock_pro/get_batch_sub.html',context)
def get_ok(req,mock_pro_id):
    data_src=toolbox.reqGETDict(req.GET)[0]#页面内容转为字典，直接DICT会造成u''的问题
    data = urllib.urlencode(data_src)#GET拼接
    url = req.GET['url']+"?"+data
    start = time.time()
    req_temp = urllib2.Request(url)
    res_data = urllib2.urlopen(req_temp)
    end = time.time()-start
    res = res_data.read()
    toolbox.logInsert(req.GET['url'],url.split('?')[1],'GET',
                      Request.objects.get(id=mock_pro_id).name,res,
                      Request.objects.get(id=mock_pro_id),str(end),str(len(res)))
    return HttpResponse(res)
def get_batch_ok(req,mock_pro_id):
    data_src=toolbox.reqGETDict(req.GET,"no normal")[0]#页面内容转为字典，直接DICT会造成u''的问题 后面的参数是为了暂缓进行加签
    TimesOfRepetition = req.GET['TimesOfRepetition'] #获取次数
    VUserNum = req.GET['VUserNum']
    ok=error=sum_res=0
    start = time.time()
    for i in range(int(TimesOfRepetition)):
        data = toolbox.requestDict(data_src,"dict") #进行数据整理 !.!类型数据生成
        data = toolbox.signCreater(data,{'sign':req.GET['sign']}) #进行加签操作
        data = urllib.urlencode(data)#GET拼接
        url = req.GET['url']+"?"+data
        try:
            req_temp = urllib2.Request(url)
            res_data = urllib2.urlopen(req_temp)
            res = res_data.read()
            sum_res += len(res)
            ok +=1
            #这里要做个结果判断的
        except:
            error +=1
    end = time.time()-start
    toolbox.logInsert(req.GET['url'],str(TimesOfRepetition),'GET',
                      Request.objects.get(id=mock_pro_id).name,str(sum_res),
                      Request.objects.get(id=mock_pro_id),str(end),str("pass:"+str(ok)+" error:"+str(error)))
    return HttpResponse("pass:"+str(ok)+" error:"+str(error))






def get_title():
    person_list = Person.objects.all()
    print person_list
