# Generated by Django 4.1.7 on 2023-06-12 16:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0086_alter_interviewee_interviewee_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="intervieweeresponse",
            name="answer_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
