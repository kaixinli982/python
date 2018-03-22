# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stress_testing', '0002_auto_20170711_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='stress_info',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('total', models.IntegerField(max_length=30)),
                ('success', models.IntegerField(max_length=30)),
                ('failed', models.IntegerField(max_length=30)),
                ('failed_rate', models.FloatField(max_length=30)),
                ('avg', models.FloatField(max_length=30)),
                ('max', models.FloatField(max_length=30)),
                ('tps', models.FloatField(max_length=30)),
                ('serialmum', models.CharField(max_length=30)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
