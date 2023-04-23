# Generated by Django 4.1.7 on 2023-04-23 16:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0036_veris_incident_action_details_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorcapture",
            name="date",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 4, 23, 17, 35, 24, 322880)
            ),
        ),
        migrations.AlterField(
            model_name="veris_incident_action_details",
            name="incident_id",
            field=models.CharField(max_length=45, unique=True),
        ),
    ]
