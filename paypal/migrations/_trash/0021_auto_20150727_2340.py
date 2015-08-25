# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0020_remove_transaction_testje'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='amount',
            field=models.DecimalField(max_digits=100, decimal_places=2),
        ),
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
