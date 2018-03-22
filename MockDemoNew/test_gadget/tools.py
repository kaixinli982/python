# -*- coding: UTF-8 -*-
from test_gadget import models
import random,datetime,cx_Oracle,paramiko,time
from django.db import connection

def sql_select_city(province):
    total_record=  models.idcard_city_code.objects.filter(privince__contains=province).values('city').distinct()
    if len(total_record)>0:

        return list(total_record)
    else:
        print '查询city出错了！'

def sql_select_area(province,city):
    print province,city
    total_record=  models.idcard_city_code.objects.filter(privince__contains=province,city=city).values('area').distinct()
    if len(total_record)>0:

        return list(total_record)
    else:
        print '查询area出错了！'

def sql_select_code(province,city,area):
    code=models.idcard_city_code.objects.filter(privince__contains=province,city=city,area=area).values('code').distinct()
    code=code[0]['code']
    return code

def check_city_code(code):
    count = models.idcard_city_code.objects.filter(code=code).count()
    return count
def check_birth_date(date):
    y=int(date[:4])
    m=int(date[4:6])
    d=int(date[6:])
    try:
        datetime.date(int(y),int(m),int(d))
        return True
    except:
        return False
#生成生份证
# S= Sum(Ai*Wi)  mod 11
# S：0  1  2  3  4  5  6  7  8  9  10
# Y：1  0  X  9  8  7  6  5  4  3  2
#生成校验码
def check_code(Ai):
    print 'Ai',Ai
    mapping={'0':1,'1':0,'2':'X','3':9,'4':8,'5':7,'6':6,'7':5,'8':4,'9':3,'10':2}
    Wi=[7 ,9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2,]
    # Ai=[3,2,1,2,8,1,1,9,9,0,1,0,0,9,4,2,2]
    sum=0
    for i in range(len(Ai)):
        sum+=Wi[i]*Ai[i]
    s=sum%11
    s=str(s)
    return mapping[s]

def id_assemble(code,year,month,day,sex):
    #顺序号
    Serial_number=random.randint(10,99)
    #性别
    if sex=='男':
        sexcode=random.randrange(1,9,2)
    else:
        sexcode = random.randrange(0, 8, 2)
    #身份证随机生成
    id=str(code)+str(year)+str(month)+str(day)+str(Serial_number)+str(sexcode)
    id_tmp =list(id)
    for i in range(len(id)):
        id_tmp[i]=int(id_tmp[i])
    id=str(id)+str(check_code(id_tmp))
    return id


def generate_banecard(bin,flag):
    cradnum = str(bin) + str(random.randint(1000000000000, 9999999999999))
    while flag:
        cradnum = str(bin) + str(random.randint(1000000000000, 9999999999999))
        tmp = list(cradnum)
        tmp = tmp[::-1]
        print 'flag',flag
        oddlist=[]
        evenlist=[]
        oddsum=0
        evensum=0
        for i in range(len(tmp)):
            if i%2==0:
                oddlist.append(tmp[i])
            else:
                evenlist.append(tmp[i])
        print oddlist,evenlist
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
            flag=False
    print cradnum
    return cradnum

def connectDb():
    # conn = cx_Oracle.connect("xxd_stage", "Bb919189", "192.168.31.225:1521/oragbst")
    conn = cx_Oracle.connect("autotest", "At618ikb", "192.168.34.10:1521/v6train")

    cursor = conn.cursor()
    return cursor
def userid_strip(userid_list):
    userid_list = userid_list.strip('\n')
    userid_list = userid_list.strip(' ')
    return userid_list

#连接shell
def shell_connect():
    host = 'relay.xxd.com'
    pkey = 'C:\Users\guoxiaoli\Downloads\guoxiaoli'
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username="guoxiaoli", password="******", pkey=key)
    channel = ssh.invoke_shell()
    channel.settimeout(10)
    return channel

def shell_send(channel,cmd):
    for i in cmd:
        channel.send(i + '\n')
        channel.send("")
#事件获取环境处理
def envir_cmd_deal(envir):
    envir_cmd = ['1', 'a2', 'date']
    envir_list = {'stage': 'a5', 'test': 'a11', 'uat': 'a26', 'dev': 'a3'}
    envir_cmd[1] = envir_list[envir]
    return  envir_cmd
#时间格式转换
def time_format(str,format_original,format_tobe):
    timeArray = time.strptime(str, format_original)
    otherStyleTime = time.strftime(format_tobe, timeArray)
    return otherStyleTime