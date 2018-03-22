from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from operator import itemgetter
import json,tools
import hashlib
from django.shortcuts import HttpResponse
# Create your views here.

def index(request):
    return render(request,'md5/index.html')


def test2(request):
    a = request.GET.get('pass',"")
    salt = request.GET.get('salt',"")
    type=request.GET.get('type',"")
    a=str(a)
    salt=str(salt)
    type=str(type)
    result = tools.xxd_md5(a,type,salt)
    print result

    return HttpResponse(json.dumps(result))