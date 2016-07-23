# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-22 00:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk_app', '0002_auto_20160721_2304'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['created_at']},
        ),
        migrations.AddField(
            model_name='question',
            name='text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='changed',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='chose',
            field=models.TextField(blank=True, null=True),
        ),
    ]