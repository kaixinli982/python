# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_pro', '0010_request_sign'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request_Unite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('backup_key', models.CharField(max_length=50)),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=1000, null=True)),
                ('f_key', models.ForeignKey(to='mock_pro.Request', null=True)),
            ],
        ),
    ]
