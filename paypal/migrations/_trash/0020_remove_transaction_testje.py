# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0019_transaction_testje'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='testje',
        ),
    ]
