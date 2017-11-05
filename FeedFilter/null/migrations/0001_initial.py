# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 11:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='statistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_blocked', models.IntegerField(default=0)),
                ('sentiments', models.FloatField(default=0.5)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(blank=True, max_length=250, unique=True)),
                ('no_of_tags', models.IntegerField(default=0)),
            ],
        ),
    ]
