from django.db import models
import uuid
import datetime

# Create your models here.


class businessProcesses(models.Model):
    entryId = models.BigAutoField(primary_key=True)
    processId = models.UUIDField()
    name = models.CharField(max_length=254)
    description = models.TextField()
    owner = models.IntegerField()
    dateCreated = models.DateField()
    reviewDate = models.DateField()

    def __unicode__(self):
        return self.name
