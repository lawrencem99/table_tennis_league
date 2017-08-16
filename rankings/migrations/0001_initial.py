# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-15 13:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('home_score', models.IntegerField(blank=True, null=True)),
                ('away_score', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the group name', max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ranking', models.FloatField(default=1000)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='players',
            field=models.ManyToManyField(blank=True, to='rankings.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(blank=True, related_name='games', to='rankings.Player'),
        ),
        migrations.AddField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winning_games', to='rankings.Player'),
        ),
        migrations.AddField(
            model_name='group',
            name='games',
            field=models.ManyToManyField(blank=True, to='rankings.Game'),
        ),
    ]
