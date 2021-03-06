# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 20:01
from __future__ import unicode_literals

import ipaddress

from django.db import migrations

import abusor.events.fields


def move_ipnetwork_data(apps, schema_editor):
    """Populate the ip_network field based on the existing old data."""
    Case = apps.get_model("events", "Case")  # noqa
    for case in Case.objects.all():
        network_str = case.ip_address
        if case.netmask:
            network_str += "/" + case.netmask
        case.ip_network = ipaddress.ip_network(network_str, strict=False)
        case.save()


class Migration(migrations.Migration):

    dependencies = [("events", "0005_case_netmask")]

    operations = [
        migrations.AddField(
            model_name="case",
            name="ip_network",
            field=abusor.events.fields.GenericIPNetworkField(default="0.0.0.0/0"),
            preserve_default=False,
        ),
        migrations.RunPython(move_ipnetwork_data),
        migrations.RemoveField(model_name="case", name="ip_address"),
        migrations.RemoveField(model_name="case", name="netmask"),
    ]
