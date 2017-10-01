# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_datainfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='datainfo',
            name='owner',
            field=models.CharField(default='admin', max_length=256),
            preserve_default=False,
        ),
    ]
