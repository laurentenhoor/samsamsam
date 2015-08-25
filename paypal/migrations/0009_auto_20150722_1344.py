# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0008_auto_20150722_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='paykey',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='paykey',
            field=models.CharField(default=b'', max_length=200, blank=True),
        ),
    ]
