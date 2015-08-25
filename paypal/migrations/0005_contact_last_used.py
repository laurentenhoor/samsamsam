# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0004_auto_20150717_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='last_used',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
