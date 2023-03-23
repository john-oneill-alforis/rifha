from django.shortcuts import render
from datetime import date
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import trainingCorpus
from .models import textLabels
from django.db.models import Count

import mysql.connector
import os

# data_dict = {}


def contentList(request):
    corpusData = trainingCorpus.objects.all().order_by("dateAdded")
    context = {
        "entries": corpusData,
    }
    template = loader.get_template("polls/contentList.html")
    return HttpResponse(template.render(context, request))


def contentReview(request, msg):
    articleData = (
        trainingCorpus.objects.all()
        .filter(linkHash=msg)
        .select_related("textLabel")
        .all()
    )

    articleClassification = textLabels.objects.all().order_by("label").values()

    template = loader.get_template("polls/content.html")
    return HttpResponse(
        template.render(
            {
                "articleContent": articleData,
                "articleClassification": articleClassification,
            },
            request,
        )
    )


def tcUpdate(request, msg):
    articleContent = request.POST["text"]
    textLabel = request.POST["textlabelValues"]

    articleUpdate = trainingCorpus.objects.get(linkHash=msg)

    articleUpdate.text = articleContent
    articleUpdate.textLabel_id = textLabel

    articleUpdate.save(update_fields=["text", "textLabel"])

    return HttpResponseRedirect(redirect_to="/content/" + msg)


def dashboard(request):
    template = loader.get_template("polls/index.html")

    sourceCounts = (
        trainingCorpus.objects.all()
        .values("source")
        .annotate(total=Count("source"))
        .order_by("total")
    )

    labelCounts = (
        textLabels.objects.all().values("entryId").annotate(count=Count("label"))
    )

    context = {"sources": sourceCounts, "labels": labelCounts}

    return HttpResponse(template.render(context, request))
