from django.db import models

import uuid
import datetime

# Create your models here.


class staff(models.Model):
    staffId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    contactNumber = models.CharField(max_length=100)
    jobTitle = models.CharField(max_length=100)
    active = models.IntegerField(default=1)

    def __unicode__(self):
        return self.name


class staffRole(models.Model):
    roleId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    roleTitle = models.CharField(max_length=100)
    description = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class assets(models.Model):
    assetId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    assetName = models.CharField(max_length=100)
    assetDescription = models.CharField(max_length=254)
    assetType = models.OneToOneField("assetsTypes", on_delete=models.CASCADE, default=1)
    assetOwner = models.ForeignKey("staff", on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.name


class assetsTypes(models.Model):
    assetId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    assetTypeName = models.CharField(max_length=100)
    assetTypeDescription = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class assetsClassifications(models.Model):
    classification_Id = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    classificationLabel = models.CharField(max_length=100)
    classificationDescription = models.CharField(max_length=1000)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class processes(models.Model):
    processId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    processName = models.CharField(max_length=100)
    processDescription = models.CharField(max_length=254)
    processAssets = models.CharField(max_length=254)
    processOwner = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name
