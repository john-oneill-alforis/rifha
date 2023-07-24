# Generated by Django 4.1.7 on 2023-07-24 08:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("polls", "0097_delete_intervieweeresponse"),
    ]

    operations = [
        migrations.CreateModel(
            name="transcriptCapture",
            fields=[
                ("response_id", models.AutoField(primary_key=True, serialize=False)),
                ("interviewee_id", models.IntegerField(default=1)),
                ("question_id", models.IntegerField(default=1)),
                ("primary_answer_text", models.TextField()),
                ("secondary_answer_text", models.TextField()),
                ("positivity_score", models.FloatField()),
                ("neutrality_score", models.FloatField()),
                ("negativity_score", models.FloatField()),
                ("compound_score", models.FloatField()),
            ],
        ),
    ]
