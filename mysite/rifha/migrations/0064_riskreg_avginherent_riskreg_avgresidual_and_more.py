# Generated by Django 4.1.7 on 2023-07-09 09:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0063_riskreg_riskassessmentstatus_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="riskreg",
            name="avgInherent",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="riskreg",
            name="avgResidual",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="riskreg",
            name="maxInherent",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="riskreg",
            name="maxResidual",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="riskreg",
            name="minInherent",
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name="riskreg",
            name="minResidual",
            field=models.FloatField(default=0.0),
        ),
    ]