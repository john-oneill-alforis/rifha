# Generated by Django 4.1.7 on 2023-03-17 21:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0017_alter_trainingcorpus_entryid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trainingcorpus",
            name="entryId",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]