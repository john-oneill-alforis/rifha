# Generated by Django 4.1.7 on 2023-03-19 07:38

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0023_remove_trainingcorpus_classificationtext"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="trainingcorpus",
            name="textLabel",
        ),
    ]
