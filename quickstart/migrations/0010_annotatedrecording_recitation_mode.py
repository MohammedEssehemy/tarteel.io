# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-09-01 18:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quickstart', '0009_demographicinformation_qiraah'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotatedrecording',
            name='recitation_mode',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
