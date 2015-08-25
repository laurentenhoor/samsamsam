# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0009_auto_20150722_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='paykey_date',
            field=models.DateTimeField(default=b'', blank=True),
        ),
    ]
