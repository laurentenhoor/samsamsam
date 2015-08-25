# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paypal', '0002_user_free_transactions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact', models.ForeignKey(related_name='user_contacts', to='paypal.User')),
                ('user', models.ForeignKey(related_name='main_user', to='paypal.User')),
            ],
        ),
    ]
