# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(max_digits=100, decimal_places=2)),
                ('status', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('paykey', models.CharField(default=b'', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(max_digits=100, decimal_places=2)),
                ('status', models.CharField(max_length=10)),
                ('paykey', models.CharField(default=b'', max_length=200)),
                ('bill', models.ForeignKey(to='paypal.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=70)),
                ('validated', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(to='paypal.User'),
        ),
        migrations.AddField(
            model_name='bill',
            name='user',
            field=models.ForeignKey(to='paypal.User'),
        ),
    ]
