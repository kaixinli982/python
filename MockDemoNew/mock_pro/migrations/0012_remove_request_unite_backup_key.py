# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mock_pro', '0011_request_unite'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='request_unite',
            name='backup_key',
        ),
    ]
