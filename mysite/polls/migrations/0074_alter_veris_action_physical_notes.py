# Generated by Django 4.1.7 on 2023-05-07 16:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0073_rename_vae_id_veris_action_environmental_vaenv_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="veris_action_physical",
            name="notes",
            field=models.CharField(max_length=3000, null=True),
        ),
    ]
