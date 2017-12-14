# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-04 12:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('null', '0002_blockedpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_id', models.CharField(blank=True, max_length=250, unique=True)),
                ('sentiments', models.FloatField(default=0.5)),
            ],
        ),
        migrations.DeleteModel(
            name='statistics',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='no_of_tags',
            new_name='no_of_post',
        ),
    ]