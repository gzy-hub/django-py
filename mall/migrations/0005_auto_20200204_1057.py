# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2020-02-04 02:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mall', '0004_auto_20200204_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classify',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='mall.Classify'),
        ),
    ]