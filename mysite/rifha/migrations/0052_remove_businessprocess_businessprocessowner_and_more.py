# Generated by Django 4.1.7 on 2023-06-24 16:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0051_alter_businessprocess_businessprocessowner"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="businessprocess",
            name="businessProcessOwner",
        ),
        migrations.AddField(
            model_name="businessprocess",
            name="businessProcessOwner",
            field=models.ManyToManyField(to="rifha.staff"),
        ),
    ]
