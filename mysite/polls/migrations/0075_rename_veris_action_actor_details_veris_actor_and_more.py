# Generated by Django 4.1.7 on 2023-05-07 16:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0074_alter_veris_action_physical_notes"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="veris_action_actor_details",
            new_name="veris_actor",
        ),
        migrations.RenameModel(
            old_name="veris_action_actor_variety",
            new_name="veris_actor_motive",
        ),
        migrations.RenameModel(
            old_name="veris_action_actor_origin",
            new_name="veris_actor_origin",
        ),
        migrations.RenameModel(
            old_name="veris_action_actor_motive",
            new_name="veris_actor_variety",
        ),
        migrations.RenameField(
            model_name="veris_actor_motive",
            old_name="variety",
            new_name="motive",
        ),
        migrations.RenameField(
            model_name="veris_actor_variety",
            old_name="motive",
            new_name="variety",
        ),
    ]
