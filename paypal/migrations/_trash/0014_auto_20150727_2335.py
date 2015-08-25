# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0013_auto_20150727_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='paykey_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 27, 21, 35, 2, 723219, tzinfo=utc)),
        ),
    ]
