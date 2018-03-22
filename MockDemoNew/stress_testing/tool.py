# -*- coding: UTF-8 -*-
import os
import requests,json
import thread
import time,re
import datetime
import threading
import random,paramiko
from stress_testing import models

# Initialization data
total_use_time2=0
total_use_time1=0
max_time=0
pass_count=0
failed_count=0
#get front-end data
def get_request_data(req):
    type = req.GET['type']
    url = req.GET['url']
    header = req.GET['header']
    data = req.GET['data']
    thread_count = req.GET['thread_count']
    thread_count = req.GET['thread_count']
    cycles = req.GET['cycles']
    control_type = req.GET['control_type']
    ramup_time = req.GET['ramup_time']
    response_code = req.GET['response_code']
    delay = req.GET['delay']
    name = req.GET['name']
    serialnum = req.GET['serialnum']
    serviceIp = req.GET['serviceIp']
    serviceIp = eval(serviceIp)
    name = str(name)
    serialnum = str(serialnum)
    data = str(data)
    type = str(type)
    response_code = str(response_code)
    url = str(url)
    header = eval(header)
    thread_count = int(thread_count)
    cycles = int(cycles)
    control_type = int(control_type)
    delay = int(delay)
    ramup_time = int(ramup_time)
    return thread_count, cycles, delay, control_type, url, type, header, data, response_code,ramup_time,serialnum,name,serviceIp

#sql
def sql_select_interface(serialmum):
    item=models.stress_info.objects.filter(serialmum=serialmum)
    test_result={}
    for object in item:
        test_result['total_request'] =object.total
        test_result['pass_count'] =object.success
        test_result['failed_count'] = object.failed
        test_result['failed_rate'] = object.failed_rate
        max_time = round(object.max, 2)
        test_result['max_time'] = max_time
        test_result['avg_time'] = object.avg
        test_result['tps'] = object.tps
    return test_result
def sql_select_service_cpu_mem(serialmum):
    time=[]
    cpu=[]
    mem=[]
    total_record=  models.service_cpu_mem.objects.filter(serialmum=serialmum).values('serialmum','create_time','cpu','mem')
    if len(total_record)>0:
        for i in total_record:
            i['create_time']=str(i['create_time'])

        return list(total_record)
    else:
        print '服务监控没有数据！'

def sql_cpumem_insert_or_update(serialmum,data):
    item=models.service_cpu_mem.objects.filter(serialmum=serialmum).count()
    print 'item',item
    print 'data',data
    if item==0:
        models.service_cpu_mem.objects.create(**data)
        print 'cpu inset success'
    else:
        models.service_cpu_mem.objects.filter(serialmum=serialmum).count()


def sql_insert_update(serialmum,data,name):
    item=models.stress_info.objects.filter(serialmum=serialmum).count()
    if 0==item:
        print 'insert'
        models.stress_info.objects.create(serialmum=serialmum,name=name,**data)
        print 'ok'

    else:
        print 'update'
        models.stress_info.objects.filter(serialmum=serialmum).update(**data)

#Simulate shell input commands
def shell_cmd(cmd):
    for i in cmd:
        cmd.send(i + '\n')
        cmd.send("")

# deal server data
def server_data_handle(data):
    cpu=[]
    mem=[]
    Time=[]
    for item in data:
        cpu.append(item['cpu'])
        mem.append(item['mem'])
        Time.append(item['create_time'])
    return cpu,mem,Time
# assembly return data
def dict_to_json(result):
        result_tmp={}
        result_tmp['interface']=result[0]
        result_tmp['cpu'] = result[1]
        result_tmp['mem'] = result[2]
        result_tmp['Time'] = result[3]
        result_tmp=json.dumps(result_tmp)
        return result_tmp

#deal files
def file_read(filename):
    file_re = open(filename)
    result_data = file_re.readline()
    result_data = eval(result_data)
    file_re.close()
    return result_data
def file_write(filename,result):
    f = open(filename, 'w+')
    result = str(result)
    f.write(result)
    f.close()
def compare_size(end,max_time):
    if end > max_time :
        return end
    else:
        return  max_time

def assemble(total_request,pass_count,failed_count,failed_rate,max_time,avg_time,tps):
    result={}
    result['total'] = total_request
    result['success'] = pass_count
    result['failed'] = failed_count
    result['failed_rate'] = failed_rate
    max_time=round(max_time,2)
    result['max'] = max_time
    result['avg'] = avg_time
    result['tps'] = tps

    return result

#Single Instace
class singleton:
    def __init__(self,aClass):
        self.aClass = aClass
        self.instance = None
    def __call__(self,*args):
        if self.instance == None:
            self.instance = self.aClass(*args)
        return self.instance
@singleton
class RWLock(object):
    def __init__(self):
        self.wlock = threading.Lock()
    def write_acquire_wait(self):
        while True:
            if self.wlock.acquire():
                return True
    def write_release(self):
        self.wlock.release()

#request
def request(threadId,threadName,counter,url,type,header,data,response_code,delay=0):
    global pass_count,failed_count,max_time,total_use_time1,total_use_time2
    start=time.time()
    try:
        #
        if type == 'GET' or type== 'DELETE':
            response = requests.request(type, url, headers=header)

        else:
            applyCode1 =str(int(time.time()) * 1000) + str(random.randint(1, 9999))
            data = data.replace('$$$TIME', applyCode1)
            response = requests.request(type,url, data=data, headers=header)
        end = time.time() - start
        total_use_time1+=end
        max_time=compare_size(end,max_time)

        if response_code in response.text:
            pass_count+=1
        else:
            failed_count += 1
    except:
        end = time.time() - start
        total_use_time2 += end
        max_time=compare_size(end,max_time)
        failed_count+=1
    time.sleep(delay)

#thread
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self,  threadId,threadName,counter,delay,filename,control_type,url,type,header,data,response_code,serialnum,name):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.counter=counter
        self.threadName=threadName
        self.delay=delay
        self.filename=filename
        self.control_type=control_type
        self.url=url
        self.type=type
        self.header=header
        self.data=data
        self.response_code=response_code
        self.serialnum=serialnum
        self.name=name


    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        global flag_stop
        global condition
        i=0
        print 'self.counter:',self.counter
        while i< self.counter:
            if condition.acquire():
                request(self.threadId ,self.threadName,self.counter,self.url,self.type,self.header,self.data,self.response_code,self.delay)
                if self.control_type==0:
                    i =int(time.time()-tt)
                    flag_stop=int(time.time()-tt)
                    print '运行时间：',i,time.time(),tt
                else:
                    i+=1
                flag_stop+=1
                condition.notify()
                condition.release()
            #statistical
        lock = RWLock()
        total_request=pass_count+failed_count
        TT = time.time() - tt
        total_use_time=total_use_time1+total_use_time2
        tps=round((total_request/TT),2)
        failed_rate=round((float(failed_count)/float(total_request)*100),2)
        avg_time=round((total_use_time/total_request),2)
        # s= '最终结果PASS:'+str(pass_count)+'\t'+'failed:'+str(failed_count)+'\t'+'异常占比数:'+str(failed_rate)+'%'+'\t'+'总请求数:'+str(total_request)+'\t'+'tps:'+str(tps)+'\t'+'最长请求时长:'+str(max_time)+'\t'+'平均请求时长:'+str(avg_time)
        result=assemble(total_request, pass_count, failed_count, failed_rate, max_time, avg_time, tps)
        if lock.write_acquire_wait():
            # file_write(self.filename, result)#写入文件
            #写入数据库
            sql_insert_update(self.serialnum,result,self.name)
            lock.write_release()

def jumtest(host, pkey, cpu_cmd, mem_cmd, filenaem,serialmum):
    global flag_stop, condition
    host = 'relay.xxd.com'
    pkey = 'C:\Users\guoxiaoli\Downloads\guoxiaoli'
    key = paramiko.RSAKey.from_private_key_file(pkey)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username="guoxiaoli", password="******", pkey=key)
    channel = ssh.invoke_shell()
    channel.settimeout(10)
    channel1 = ssh.invoke_shell()
    channel1.settimeout(10)
    shell_cmd(cpu_cmd)
    shell_cmd(mem_cmd)
    count = 0
    # file = open(filenaem, 'w')
    while flag_stop:
        print 'flag_stop',flag_stop
        if condition.acquire():
            if count < 5:
                try:
                    output = channel.recv(2024)
                    output1 = channel1.recv(2024)
                except:
                    print "error!!!!"
                    pass
            else:
                try:
                    output = channel.recv(2024)
                    output1 = channel1.recv(2024)
                    output_cpu = output.split("\r\n")
                    output_mem = output1.split("\r\n")
                    new_cpu = []
                    for i in output_cpu:
                        if len(i) > 1:
                            new_cpu.append(i)
                    # 获取cpu,men
                    cpu_list = re.findall("(\d*.\d*)%\w+", new_cpu[2])
                    total_mem = re.split("[ ]+", output_mem[1])
                    used_mem = re.split("[ ]+", output_mem[2])
                    men_per = round((float(used_mem[2]) / float(total_mem[1]) * 100), 2)
                    Time = str(datetime.datetime.now())
                    # file.write(Time + ',' + str(cpu_list[0]) + ',' + str(men_per) + '\n')#写入文件
                    #写入数据库
                    models.service_cpu_mem.objects.create(serialmum=serialmum,cpu=float(cpu_list[0]),mem=float(men_per),time=Time)
                except:
                    print "开小差了"
            flag_stop-=1
            condition.notify()
            condition.release()
        count += 1
        print count
    # file.close()

class myMonitorThreads(threading.Thread):
    def __init__(self, host, pkey, cpu_cmd, mem_cmd, filename,serialmum):
        threading.Thread.__init__(self)
        self.host = host
        self.pkey = pkey
        self.cpu_cmd = cpu_cmd
        self.mem_cmd = mem_cmd
        self.filename = filename
        self.serialmum=serialmum
        global flag_stop

    def run(self):
        try:
            jumtest(self.host, self.pkey, self.cpu_cmd, self.mem_cmd, self.filename,self.serialmum)
        except:
            print 'Stop monitoring'


#Single interface pressure measurement
def thread_config(threadcount,counter,delay,control_type,url,type,header,data,response_code,ramup_time,serialnum,interfacename,serviceIp):
    global pass_count,failed_count,max_time,total_use_time1,total_use_time2,tt
    global condition,flag_stop
    flag_stop=counter+10
    cpu_cmd=serviceIp+["top -bi  -d 1"]
    mem_cmd=serviceIp+["free -m  -s 1"]
    condition = threading.Condition()
    pass_count, failed_count, max_time, total_use_time1, total_use_time2, tt = [0, 0, 0, 0, 0, time.time()]
    # create thread
    threads = []
    name=time.strftime("%Y-%d-%m-%H_%M_%S")
    filename=name+'single.txt'
    threads.append(myMonitorThreads('relay.xxd.com', 'C:\Users\guoxiaoli\Downloads\guoxiaoli', cpu_cmd, mem_cmd, filename,serialnum))
    for i in range(threadcount):

        threads.append(myThread(i,str(i),counter,delay,filename,control_type,url,type,header,data,response_code,serialnum,interfacename))
    postpone=round(float(ramup_time)/float(threadcount),2)
    #start thread
    for i in range(threadcount+1):
        if i==0:
            threads[i].start()
            time.sleep(10)
        else:
            threads[i].start()
            time.sleep(postpone)
    #main thread ends after the child thread ends.
    for t in threads:
        t.join()
    data_interface=sql_select_interface(serialnum)#从数据库中获取

    # result_data=file_read(filename)#从文件中获取
    result_data=data_interface
    cpu_mem_data=sql_select_service_cpu_mem(serialnum)
    #deal server data
    cpu,mem,Time=server_data_handle(cpu_mem_data)
    return result_data,cpu,mem,Time

