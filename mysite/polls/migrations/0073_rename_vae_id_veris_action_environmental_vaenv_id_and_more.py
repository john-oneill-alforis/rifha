# Generated by Django 4.1.7 on 2023-05-07 16:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0072_veris_action_environmental_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="veris_action_environmental",
            old_name="vae_Id",
            new_name="vaenv_Id",
        ),
        migrations.RenameField(
            model_name="veris_action_environmental_variety",
            old_name="vae_Id",
            new_name="vaenv_Id",
        ),
    ]