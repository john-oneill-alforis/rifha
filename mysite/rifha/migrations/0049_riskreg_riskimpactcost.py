# Generated by Django 4.1.7 on 2023-06-25 11:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0048_alter_businessprocess_businessprocessowner"),
    ]

    operations = [
        migrations.AddField(
            model_name="riskreg",
            name="riskImpactCost",
            field=models.FloatField(default=5000.0),
            preserve_default=False,
        ),
    ]
