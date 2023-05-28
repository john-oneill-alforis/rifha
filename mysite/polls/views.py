from django.shortcuts import render, redirect, reverse
from django.db.models import Count, DateTimeField
from datetime import date, timezone, datetime, timedelta
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from math import log
from .models import trainingCorpus
from .models import textLabels
from .models import veris_incident_details
from .models import veris_incident_action_details
from .models import errorCapture
from .models import web_scraper_log
from .models import veris_asset_variety
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncYear, Cast, TruncDay
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# data_dict = {}


@login_required
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


@login_required
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


@login_required
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


@login_required
def debugDashboard(request):
    template = loader.get_template("polls/debugDash.html")

    errorCounts = (
        errorCapture.objects.annotate(created=TruncDay("date"))
        .values("created")
        .annotate(total=Count("incident_id"))
        .values("created", "total")
    )

    actionCounts_BC = (
        web_scraper_log.objects.all()
        .filter(source="Bleeping Computer")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_DR = (
        web_scraper_log.objects.all()
        .filter(source="Dark Reading")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_ISN = (
        web_scraper_log.objects.all()
        .filter(source="Information Security News")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    actionCounts_THN = (
        web_scraper_log.objects.all()
        .filter(source="The Hacker News")
        .values("source", "article_count", "date")
        .order_by("date")
    )

    dates = web_scraper_log.objects.values("date").distinct().order_by("date")

    context = {
        "errorCounts": errorCounts,
        "logged_dates": dates,
        "actionCounts_BC": actionCounts_BC,
        "actionCounts_DR": actionCounts_DR,
        "actionCounts_ISN": actionCounts_ISN,
        "actionCounts_THN": actionCounts_THN,
    }

    return HttpResponse(template.render(context, request))


###########################################################################################
# Veris Annualized Rate of Occurence Dashboard
###########################################################################################


@login_required
def verisaro(request):
    template = loader.get_template("polls/verisaro.html")

    # Retrieve all instances of the veris_asset_variety model
    data = veris_asset_variety.objects.exclude(variety__icontains="unknown").exclude(
        variety__icontains="other"
    )
    # Create a dictionary to store the frequency of each value
    frequency_dict = defaultdict(int)
    for instance in data:
        frequency_dict[instance.variety] += 1

    # Calculate the total number of instances
    total_count = len(data)

    # Calculate the probability and annualized rate of occurrence of each value
    results_dict = {}
    time_period = 1  # Time period in years
    for key, value in frequency_dict.items():
        probability = value / total_count
        annualized_rate = -log(1 - probability) / time_period
        results_dict[key] = {
            "probability": round(probability, 4),
            "annualized_rate": round(annualized_rate, 4),
        }

    # Pass the dictionary to the template context
    context = {"results_dict": results_dict}

    return HttpResponse(template.render(context, request))


###########################################################################################
# login stuff
###########################################################################################


def home(request):
    return render(request, "templates/polls/success.html", {})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("dashBoard")
    else:
        form = UserCreationForm()
    return render(request, "templates/polls/register.html", {"form": form})
