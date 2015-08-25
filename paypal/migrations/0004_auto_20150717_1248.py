# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0003_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact',
            field=models.ForeignKey(related_name='user_contact', to='paypal.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=70),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together=set([('user', 'contact')]),
        ),
    ]
