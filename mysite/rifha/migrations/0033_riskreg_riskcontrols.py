# Generated by Django 4.1.7 on 2023-06-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0032_controlcatalogue"),
    ]

    operations = [
        migrations.AddField(
            model_name="riskreg",
            name="riskControls",
            field=models.ManyToManyField(to="rifha.controlcatalogue"),
        ),
    ]