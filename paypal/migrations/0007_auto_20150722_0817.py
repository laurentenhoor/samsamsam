# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0006_auto_20150721_1921'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ['date']},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-last_used']},
        ),
    ]
