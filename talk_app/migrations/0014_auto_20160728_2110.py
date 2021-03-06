# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 21:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk_app', '0013_video_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='survey',
            old_name='changed',
            new_name='what_changed',
        ),
        migrations.RenameField(
            model_name='survey',
            old_name='chose',
            new_name='who_choose',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='discussion_level',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='top_area',
        ),
        migrations.AddField(
            model_name='survey',
            name='discussion_intensity',
            field=models.CharField(choices=[(('Deep',), 'Deep'), (('Medium',), 'Medium'), (('Shallow',), 'Shallow')], default=('Medium',), max_length=40),
        ),
        migrations.AddField(
            model_name='survey',
            name='top_topic',
            field=models.CharField(choices=[(('Values',), 'Values'), (('Policy',), 'Policy'), ('Personal qualities', 'Personal qualities')], default=('Policy',), max_length=40),
        ),
    ]
