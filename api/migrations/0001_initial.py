# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_id', models.CharField(max_length=256)),
                ('access_date', models.DateTimeField(verbose_name=b'date accessed')),
                ('action', models.CharField(max_length=100)),
                ('user_id', models.CharField(max_length=100)),
                ('command', models.CharField(max_length=512)),
            ],
        ),
    ]
