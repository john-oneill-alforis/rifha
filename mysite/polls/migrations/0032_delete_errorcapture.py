# Generated by Django 4.1.7 on 2023-04-22 16:51

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0031_errorcapture"),
    ]

    operations = [
        migrations.DeleteModel(
            name="errorCapture",
        ),
    ]
