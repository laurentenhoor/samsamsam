# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0017_transaction_paykey_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='paykey_date',
        ),
    ]
