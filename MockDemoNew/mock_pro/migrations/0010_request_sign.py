# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_pro', '0009_auto_20160708_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='sign',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
