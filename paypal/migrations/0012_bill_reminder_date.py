# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0011_transaction_paykey_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='reminder_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
