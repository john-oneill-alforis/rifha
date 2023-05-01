# Generated by Django 4.1.7 on 2023-05-01 15:02

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="staff",
            fields=[
                (
                    "staffId",
                    models.UUIDField(
                        auto_created=True, primary_key=True, serialize=False
                    ),
                ),
                ("firstName", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                ("contactNUmber", models.CharField(max_length=100)),
            ],
        ),
    ]
