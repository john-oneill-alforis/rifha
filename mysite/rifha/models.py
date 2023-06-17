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
    fullName = models.CharField(max_length=100)
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
    assetDescription = models.TextField(max_length=1000)
    assetType = models.ForeignKey("assetsTypes", on_delete=models.CASCADE, default=1)
    assetClassification = models.ForeignKey(
        "assetsClassifications", on_delete=models.CASCADE, default=1
    )
    assetOwner = models.ForeignKey("staff", on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.name


class assetsTypes(models.Model):
    assetTypeId = models.CharField(
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


class riskReg(models.Model):
    riskId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )

    riskOwner = models.ForeignKey("staff", on_delete=models.CASCADE, default=1)
    riskAsset = models.ForeignKey("assets", on_delete=models.CASCADE, default=1)
    riskDescription = models.TextField(max_length=2000)
    riskCreationDate = models.DateField()
    riskReviewDate = models.DateField()
    riskNotes = models.TextField(max_length=2000, null=True, blank=True)
    riskAnalysisStatus = models.BooleanField(
        default=False, verbose_name="Analysis Completed"
    )
    controlAnalysisStatus = models.BooleanField(
        default=False, verbose_name="Analysis Completed"
    )
    """riskThreats = models.CharField(
        default="a5eb6a73-22ca-450b-a6b8-c2273f994ef3", max_length=36
    )"""
    riskThreats = models.ManyToManyField(
        "threatCatalogue",
    )
    riskControls = models.ManyToManyField(
        "controlCatalogue",
    )

    def __unicode__(self):
        return self.name


class threatCatalogue(models.Model):
    threatId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )

    threatName = models.CharField(max_length=200)
    threatCategory = models.CharField(max_length=200)
    threatlikelihood = models.FloatField()
    threatARO = models.FloatField()

    def __unicode__(self):
        return self.name


class controlCatalogue(models.Model):
    controlId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )

    controlName = models.CharField(max_length=200)
    controlCategory = models.CharField(max_length=200)
    controlDescription = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.name
