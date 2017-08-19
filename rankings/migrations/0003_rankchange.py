# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-19 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rankings', '0002_group_admins'),
    ]

    operations = [
        migrations.CreateModel(
            name='RankChange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('before', models.FloatField()),
                ('after', models.FloatField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rankings.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rankings.Player')),
            ],
        ),
    ]
