# Generated by Django 4.1.7 on 2023-06-14 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0016_assets_assetclassification"),
    ]

    operations = [
        migrations.RenameField(
            model_name="assetstypes",
            old_name="assetId",
            new_name="assetTypeId",
        ),
    ]
