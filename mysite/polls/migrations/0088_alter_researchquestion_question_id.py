# Generated by Django 4.1.7 on 2023-06-12 16:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0087_alter_intervieweeresponse_answer_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="researchquestion",
            name="question_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]