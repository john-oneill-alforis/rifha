# Generated by Django 4.1.7 on 2023-07-23 19:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0089_intervieweeresponse_compound_score"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="intervieweeresponse",
            name="interviewee_id",
        ),
        migrations.RemoveField(
            model_name="intervieweeresponse",
            name="question_id",
        ),
        migrations.AddField(
            model_name="intervieweeresponse",
            name="interviewee_id",
            field=models.ManyToManyField(to="polls.interviewee"),
        ),
        migrations.AddField(
            model_name="intervieweeresponse",
            name="question_id",
            field=models.ManyToManyField(to="polls.researchquestion"),
        ),
    ]
