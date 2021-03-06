# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-02 17:49
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Case",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
                ("start_date", models.DateTimeField()),
                ("end_date", models.DateTimeField()),
                ("summary", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip_address", models.GenericIPAddressField()),
                ("date", models.DateTimeField()),
                ("subject", models.CharField(max_length=128)),
                ("description", models.TextField()),
                (
                    "score",
                    models.DecimalField(
                        decimal_places=2, default=None, max_digits=5, null=True
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("login", "Attempts to gain unauthorized access"),
                            ("malware", "Attempts to exploit software bugs"),
                            ("spam", "Unsolicited bulk email sending"),
                        ],
                        max_length=10,
                    ),
                ),
                ("report_date", models.DateTimeField()),
                ("external_reference", models.CharField(max_length=128)),
                (
                    "case",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="events.Case",
                    ),
                ),
            ],
        ),
    ]
