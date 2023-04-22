from django.db import models
import uuid

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class textLabels(models.Model):
    entryId = models.BigAutoField(primary_key=True)
    label = models.TextField(max_length=200)
    modelAssociated = models.BooleanField()

    def __unicode__(self):
        return self.label

    def __str__(self):
        return self.label


class trainingCorpus(models.Model):
    entryId = models.BigAutoField(primary_key=True)
    source = models.CharField(max_length=200)
    author = models.CharField(max_length=45)
    publishedDate = models.DateField()
    dateAdded = models.DateField()
    link = models.TextField()
    text = models.TextField()
    linkHash = models.CharField(max_length=256, db_index=True, unique=True)
    included = models.IntegerField(default=1)
    verisCompatible = models.CharField(max_length=45, blank=True, null=True)
    textLabel = models.ForeignKey(
        textLabels,
        on_delete=models.CASCADE,
        default=1,
    )

    def __unicode__(self):
        return self.name


class veris_incident_details(models.Model):
    incident_id = models.CharField(max_length=45, primary_key=True)
    security_incident = models.CharField(max_length=45)
    source_id = models.CharField(max_length=45)

    summary = models.TextField
    analysis_status = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now=False, auto_now_add=False)

    master_id = models.CharField(max_length=45)
    modified = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.name
