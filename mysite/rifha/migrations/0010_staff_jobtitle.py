# Generated by Django 4.1.7 on 2023-06-13 11:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0009_remove_staff_jobtitle"),
    ]

    operations = [
        migrations.AddField(
            model_name="staff",
            name="jobTitle",
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
