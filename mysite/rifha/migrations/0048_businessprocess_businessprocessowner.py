# Generated by Django 4.1.7 on 2023-06-24 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0047_businessprocesscriticality_businessprocess"),
    ]

    operations = [
        migrations.AddField(
            model_name="businessprocess",
            name="businessProcessOwner",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="rifha.staff",
            ),
            preserve_default=False,
        ),
    ]
