# Generated by Django 4.1.7 on 2023-04-09 12:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0028_alter_textlabels_modelassociated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="textlabels",
            name="modelAssociated",
            field=models.BooleanField(),
        ),
    ]
