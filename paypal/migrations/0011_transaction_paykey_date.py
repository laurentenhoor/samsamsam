# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0010_auto_20150727_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='paykey_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
