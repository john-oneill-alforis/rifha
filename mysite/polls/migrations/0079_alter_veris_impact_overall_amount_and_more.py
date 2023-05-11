# Generated by Django 4.1.7 on 2023-05-08 19:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0078_veris_impact_veris_impact_overall_rating_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="veris_impact",
            name="overall_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="veris_impact",
            name="overall_max_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="veris_impact",
            name="overall_min_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="veris_impact_loss",
            name="max_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="veris_impact_loss",
            name="min_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="veris_impact_loss",
            name="overall_amount",
            field=models.IntegerField(),
        ),
    ]