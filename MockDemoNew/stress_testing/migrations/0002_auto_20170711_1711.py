# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stress_testing', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=200)),
                ('kind', models.CharField(default='KIND_CHOICES[0]', max_length=20, choices=[('Pyhton', 'Pyhton'), ('money', 'money'), ('paper', 'paper')])),
                ('user_name', models.CharField(default='jack', max_length=20)),
            ],
        ),
        migrations.DeleteModel(
            name='stress_result',
        ),
    ]
