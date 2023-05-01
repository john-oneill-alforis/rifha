from django.db import models

import uuid
import datetime

# Create your models here.


class staff(models.Model):
    staffId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    contactNUmber = models.CharField(max_length=100)
    jobTitle = models.ForeignKey("staffRole", on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.name


class staffRole(models.Model):
    roleId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    roleTitle = models.CharField(max_length=100)
    description = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name
