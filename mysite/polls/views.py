from django.shortcuts import render, redirect, reverse
from django.db.models import Count, DateTimeField
from datetime import date, timezone, datetime, timedelta
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from collections import defaultdict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from math import log
from django.db.models import Avg, F
from .models import trainingCorpus
from .models import textLabels
from .models import veris_incident_details
from .models import veris_incident_action_details
from .models import errorCapture
from .models import web_scraper_log
from .models import veris_asset_variety
from .models import interviewQuestions
from .models import interviewee
from .models import researchQuestion
from .models import intervieweeResponse

from django.db.models import Count
from django.db.models.functions import TruncDate, TruncYear, Cast, TruncDay
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import createInterviewee
from .forms import createResearchQuestion
from .forms import createResearchResponse

# data_dict = {}


###########################################################################################
# Pull all of the unclassfied data to be shown on the classification screen
###########################################################################################
@login_required
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
@login_required
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


@login_required
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
# Login controls
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


###########################################################################################
# Display Errors
###########################################################################################


@login_required
def errorLog(request):
    template = loader.get_template("polls/errors.html")

    erroLog = errorCapture.objects.all

    context = {
        "errorCounts": erroLog,
    }

    return HttpResponse(template.render(context, request))


###########################################################################################
# Adding Interview Data to the Database
###########################################################################################


@login_required
def get_interviewStats(request):
    template = loader.get_template("polls/interviewStats.html")

    """question1_sentiment = (
        interviewQuestions.objects.all().values("question_1").order_by("id")
    )

    question2_sentiment = (
        interviewQuestions.objects.all().values("question_2").order_by("id")
    )

    question3_sentiment = (
        interviewQuestions.objects.all().values("question_3").order_by("id")
    )

    question4_sentiment = (
        interviewQuestions.objects.all().values("question_4").order_by("id")
    )

    question5_sentiment = (
        interviewQuestions.objects.all().values("question_5").order_by("id")
    )

    question6_sentiment = (
        interviewQuestions.objects.all().values("question_6").order_by("id")
    )

    question7_sentiment = (
        interviewQuestions.objects.all().values("question_7").order_by("id")
    )

    question8_sentiment = (
        interviewQuestions.objects.all().values("question_8").order_by("id")
    )

    question9_sentiment = (
        interviewQuestions.objects.all().values("question_9").order_by("id")
    )

    q1_sentiment = []
    for x in question1_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_1"])

        q1_sentiment.append(sentiment_scores)

    q2_sentiment = []
    for x in question2_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_2"])

        q2_sentiment.append(sentiment_scores)

    q3_sentiment = []
    for x in question3_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_3"])

        q3_sentiment.append(sentiment_scores)

    q4_sentiment = []
    for x in question4_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_4"])

        q4_sentiment.append(sentiment_scores)

    q5_sentiment = []
    for x in question5_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_5"])

        q5_sentiment.append(sentiment_scores)

    q6_sentiment = []
    for x in question6_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_6"])

        q6_sentiment.append(sentiment_scores)

    q7_sentiment = []
    for x in question7_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_7"])

        q7_sentiment.append(sentiment_scores)

    q8_sentiment = []
    for x in question8_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_8"])

        q8_sentiment.append(sentiment_scores)

    q9_sentiment = []
    for x in question9_sentiment:
        analyzer = SentimentIntensityAnalyzer()
        sentiment_scores = analyzer.polarity_scores(x["question_9"])

        q9_sentiment.append(sentiment_scores)

    responseData = (
        interviewQuestions.objects.all()
        .values("interviewee_Id", "date_created")
        .order_by("id")
    )

    context = {
        "entries": responseData,
        "q1_sentiment": q1_sentiment,
        "q2_sentiment": q2_sentiment,
        "q3_sentiment": q3_sentiment,
        "q4_sentiment": q4_sentiment,
        "q5_sentiment": q5_sentiment,
        "q6_sentiment": q6_sentiment,
        "q7_sentiment": q7_sentiment,
        "q8_sentiment": q8_sentiment,
        "q9_sentiment": q9_sentiment,
        "questions": question1_sentiment,
    }

    return HttpResponse(template.render(context, request))"""

    response_data = intervieweeResponse.objects.values("question_id_id").annotate(
        answer_text=F("answer_text"),
        positivity_score=Avg("positivity_score"),
        neutrality_score=Avg("neutrality_score"),
        negativity_score=Avg("negativity_score"),
        compound_score=Avg("compound_score"),
    )

    context = {"data": response_data}

    template = loader.get_template("polls/interviewStats.html")
    return HttpResponse(template.render(context, request))


@login_required
def get_createInterviewee(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = createInterviewee(request.POST)
        if form.is_valid():
            en = interviewee(
                interviewee_reference=form.cleaned_data["interviewee_reference"],
                interviewee_role=form.cleaned_data["interviewee_role"],
                interviewee_fte=form.cleaned_data["interviewee_fte"],
                interviewee_org_type=form.cleaned_data["interviewee_org_type"],
            )

            en.save()

            return HttpResponseRedirect("/interviewStats/")

        # if a GET (or any other method) we'll create a blank form
    else:
        # form = interviewForm()
        intervieweeForm = createInterviewee()
        # question_texts = researchQuestion()

        context = {"intervieweeForm": intervieweeForm}

    return render(
        request,
        "polls/createInterviewee.html",
        context=context,
    )


@login_required
def get_interviewQuestion(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = createResearchQuestion(request.POST)
        if form.is_valid():
            en = researchQuestion(
                question_text=form.cleaned_data["question_text"],
            )

            en.save()

            return HttpResponseRedirect("/interviewStats/")

        # if a GET (or any other method) we'll create a blank form
    else:
        questionForm = createResearchQuestion()
        context = {"questionForm": questionForm}

    return render(
        request,
        "polls/createInterviewQuestion.html",
        context=context,
    )


@login_required
def get_interviewResponses(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = createResearchResponse(request.POST)
        if form.is_valid():
            interviewee_id = form.cleaned_data["interviewee"]
            # Initialize the Vader sentiment analyzer
            analyzer = SentimentIntensityAnalyzer()

            for key, value in form.cleaned_data.items():
                if key.startswith("question_"):
                    # Extract the number and text from the field name
                    question_number = key.split("_")[1]
                    question_text = value

                    # Perform sentiment analysis on the question text
                    sentiment_scores = analyzer.polarity_scores(question_text)
                    positivity_score = sentiment_scores["pos"]
                    neutrality_score = sentiment_scores["neu"]
                    negativity_score = sentiment_scores["neg"]
                    compound_score = sentiment_scores["compound"]

                    # Save the number and text to the database
                    en = intervieweeResponse(
                        answer_text=question_text,
                        positivity_score=positivity_score,
                        neutrality_score=neutrality_score,
                        negativity_score=negativity_score,
                        interviewee_id_id=interviewee_id,
                        question_id_id=question_number,
                        compound_score=compound_score,
                    )

                    en.save()

            return HttpResponseRedirect("/interviewStats/")
    else:
        responseForm = createResearchResponse()
        context = {"responseForm": responseForm}

    return render(
        request,
        "polls/createInterviewResponse.html",
        context=context,
    )
