# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0015_auto_20150727_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='paykey_date',
        ),
    ]
