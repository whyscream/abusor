# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-02 20:54
from __future__ import unicode_literals

import datetime

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="case", name="summary"),
        migrations.AddField(
            model_name="case", name="description", field=models.TextField(blank=True)
        ),
        migrations.AddField(
            model_name="case",
            name="subject",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name="case", name="end_date", field=models.DateTimeField(blank=True)
        ),
        migrations.AlterField(
            model_name="case",
            name="start_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="event",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("login", "Attempts to gain unauthorized access"),
                    ("malware", "Attempts to exploit software bugs"),
                    ("spam", "Unsolicited bulk email sending"),
                ],
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="event", name="description", field=models.TextField(blank=True)
        ),
        migrations.AlterField(
            model_name="event",
            name="external_reference",
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name="event",
            name="report_date",
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name="event",
            name="score",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]
