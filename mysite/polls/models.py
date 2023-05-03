from django.db import models
import uuid
import datetime

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
        return self.link

    def __str__(self):
        return self.link, self.source


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
        return self.incident_id


######################################################################
# Veris Incident Information Tables
######################################################################


class veris_incident_details(models.Model):
    incident_id = models.CharField(max_length=45, primary_key=True)
    security_incident = models.CharField(max_length=45)
    source_id = models.CharField(max_length=45)

    summary = models.TextField(default="None")
    analysis_status = models.CharField(max_length=200)
    created = models.DateField(auto_now=False)

    master_id = models.CharField(max_length=45)
    modified = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __unicode__(self):
        return self.name


######################################################################
# Veris Incident Action Information Tables
######################################################################


class veris_incident_action_details(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    action = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name


class veris_action_details(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    incident_id = models.CharField(max_length=45)
    action = models.CharField(max_length=45)

    def __unicode__(self):
        return self.name


######################################################################
# Action Logging for Scripts
######################################################################


# Error Captures
class errorCapture(models.Model):
    incident_id = models.BigAutoField(primary_key=True)
    execution_type = models.TextField(blank=True)
    execution_object = models.CharField(max_length=1000)
    file_name = models.CharField(max_length=250)
    file_line = models.IntegerField(blank=True)
    date = models.DateField(blank=True)

    def __unicode__(self):
        return self.name


# Work Capture
class web_scraper_log(models.Model):
    entry_Id = models.BigAutoField(primary_key=True)
    source = models.CharField(max_length=45)
    article_count = models.IntegerField()
    date = models.DateField(blank=True)

    def __unicode__(self):
        return self.source, self.date

    def __str__(self):
        return self.source, self.date
