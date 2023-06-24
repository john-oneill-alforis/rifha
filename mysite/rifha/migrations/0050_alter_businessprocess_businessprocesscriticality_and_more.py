# Generated by Django 4.1.7 on 2023-06-24 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("rifha", "0049_alter_businessprocess_businessprocesscriticality"),
    ]

    operations = [
        migrations.AlterField(
            model_name="businessprocess",
            name="businessProcessCriticality",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="rifha.businessprocesscriticality",
            ),
        ),
        migrations.AlterField(
            model_name="businessprocess",
            name="businessProcessOwner",
            field=models.ForeignKey(
                default="8aa92088-2d64-4674-90c9-4144e5f1c2d1",
                on_delete=django.db.models.deletion.CASCADE,
                to="rifha.staff",
            ),
        ),
    ]
