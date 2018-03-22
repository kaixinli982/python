# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_gadget', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='car_bin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bankname', models.CharField(max_length=30)),
                ('bincode', models.CharField(max_length=30)),
                ('banktype', models.IntegerField()),
            ],
        ),
    ]
