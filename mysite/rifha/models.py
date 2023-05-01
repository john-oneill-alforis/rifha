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


class assets(models.Model):
    assetId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    assetName = models.CharField(max_length=100)
    assetDescription = models.CharField(max_length=254)
    assetType = models.OneToOneField("assetsTypes", on_delete=models.CASCADE, default=1)
    assetOwner = models.ForeignKey("staff", on_delete=models.CASCADE, default=1)

    def __unicode__(self):
        return self.name


class assetsTypes(models.Model):
    assetId = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    assetTypeName = models.CharField(max_length=100)
    assetDTypeDescription = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name


class processes(models.Model):
    processId = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4
    )
    processName = models.CharField(max_length=100)
    processDescription = models.CharField(max_length=254)
    processAssets = models.CharField(max_length=254)
    processOwner = models.CharField(max_length=254)

    def __unicode__(self):
        return self.name
