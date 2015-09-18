# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nonterminal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('char', models.CharField(max_length=1, verbose_name='Nonterminal')),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('left_hand_side', models.CharField(max_length=1, verbose_name='Left hand side')),
                ('right_hand_side', models.CharField(max_length=42, verbose_name='Right hand side')),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('char', models.CharField(max_length=1, verbose_name='Terminal')),
            ],
        ),
    ]
