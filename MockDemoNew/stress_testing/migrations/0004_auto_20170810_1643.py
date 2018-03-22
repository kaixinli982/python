# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stress_testing', '0003_stress_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stress_info',
            name='avg',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='failed',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='failed_rate',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='max',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='success',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='total',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='stress_info',
            name='tps',
            field=models.FloatField(),
        ),
    ]
