# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='stress_result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('interface_name', models.CharField(max_length=200)),
                ('total', models.CharField(max_length=20)),
                ('success', models.CharField(max_length=20)),
                ('failed', models.CharField(max_length=20)),
                ('error_rate', models.CharField(max_length=20)),
                ('avg', models.CharField(max_length=20)),
                ('max', models.CharField(max_length=20)),
                ('tps', models.CharField(max_length=20)),
                ('image_path', models.CharField(max_length=200)),
            ],
        ),
    ]
