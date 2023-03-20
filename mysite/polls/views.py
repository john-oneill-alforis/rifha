from django.shortcuts import render
from datetime import date
from django.template import loader
from django.http import HttpResponse
from .models import trainingCorpus
from .models import textLabels

import mysql.connector
import os

# data_dict = {}


def index(request):
    corpusData = trainingCorpus.objects.all()
    context = {
        "entries": corpusData,
    }
    template = loader.get_template("polls/index.html")
    return HttpResponse(template.render(context, request))


def contentReview(request, msg):
    articleData = (
        trainingCorpus.objects.all()
        .filter(linkHash=msg)
        .select_related("textLabel")
        .all()
    )

    articleClassification = textLabels.objects.all()

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
