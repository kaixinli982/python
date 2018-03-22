from django.db import models

# Create your models here.

class idcard_city_code(models.Model):

    privince=models.CharField(max_length=30)
    city=models.CharField(max_length=30)
    area=models.CharField(max_length=30)
    code=models.CharField(max_length=30)

    def  __unicode__(self):
        return self.privince

class card_bin(models.Model):
    bankname=models.CharField(max_length=30)
    bincode=models.CharField(max_length=30)
    banktype=models.IntegerField()

    def __unicode__(self):
        return self.bankname