# Generated by Django 4.1.7 on 2023-06-15 10:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0021_alter_assets_assetid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assets",
            name="assetDescription",
            field=models.TextField(max_length=1000),
        ),
        migrations.CreateModel(
            name="riskReg",
            fields=[
                (
                    "riskId",
                    models.CharField(
                        auto_created=True,
                        default=uuid.uuid4,
                        max_length=36,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("riskRef", models.CharField(max_length=100)),
                ("riskDescription", models.TextField(max_length=2000)),
                ("riskCreationDate", models.DateField()),
                ("riskReviewDate", models.DateField()),
                (
                    "riskOwner",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="rifha.staff",
                    ),
                ),
            ],
        ),
    ]