# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 22:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talk_app', '0009_auto_20160725_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dinnerparty',
            old_name='name',
            new_name='party_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='friend_mix',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='friends',
        ),
        migrations.AddField(
            model_name='dinnerparty',
            name='friend_mix',
            field=models.CharField(choices=[('Democrat', 'Democrat'), ('Independent', 'Independent'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('GreenParty', 'GreenParty'), ('Mixed', 'Mixed')], default='Mixed', max_length=20),
        ),
        migrations.AddField(
            model_name='dinnerparty',
            name='friend_names',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='affiliation',
            field=models.CharField(choices=[('Democrat', 'Democrat'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('GreenParty', 'GreenParty')], max_length=20),
        ),
        migrations.AlterField(
            model_name='profile',
            name='affiliation',
            field=models.CharField(blank=True, choices=[('Democrat', 'Democrat'), ('Independent', 'Independent'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('GreenParty', 'GreenParty')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='registered',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='pundit',
            name='affiliation',
            field=models.CharField(choices=[('Democrat', 'Democrat'), ('Independent', 'Independent'), ('Republican', 'Republican'), ('Libertarian', 'Libertarian'), ('GreenParty', 'GreenParty')], max_length=20),
        ),
    ]
