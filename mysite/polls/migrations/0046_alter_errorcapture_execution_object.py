# Generated by Django 4.1.7 on 2023-04-28 09:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0045_alter_errorcapture_date_alter_web_scraper_log_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="errorcapture",
            name="execution_object",
            field=models.CharField(max_length=1000),
        ),
    ]
