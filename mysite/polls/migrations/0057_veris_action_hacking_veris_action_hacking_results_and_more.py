# Generated by Django 4.1.7 on 2023-05-07 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0056_remove_veris_action_actor_details_industry_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="veris_action_hacking",
            fields=[
                ("vah_Id", models.BigAutoField(primary_key=True, serialize=False)),
                ("incident_id", models.CharField(max_length=45)),
                ("cve", models.CharField(max_length=200)),
                ("notes", models.CharField(max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="veris_action_hacking_results",
            fields=[
                ("entry_Id", models.BigAutoField(primary_key=True, serialize=False)),
                ("notes", models.CharField(max_length=1000)),
                (
                    "vam_Id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.veris_action_malware",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="veris_action_hacking_variety",
            fields=[
                ("entry_Id", models.BigAutoField(primary_key=True, serialize=False)),
                ("variety", models.CharField(max_length=200)),
                ("name", models.CharField(max_length=200)),
                (
                    "vam_Id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.veris_action_malware",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="veris_action_hacking_vector",
            fields=[
                ("entry_Id", models.BigAutoField(primary_key=True, serialize=False)),
                ("vector", models.CharField(max_length=200)),
                (
                    "vam_Id",
                    models.ForeignKey(
                        default=1,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="polls.veris_action_malware",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="veris_action_details",
        ),
    ]
