# Generated by Django 4.1.7 on 2023-04-24 17:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0038_alter_errorcapture_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorcapture",
            name="date",
            field=models.DateField(
                blank=True, default=datetime.datetime(2023, 4, 24, 18, 56, 34, 726929)
            ),
        ),
    ]