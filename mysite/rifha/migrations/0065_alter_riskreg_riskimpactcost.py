# Generated by Django 4.1.7 on 2023-07-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0064_riskreg_avginherent_riskreg_avgresidual_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="riskreg",
            name="riskImpactCost",
            field=models.FloatField(default=0.0),
        ),
    ]