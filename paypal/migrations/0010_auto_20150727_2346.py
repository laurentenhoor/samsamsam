# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0009_auto_20150722_1344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(max_digits=10, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='bill',
            name='paykey',
            field=models.CharField(default=b'', max_length=40, blank=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='paykey',
            field=models.CharField(default=b'', max_length=40, blank=True),
        ),
    ]
