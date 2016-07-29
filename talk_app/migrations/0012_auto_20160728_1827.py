# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 18:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('talk_app', '0011_candidate_twt_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='dinnerparty',
            name='video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='talk_app.Video'),
        ),
    ]