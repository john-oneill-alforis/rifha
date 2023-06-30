from math import log
from django.shortcuts import render
from collections import defaultdict
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from decimal import Decimal
import json, random

# from django.db.models import Count, DateTimeField
from datetime import date, datetime, timedelta
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import (
    staff,
    assetsClassifications,
    assetsTypes,
    assets,
    riskReg,
    threatCatalogue,
    controlCatalogue,
    businessProcess,
)
from polls.models import (
    veris_action_malware_variety,
    veris_action_hacking_variety,
    veris_action_social_variety,
    veris_action_misuse_variety,
    veris_action_error_variety,
    veris_action_environmental_variety,
)

from django.db.models.functions import Trunc, TruncYear
from django.contrib.auth.decorators import login_required
from .forms import (
    peopleAddForm,
    assetTypesEditForm,
    peopleEditForm,
    classificationAddForm,
    classificationEditForm,
    assettTypeAddForm,
    addAssetForm,
    addRiskForm,
    addRiskAnalysisForm,
    addRiskThreatForm,
    addRiskControlForm,
    addControlForm,
    addBusinessProcessForm,
    residualRiskOffsetForm,
)
from django.shortcuts import get_object_or_404

# Create your views here.


@login_required
def dashboard(request):
    date_today = date.today().strftime("%Y-%m-%d")

    context = {
        "date": date_today,
    }
    template = loader.get_template("index.html")
    return HttpResponse(template.render(context, request))


@login_required
def assettHome(request):
    all_assets = assets.objects.select_related(
        "assetType",
        "assetClassification",
        "assetOwner",
    ).all()
    context = {
        "assets": all_assets,
    }
    template = loader.get_template("assetsDashboard.html")
    return HttpResponse(template.render(context, request))


@login_required
def assettAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = addAssetForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/assets/")
    else:
        form = addAssetForm()

    context = {"form": form}
    return render(request, "assetsAdd.html", context)


@login_required
def assettEdit(request, msg):
    assetData = assets.objects.get(assetId=msg)

    if request.method == "POST":
        form = addAssetForm(request.POST, instance=assetData)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/rifha/assettEdit/" + msg)
    else:
        form = addAssetForm(instance=assetData)

    context = {"form": form, "assetId": msg}
    return render(request, "assetsEdit.html", context)


@login_required
def controlsHome(request):
    all_controls = controlCatalogue.objects.select_related("controlCategory").all()
    context = {
        "controls": all_controls,
    }
    template = loader.get_template("controlsDashboard.html")
    return HttpResponse(template.render(context, request))


@login_required
def controlsEdit(request, msg):
    controlData = controlCatalogue.objects.get(controlId=msg)

    if request.method == "POST":
        form = addControlForm(request.POST, instance=controlData)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/rifha/controlsEdit/" + msg)
    else:
        form = addControlForm(instance=controlData)

    context = {"form": form, "controlId": msg}
    return render(request, "controlsEdit.html", context)


@login_required
def controlAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = addControlForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/controls/")
    else:
        form = addControlForm()

    context = {"form": form}
    return render(request, "controlsAdd.html", context)


@login_required
def peopleHome(request):
    team = staff.objects.all().order_by("firstName")

    context = {
        "team": team,
    }
    template = loader.get_template("peopleDashboard.html")
    return HttpResponse(template.render(context, request))


@login_required
def peopleEdit(request, msg):
    # personnelData = get_object_or_404(staff, staffId=msg)
    personnelData = staff.objects.get(staffId=msg)

    if request.method == "POST":
        form = peopleEditForm(request.POST, instance=personnelData)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/peopleEdit/" + msg)
    else:
        form = peopleEditForm(instance=personnelData)

    context = {"form": form, "staffId": msg}
    return render(request, "peopleEdit.html", context)


@login_required
def peopleAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = peopleAddForm(request.POST)
        if form.is_valid():
            # Save the number and text to the database
            en = staff(
                firstName=form.cleaned_data["firstName"],
                lastName=form.cleaned_data["lastName"],
                email=form.cleaned_data["email"],
                jobTitle=form.cleaned_data["jobTitle"],
                contactNumber=form.cleaned_data["contactNumber"],
            )

            en.save()

            return HttpResponseRedirect("/rifha/people/")
    else:
        createPeople = peopleAddForm()
        context = {"peopleAdd": createPeople}

    return render(
        request,
        "peopleAdd.html",
        context=context,
    )


@login_required
def admin(request):
    team = assetsClassifications.objects.all().order_by("-rank")
    asset_type = assetsTypes.objects.all().order_by("assetTypeName")

    context = {"classifications": team, "assettTypes": asset_type}
    template = loader.get_template("adminDashboard.html")
    return HttpResponse(template.render(context, request))


@login_required
def classificationAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = classificationAddForm(request.POST)
        if form.is_valid():
            # Save the number and text to the database
            en = assetsClassifications(
                # classification_Id=uuid.uuid4(),
                classificationLabel=form.cleaned_data["classificationLabel"],
                classificationDescription=form.cleaned_data[
                    "classificationDescription"
                ],
            )

            en.save()

            return HttpResponseRedirect("/rifha/admin/")
    else:
        createClassification = classificationAddForm()
        context = {"createClassification": createClassification}

    return render(
        request,
        "classificationAdd.html",
        context=context,
    )


@login_required
def classificationEdit(request, msg):
    classificatonData = assetsClassifications.objects.get(classification_Id=msg)

    if request.method == "POST":
        form = classificationEditForm(request.POST, instance=classificatonData)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/classificationEdit/" + msg)
    else:
        form = classificationEditForm(instance=classificatonData)

    context = {"form": form, "classification_Id": msg}
    return render(request, "classificationEdit.html", context)


@login_required
def assettTypeAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = assettTypeAddForm(request.POST)
        if form.is_valid():
            # Save the number and text to the database
            en = assetsTypes(
                assetTypeName=form.cleaned_data["assetTypeLabel"],
                assetTypeDescription=form.cleaned_data["assettTypeDescription"],
            )

            en.save()

            return HttpResponseRedirect("/rifha/admin/")
    else:
        createAssettType = assettTypeAddForm()
        context = {"createassettType": createAssettType}

    return render(
        request,
        "assettTypeAdd.html",
        context=context,
    )


@login_required
def assettTypeEdit(request, msg):
    assetTypeData = assetsTypes.objects.get(assetTypeId=msg)

    if request.method == "POST":
        form = assetTypesEditForm(request.POST, instance=assetTypeData)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/assettTypeEdit/" + msg)
    else:
        form = assetTypesEditForm(instance=assetTypeData)

    context = {"form": form, "assetTypeId": msg}
    return render(request, "assettTypeEdit.html", context)


@login_required
def riskHome(request):
    all_risks = riskReg.objects.all()
    context = {
        "risks": all_risks,
    }
    template = loader.get_template("riskDashBoard.html")
    return HttpResponse(template.render(context, request))


@login_required
def riskAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = addRiskForm(request.POST)
        if form.is_valid():
            """form.save()"""
            en = riskReg(
                riskId=form.cleaned_data["riskId"],
                riskOwner=form.cleaned_data["riskOwner"],
                riskAsset=form.cleaned_data["riskAsset"],
                riskDescription=form.cleaned_data["riskDescription"],
                riskCreationDate=form.cleaned_data["riskCreationDate"],
                riskReviewDate=form.cleaned_data["riskReviewDate"],
                riskNotes=form.cleaned_data["riskNotes"],
            )
            en.save()
            # Handle successful form submission by moving to the anlaysis phase
            return HttpResponseRedirect(
                "/rifha/riskAnalysisAdd/" + form.cleaned_data["riskId"]
            )
    else:
        form = addRiskForm()

    context = {"form": form}
    return render(request, "riskAdd.html", context)


@login_required
def riskAnalysisAdd(request, msg):
    riskData = riskReg.objects.get(riskId=msg)
    context = {}

    form = addRiskAnalysisForm(instance=riskData)
    threatList = addRiskThreatForm()
    threatData = threatCatalogue.objects.filter(riskreg__riskId=msg).values(
        "threatName", "threatlikelihood", "threatARO"
    )

    context = {
        "riskId": msg,
        "form": form,
        "threat_list": threatList,
        "threatData": threatData,
    }
    return render(request, "riskAnalysisAdd.html", context)


@login_required
def riskthreatAdd(request, msg):
    risk = riskReg.objects.get(riskId=msg)

    if request.method == "POST":
        # Get the list of threat IDs from the form data
        threat_ids = request.POST.getlist("riskThreats")

        # Add selected threats to the risk
        for threat_id in threat_ids:
            threat = threatCatalogue.objects.get(threatId=threat_id)
            risk.riskThreats.add(threat)

    return HttpResponseRedirect("/rifha/riskAnalysisAdd/" + msg)


@login_required
def riskControlsAdd(request, msg):
    riskData = riskReg.objects.get(riskId=msg)

    if request.method == "POST":
        riskData.riskAnalysisStatus = 1
        riskData.save()

    if request.method == "POST":
        # Get the list of threat IDs from the form data
        control_ids = request.POST.getlist("riskControls")

        # Add selected threats to the risk
        for control_id in control_ids:
            control = controlCatalogue.objects.get(controlId=control_id)
            riskData.riskControls.add(control)

    if request.method == "POST":
        # Process the form data
        residual_risk_offset_form = residualRiskOffsetForm(
            request.POST, instance=riskData
        )
        if residual_risk_offset_form.is_valid():
            residual_risk_offset_form.save()
    else:
        residual_risk_offset_form = residualRiskOffsetForm(instance=riskData)

    riskData = addRiskAnalysisForm(instance=riskData)
    threatData = threatCatalogue.objects.filter(riskreg__riskId=msg).values(
        "threatName",
        "threatlikelihood",
        "threatARO",
    )

    # controlCatalogue.objects.select_related("controlCategory").all()

    controlList = addRiskControlForm()
    controlData = controlCatalogue.objects.filter(riskreg__riskId=msg).values(
        "controlName", "controlCategory__controlTypeName", "controlDescription"
    )

    context = {
        "riskId": msg,
        "form": riskData,
        "controlList": controlList,
        "controlData": controlData,
        "threatData": threatData,
        "residualRiskOffsetForm": residual_risk_offset_form,
    }
    return render(request, "riskControlsAdd.html", context)


@login_required
def riskReport(request, msg):
    # Fetch risk data from the database

    riskData = riskReg.objects.get(riskId=msg)

    # Retrieve threat data from the database
    threats = threatCatalogue.objects.filter(riskreg__riskId=msg).values(
        "threatName",
        "threatlikelihood",
        "threatMinCost",
        "threatMaxCost",
    )

    # Set a number to represent the reduction in risk gained
    # from control maturity
    controlMaturity = 0.98

    # Set the number of Monte Carlo simulation iterations
    numIterations = 5000

    inherentProbValue = []
    inherentCalculatedLosses = []

    # Generate scenarios and combine financial outcomes for each series
    for threat in threats:
        probability = threat["threatlikelihood"]
        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

        randomProbability = np.random.uniform(0, 1, numIterations)

        for x in randomProbability:
            if x <= probability:
                mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
                std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

                inherentProbValue.append(x)
                inherentCalculatedLosses.append(np.random.lognormal(mean, std_dv))

    residualProbValue = []
    residualCalculatedLosses = []
    # Generate scenarios and combine financial outcomes for each series
    for threat in threats:
        probability = threat["threatlikelihood"] - (
            threat["threatlikelihood"] * controlMaturity
        )
        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

        randomProbability = np.random.uniform(0, 1, numIterations)

        for x in randomProbability:
            if x <= probability:
                mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
                std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

                residualProbValue.append(x)
                residualCalculatedLosses.append(np.random.lognormal(mean, std_dv))

    inherentCalculatedLosses.sort(reverse=True)
    residualCalculatedLosses.sort(reverse=True)

    inherentProbValue.sort()
    residualProbValue.sort()

    # Prepare data
    y_data1 = inherentProbValue
    y_data2 = residualProbValue
    x_data1 = inherentCalculatedLosses
    x_data2 = residualCalculatedLosses

    # Create Plotly graph with multiple line graphs
    graph = go.Figure()
    graph.add_trace(
        go.Scatter(
            x=x_data1,
            y=y_data1,
            mode="lines",
            name="Inherent Risk - Loss Exceedence Curve",
        )
    )
    graph.add_trace(
        go.Scatter(
            x=x_data2,
            y=y_data2,
            mode="lines",
            name="Residual Risk - Loss Exceedence Curve",
        )
    )

    graph.update_layout(
        width=1600,
        height=800,
        plot_bgcolor="rgba(0,0,0,0)",
    )

    # Convert the graph to JSON
    graph_json = graph.to_json()

    averageInherent = max(inherentCalculatedLosses)
    averageResidual = max(residualCalculatedLosses)

    minInherent = min(inherentCalculatedLosses)
    minResidual = min(residualCalculatedLosses)

    context = {
        "inherentCalculatedLosses": inherentCalculatedLosses,
        "residualCalculatedLosses": residualCalculatedLosses,
        "inherentProbValue": inherentProbValue,
        "residualProbValue": residualProbValue,
        "graph_json": graph_json,
        "averageInherent": averageInherent,
        "averageResidual": averageResidual,
        "minInherent": minInherent,
        "minResidual": minResidual,
        "riskData": riskData,
    }
    return render(request, "riskReport.html", context)


@login_required
def riskEdit(request, msg):
    riskData = riskReg.objects.get(riskId=msg)
    if request.method == "POST":
        form = addRiskForm(request.POST, instance=riskData)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/rifha/riskEdit/" + msg)
    else:
        form = addRiskForm(instance=riskData)

    context = {"form": form, "riskId": msg}
    return render(request, "riskEdit.html", context)


@login_required
def populateThreatInformation(request):
    # Delete out the existing dataset to avoid dupes
    threatCatalogue.objects.all().delete()

    tables = []
    tableDict = [
        veris_action_malware_variety,
        veris_action_hacking_variety,
        veris_action_social_variety,
        veris_action_misuse_variety,
        veris_action_error_variety,
        veris_action_environmental_variety,
    ]

    for x in tableDict:
        # split the string to create the category
        parts = str(x).split("_")
        category = "_".join(parts[2:3])

        # Retrieve all instances of the veris_action_X_varieties model
        data = x.objects.exclude(variety__icontains="unknown").exclude(
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

            en = threatCatalogue(
                # classification_Id=uuid.uuid4(),
                threatCategory=category,
                threatName=key,
                threatlikelihood=round(probability, 4),
                threatARO=round(annualized_rate, 4),
            )

            en.save()

    context = {"results_dict": results_dict, "category": category}
    return render(request, "adminDashboard.html", context)


@login_required
def processesHome(request):
    pass
    all_processes = businessProcess.objects.select_related(
        "businessProcessCriticality"
    ).all()

    context = {
        "processes": all_processes,
    }
    template = loader.get_template("processDashboard.html")
    return HttpResponse(template.render(context, request))


@login_required
def processAdd(request):
    context = {}
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        form = addBusinessProcessForm(request.POST)
        if form.is_valid():
            form.save()
            # Handle successful form submission, e.g., redirect to a success page
            return HttpResponseRedirect("/rifha/processes/")
    else:
        form = addBusinessProcessForm()

    context = {"form": form}
    return render(request, "processAdd.html", context)


@login_required
def processEdit(request, msg):
    businessProcessData = businessProcess.objects.get(businessProcessId=msg)
    if request.method == "POST":
        form = addBusinessProcessForm(request.POST, instance=businessProcessData)
        if form.is_valid():
            form.save()

        return HttpResponseRedirect("/rifha/processEdit/" + msg)
    else:
        form = addBusinessProcessForm(instance=businessProcessData)

    context = {"form": form, "businessProcessId": msg}
    return render(request, "processEdit.html", context)
