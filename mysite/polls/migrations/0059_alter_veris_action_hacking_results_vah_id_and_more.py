# Generated by Django 4.1.7 on 2023-05-07 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0058_rename_notes_veris_action_hacking_results_results_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="veris_action_hacking_results",
            name="vah_Id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.veris_action_hacking",
            ),
        ),
        migrations.AlterField(
            model_name="veris_action_hacking_variety",
            name="vah_Id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.veris_action_hacking",
            ),
        ),
        migrations.AlterField(
            model_name="veris_action_hacking_vector",
            name="vah_Id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="polls.veris_action_hacking",
            ),
        ),
    ]