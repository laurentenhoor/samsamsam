# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0010_transaction_paykey_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='paykey',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
