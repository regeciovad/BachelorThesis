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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('char', models.CharField(verbose_name='Nonterminal', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('left_side', models.CharField(verbose_name='Left side', max_length=1)),
                ('right_side', models.CharField(verbose_name='Right side', max_length=42)),
            ],
        ),
        migrations.CreateModel(
            name='Terminal',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('char', models.CharField(verbose_name='Terminal', max_length=1)),
            ],
        ),
    ]
