# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data_id', models.CharField(max_length=256)),
                ('data_type', models.CharField(max_length=256)),
                ('data_storage', models.CharField(max_length=256)),
                ('data_location', models.CharField(max_length=512)),
            ],
        ),
    ]
