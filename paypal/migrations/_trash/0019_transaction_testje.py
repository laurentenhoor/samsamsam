# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0018_remove_transaction_paykey_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='testje',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
