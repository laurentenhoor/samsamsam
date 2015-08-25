# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0007_auto_20150722_0817'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='transaction',
            name='hash',
            field=models.CharField(default=b'', max_length=10),
        ),
    ]
