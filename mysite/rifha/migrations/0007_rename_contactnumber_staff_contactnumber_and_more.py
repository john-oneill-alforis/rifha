# Generated by Django 4.1.7 on 2023-05-01 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0006_assetstypes_processes_assets"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staff",
            old_name="contactNUmber",
            new_name="contactNumber",
        ),
        migrations.AlterField(
            model_name="staff",
            name="jobTitle",
            field=models.ForeignKey(
                default="040f8643-2c82-46b3-9cd4-6e095b74b9f9",
                on_delete=django.db.models.deletion.CASCADE,
                to="rifha.staffrole",
            ),
        ),
    ]
