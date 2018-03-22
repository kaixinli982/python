# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('test_gadget', '0002_car_bin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='car_bin',
            new_name='card_bin',
        ),
    ]
