from django.shortcuts import render
import tools,apis
import time
from django.http import HttpResponse

# Create your views here.
def index(req):
    return render(req,'test_data/index.html')

def borrow_index(req):
    return render(req,'test_data/borrow.html')

def b_a_test(req):
    print 'test_________________'
    return HttpResponse('test_test')

def borrow_auto(req):
    req_data=tools.req_data_deal(req)
    print 'req_data',req_data
    data_interface_cor = tools.data_interface_correspondence()
    data = tools.request_data(req_data, data_interface_cor)
    a = apis.APIS(req_data["environment"])
    tmp_name = str(long(time.time() * 100))
    logfilename = tmp_name + 'test.log'
    resultname = tmp_name + 'result.txt'
    a.log_config(logfilename)
    print str(time.time()) + "_" * 300

    a.run(data, borrow_id="")
    # a.log_sort_out("152094678703test.log", "152101215143result.txt")
    # a.log_sort_out(logfilename, resultname)
    with open(logfilename, 'r') as f:
        logs = f.readlines()
        if len(logs) > 3:
            response_data=logs[3][-15:]
        else:
            response_data='failed'

    return HttpResponse(response_data)