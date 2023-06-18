# Generated by Django 4.1.7 on 2023-06-17 06:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0031_remove_riskreg_riskref"),
    ]

    operations = [
        migrations.CreateModel(
            name="controlCatalogue",
            fields=[
                (
                    "controlId",
                    models.CharField(
                        auto_created=True,
                        default=uuid.uuid4,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("controlName", models.CharField(max_length=200)),
                ("controlCategory", models.CharField(max_length=200)),
                ("controlDescription", models.TextField(max_length=2000)),
            ],
        ),
    ]