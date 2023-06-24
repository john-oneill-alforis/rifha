# Generated by Django 4.1.7 on 2023-06-24 11:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0041_rename_processeid_processcriticality_processecriticalityid"),
    ]

    operations = [
        migrations.RenameField(
            model_name="processcriticality",
            old_name="processeCriticalityId",
            new_name="processCriticalityId",
        ),
        migrations.AlterField(
            model_name="processes",
            name="processCriticality",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rifha.processcriticality",
            ),
        ),
    ]