# -*- coding :utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.
KIND_CHOICES=(
    (u'Pyhton',u'Pyhton'),
    (u'money',u'money'),
    (u'paper',u'paper'),
)
class Moment(models.Model):
    content = models.CharField(max_length=200)
    kind = models.CharField(max_length=20,choices=KIND_CHOICES,default='KIND_CHOICES[0]')
    user_name = models.CharField(max_length=20,default=u'jack')

class stress_info(models.Model):
    name=models.CharField(max_length=30)
    total=models.IntegerField()
    success=models.IntegerField()
    failed=models.IntegerField()
    failed_rate=models.FloatField()
    avg=models.FloatField()
    max=models.FloatField()
    tps=models.FloatField()
    serialmum=models.CharField(max_length=30)
    create_time=models.DateTimeField(auto_now_add=True)
    update_time=models.DateTimeField(auto_now =True)
    def __unicode__(self):
        return self.name

class service_cpu_mem(models.Model):
    serialmum=models.CharField(max_length=30)
    time=models.DateTimeField()
    cpu=models.FloatField()
    mem=models.FloatField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def  __unicode__(self):
        return self.serialmum