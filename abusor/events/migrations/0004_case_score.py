# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-21 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0003_alter-datetime-fields")]

    operations = [
        migrations.AddField(
            model_name="case",
            name="score",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        )
    ]
