# Generated by Django 4.1.7 on 2023-05-07 09:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0053_veris_actor_details_veris_action_actor_variety_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="veris_action_actor_motive",
            old_name="result",
            new_name="motive",
        ),
        migrations.RenameField(
            model_name="veris_action_actor_origin",
            old_name="result",
            new_name="origin",
        ),
        migrations.RenameField(
            model_name="veris_action_actor_variety",
            old_name="result",
            new_name="variety",
        ),
        migrations.AlterField(
            model_name="veris_incident_details",
            name="modified",
            field=models.DateField(),
        ),
        migrations.DeleteModel(
            name="veris_action_actor_notes",
        ),
    ]
