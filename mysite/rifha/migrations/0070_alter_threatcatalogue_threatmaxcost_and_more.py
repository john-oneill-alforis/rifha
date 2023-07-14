# Generated by Django 4.1.7 on 2023-07-14 10:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0069_alter_threatcatalogue_threatmaxcost_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="threatcatalogue",
            name="threatMaxCost",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="threatcatalogue",
            name="threatMinCost",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
