# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0014_auto_20150727_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='paykey_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
