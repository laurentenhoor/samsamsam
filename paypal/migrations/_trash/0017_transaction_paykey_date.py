# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0016_remove_transaction_paykey_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='paykey_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 27, 21, 37, 23, 98217, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
