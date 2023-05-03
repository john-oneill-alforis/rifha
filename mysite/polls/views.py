from django.shortcuts import render
from django.db.models import Count, DateTimeField
from datetime import date, timezone, datetime, timedelta
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import trainingCorpus
from .models import textLabels
from .models import veris_incident_details
from .models import veris_incident_action_details
from .models import errorCapture
from .models import web_scraper_log
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncYear, Cast


# data_dict = {}


###########################################################################################
# Pull all of the unclassfied data to be shown on the classification screen
###########################################################################################
def contentList(request):
    corpusData = (
        trainingCorpus.objects.all().filter(textLabel_id=1).order_by("dateAdded")
    )
    context = {
        "entries": corpusData,
    }
    template = loader.get_template("polls/contentList.html")
    return HttpResponse(template.render(context, request))


###########################################################################################
# Pull the article so it can be classified
###########################################################################################
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


###########################################################################################
# Text Classification Update
###########################################################################################


def tcUpdate(request, msg):
    articleContent = request.POST["text"]
    textLabel = request.POST["textlabelValues"]

    articleUpdate = trainingCorpus.objects.get(linkHash=msg)

    articleUpdate.text = articleContent
    articleUpdate.textLabel_id = textLabel

    articleUpdate.save(update_fields=["text", "textLabel"])

    return HttpResponseRedirect(redirect_to="/trainingcorpus")


###########################################################################################
# Dashboard Screen
###########################################################################################


def dashboard(request):
    template = loader.get_template("polls/index.html")

    sourceCounts = (
        trainingCorpus.objects.all()
        .values("source")
        .annotate(total=Count("source"))
        .order_by("total")
    )

    labelCounts = (
        textLabels.objects.values("label")
        .annotate(num_entries=Count("trainingcorpus"))
        .order_by("label")
    )

    assoclabelCounts = (
        textLabels.objects.values("label")
        .exclude(modelAssociated=0)
        .annotate(num_entries=Count("trainingcorpus"))
        .order_by("label")
    )

    totalCount = trainingCorpus.objects.all().count()

    classifiedEntries = trainingCorpus.objects.exclude(textLabel=1).count()

    context = {
        "sources": sourceCounts,
        "labels": labelCounts,
        "count": totalCount,
        "classified": classifiedEntries,
        "associated": assoclabelCounts,
    }

    return HttpResponse(template.render(context, request))


###########################################################################################
# Veris Information Screens
###########################################################################################


def verisDashboard(request):
    template = loader.get_template("polls/verisDash.html")
    totalCount = veris_incident_details.objects.all().count()

    yearCounts = (
        veris_incident_details.objects.annotate(year=TruncYear("created"))
        .values("year")
        .annotate(total=Count("incident_id"))
        .order_by("year")
    )

    actionCounts = veris_incident_action_details.objects.values("action").annotate(
        total=Count("action")
    )

    context = {
        "total_count": totalCount,
        "year_counts": yearCounts,
        "action_counts": actionCounts,
    }

    return HttpResponse(template.render(context, request))


###########################################################################################
# Debug Information
###########################################################################################


def debugDashboard(request):
    template = loader.get_template("polls/debugDash.html")

    errorCounts = (
        errorCapture.objects.all().values("date").annotate(total=Count("incident_id"))
    )

    actionCounts_BC = (
        web_scraper_log.objects.all()
        .filter(source="bleepingcomputer")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_DR = (
        web_scraper_log.objects.all()
        .filter(source="darkreading")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_ISN = (
        web_scraper_log.objects.all()
        .filter(source="informationsecuritynews")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_THN = (
        web_scraper_log.objects.all()
        .filter(source="thehackernews")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    context = {
        "errorCounts": errorCounts,
        "actionCounts_BC": actionCounts_BC,
        "actionCounts_DR": actionCounts_DR,
        "actionCounts_ISN": actionCounts_ISN,
        "actionCounts_THN": actionCounts_THN,
    }

    return HttpResponse(template.render(context, request))
