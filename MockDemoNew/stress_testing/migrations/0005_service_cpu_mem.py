# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stress_testing', '0004_auto_20170810_1643'),
    ]

    operations = [
        migrations.CreateModel(
            name='service_cpu_mem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('serialmum', models.CharField(max_length=30)),
                ('time', models.DateTimeField()),
                ('cpu', models.FloatField()),
                ('mem', models.FloatField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
