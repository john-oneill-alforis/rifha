# Generated by Django 4.1.7 on 2023-06-14 21:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0020_alter_assets_assetclassification_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="assets",
            name="assetId",
            field=models.CharField(
                auto_created=True,
                default=uuid.uuid4,
                max_length=36,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]