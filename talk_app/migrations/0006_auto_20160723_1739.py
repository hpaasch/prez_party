# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-23 17:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk_app', '0005_auto_20160723_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('candidate', models.CharField(max_length=30)),
                ('party', models.CharField(max_length=3)),
                ('total', models.FloatField()),
                ('contribution_count', models.IntegerField()),
                ('state', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ZIPFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=30)),
                ('candidate', models.CharField(max_length=30)),
                ('party', models.CharField(max_length=3)),
                ('total', models.FloatField()),
                ('contribution_count', models.IntegerField()),
                ('zip_code', models.IntegerField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Finance',
            new_name='USFinance',
        ),
    ]
