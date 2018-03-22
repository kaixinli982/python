# -*- coding: UTF-8 -*-
from django.shortcuts import render
import datetime,random,time,math,json
from django.http import HttpResponse
import tools,paramiko,re
# Create your views here.

#check Card number
def check_bankcode(bankcard):

    tmp = list(bankcard)
    tmp = tmp[::-1]
    oddlist=[]
    evenlist=[]
    oddsum=0
    evensum=0
    for i in range(len(tmp)):
        if i%2==0:
            oddlist.append(tmp[i])
        else:
            evenlist.append(tmp[i])
    #奇数位
    for i in oddlist:
        oddsum+=int(i)
    #偶数位
    for i in evenlist:
        tmp_eve=int(i)*2
        if tmp_eve>=10:
            tmp_eve-=9
        evensum+=tmp_eve
    print oddsum,evensum
    if (oddsum+evensum)%10==0:
        return False
    else:
        return True
#Generate the card number
def generate_banecard(bin,type,flag=True):
    cradnum=0
    if type:
        while flag:
            cradnum = str(bin) + str(random.randint(1000000000000, 9999999999999))
            flag=check_bankcode(cradnum)
    else:
        while flag:
            cradnum = str(bin) + str(random.randint(1000000000, 9999999999))
            flag = check_bankcode(cradnum)

    return cradnum


def bankcard_index(req):
    return render(req,'test_gadget/Bankcard.html')

def banckcard_generate(req):
    card_bin=req.GET['carbin']
    card_type=req.GET['type']
    print card_bin,card_type
    bank_card=generate_banecard(card_bin,card_type)
    return HttpResponse(bank_card)


def index(req):
    return render(req,'test_gadget/index.html')

def idcard_index(req):
    print 'idcard_index'
    return render(req,'test_gadget/idcard.html')

def city_get(req):
    citys={}
    province=req.GET['province']
    citys['list']=tools.sql_select_city(province)

    return HttpResponse(json.dumps(citys))
def area_get(req):
    areas={}
    province=req.GET['province']
    city = req.GET['city']
    print 'city',city
    areas['list']=tools.sql_select_area(province,city)

    return HttpResponse(json.dumps(areas))

def generate_idcard(req):
    province = req.GET['province']
    city = req.GET['city']
    area = req.GET['area']
    year=req.GET['year']
    month = req.GET['month']
    day = req.GET['day']
    sex=req.GET['sex']
    count=req.GET['count']
    #获取区域code
    print '前台数据获取', province,city,area,year,month,day,sex,count
    #城市code获取
    code=tools.sql_select_code(province,city,area)
    idlist=[]
    for i in range(int(count)):
        id=tools.id_assemble(code, year, month, day, sex)
        idlist.append(id)
    print 'houtai',idlist
    return HttpResponse(json.dumps(idlist))
def id_check_index(req):
    print 'id_check_index'
    return render(req,'test_gadget/idcheck.html')
def id_check(req):
    id = req.GET['idnum']
    id_tmp =list(id[:-1])
    for i in range(len(id[:-1])):

        id_tmp[i]=int(id[i])
    id_legitimacy=[id]
    if tools.check_city_code(id[:6])>=1 and tools.check_birth_date(id[6:14]) and str(tools.check_code(id_tmp))==id[-1:]:
        id_legitimacy.append('true')
    else:
        id_legitimacy.append('false')
    return HttpResponse(json.dumps(id_legitimacy))


def useraccount_index(req):
    return render(req, 'test_gadget/user_account.html')
def user_account(req):
    userid_list=req.GET['userid']
    userid_list=tools.userid_strip(userid_list)
    cr=tools.connectDb()
    s="select sum(usable) from xinxindb.xxd_account where pcode='1001' and userid in "+str(eval(userid_list))
    cr.execute(s)
    data=cr.fetchone()
    cr.close()
    print data[0]
    return HttpResponse(json.dumps([data[0]]))

def servertime_index(req):
    return render(req,'test_gadget/servertime.html')

def servertime(req):
    envir=req.GET['environment']
    envir_cmd=tools.envir_cmd_deal(envir)
    print envir_cmd
    channel = tools.shell_connect()
    tools.shell_send(channel,envir_cmd)
    output = channel.recv(2024)
    tm = re.findall(r'Last login: (.*) from', output)
    otherStyleTime=tools.time_format(tm[0],"%a %b %d %H:%M:%S %Y","%Y/%m/%d %H:%M:%S")
    data={envir:otherStyleTime}
    print otherStyleTime
    return HttpResponse(json.dumps(data))