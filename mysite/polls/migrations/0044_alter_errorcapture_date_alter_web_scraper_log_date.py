# Generated by Django 4.1.7 on 2023-04-28 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0043_alter_errorcapture_date_alter_web_scraper_log_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorcapture",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="web_scraper_log",
            name="date",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
