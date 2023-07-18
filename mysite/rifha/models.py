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
    riskOwner = models.ForeignKey("staff", on_delete=models.PROTECT, default=1)
    riskAsset = models.ForeignKey("assets", on_delete=models.PROTECT, default=1)
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
    riskAssessmentStatus = models.BooleanField(
        default=False, verbose_name="Analysis Completed"
    )
    riskThreats = models.ManyToManyField(
        "threatCatalogue",
    )
    riskControls = models.ManyToManyField(
        "controlCatalogue",
    )
    residualRiskOffset = models.DecimalField(decimal_places=2, max_digits=10,default=0)
    minInherent = models.FloatField(default=0.00)
    avgInherent = models.FloatField(default=0.00)
    maxInherent = models.FloatField(default=0.00)

    minResidual = models.FloatField(default=0.00)
    avgResidual = models.FloatField(default=0.00)
    maxResidual = models.FloatField(default=0.00)


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
    threatMinCost = models.FloatField()
    threatMaxCost = models.FloatField()

    def __unicode__(self):
        return self.name


class controlCatalogue(models.Model):
    controlId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )

    controlName = models.CharField(max_length=200)
    controlCategory = models.ForeignKey(
        "controlTypes",
        on_delete=models.CASCADE,
        default="00545586-f865-48f5-9c33-19394977b783",
    )
    controlDescription = models.TextField(max_length=2000)

    def __unicode__(self):
        return self.name


class controlTypes(models.Model):
    controlTypeId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    controlTypeName = models.CharField(max_length=100)
    controlTypeDescription = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.name


class businessProcess(models.Model):
    businessProcessId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    businessProcessName = models.CharField(max_length=100)
    businessProcessDescription = models.CharField(max_length=2000)
    businessProcessCriticality = models.ForeignKey(
        "businessProcessCriticality",
        on_delete=models.CASCADE,
    )

    businessProcessOwner = models.ForeignKey(
        "staff",
        on_delete=models.CASCADE,
    )

    def __unicode__(self):
        return self.name


class businessProcessCriticality(models.Model):
    businessProcessCriticalityId = models.CharField(
        primary_key=True, auto_created=True, default=uuid.uuid4, max_length=36
    )
    businessProcessCriticality = models.CharField(max_length=100)
    businessProcessCriticalityDescription = models.CharField(max_length=2000)

    def __unicode__(self):
        return self.name
