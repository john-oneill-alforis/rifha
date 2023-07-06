from math import log
from django.shortcuts import render
from collections import defaultdict
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from decimal import Decimal
import json, random, kaleido
import os

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
    businessProcessCriticality,
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
from django.templatetags.static import static
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

    assetCount = assets.objects.all().count
    riskOwners = riskReg.objects.values("riskOwner").distinct().count()
    processCount = businessProcess.objects.all().count
    controlCount = controlCatalogue.objects.all().count

    ####################################################################
    # Calcualte the % of completed risk assessments
    ####################################################################

    totalCount = riskReg.objects.count()
    completedCount = riskReg.objects.filter(riskAnalysisStatus=1).count()

    if totalCount > 0:
        completionPercentage = (completedCount / totalCount) * 100
    else:
        completionPercentage = 0.0

    incompletePercentage = 100 - completionPercentage

    ####################################################################
    # Retrieve the business processes and the criticality of each
    ####################################################################

    criticalityCounts = businessProcessCriticality.objects.annotate(
        count=Count("businessprocess")
    )

    context = {
        "date": date_today,
        "assetCount": assetCount,
        "riskOwners": riskOwners,
        "processCount": processCount,
        "controlCount": controlCount,
        "completionPercentage": completionPercentage,
        "incompletePercentage": incompletePercentage,
        "criticalityCounts": criticalityCounts,
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

    """# Set a number to represent the reduction in risk gained
    # from control maturity

    controlMaturity = float(riskData.residualRiskOffset)

    # Set the number of Monte Carlo simulation iterations
    numIterations = 10000

    # Generate the randdom probabilities and add them to a list

    randomProbability = np.random.uniform(0, 1, numIterations)

    # Create empty lists to hold values to plot later
    inherentProbValue = []
    inherentCalculatedLosses = []
    residualProbValue = []
    residualCalculatedLosses = []

    # Generate scenarios and combine financial outcomes for each series
    for threat in threats:
        probability = threat["threatlikelihood"]
        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

        # Calcualte the inhernet probability losses
        for x in randomProbability:
            if x <= probability:
                mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
                std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

                inherentProbValue.append(x)
                inherentCalculatedLosses.append(np.random.lognormal(mean, std_dv))

    # Second loop to deal with the residual risk
    for threat in threats:
        probability = threat["threatlikelihood"] - (
            threat["threatlikelihood"] * controlMaturity / 100
        )
        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

        for x in randomProbability:
            if x <= probability:
                mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
                std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29
                residualProbValue.append(x)
                residualCalculatedLosses.append(np.random.lognormal(mean, std_dv))

    # Loss Exceedance Curve Calculations

    np.cumsum(inherentCalculatedLosses)

    inherentCalculatedLosses.sort()
    residualCalculatedLosses.sort()

    inherentProbValue.sort()
    residualProbValue.sort()

    avgCostInherent = (sum(inherentCalculatedLosses) / len(inherentCalculatedLosses), 2)
    avgCostResidual = (sum(residualCalculatedLosses) / len(residualCalculatedLosses), 2)

    yData = inherentProbValue + residualProbValue

    inherentRiskDist = go.Figure(
        data=[
            go.Histogram(
                x=inherentCalculatedLosses, y=yData, name="Inherent Risk", nbinsx=50
            ),
            go.Histogram(x=residualCalculatedLosses, name="Residual Risk", nbinsy=50),
        ]
    )

    inherentRiskDist.update_layout(
        title="Inherent Risk Distribution",
        xaxis_title="Risk Impact",
        yaxis_title="f(x) Distribution",
        legend_title="Legend Title",
    )"""

    # Set the number of Monte Carlo simulation iterations
    numIterations = 10000

    inherentProbValue = []
    inherentCalculatedLosses = []
    threatOffset = riskData.residualRiskOffset

    randomProbability = np.random.uniform(0, 1, numIterations)

    # Generate scenarios and combine financial outcomes for each series
    for threat in threats:
        probability = threat["threatlikelihood"]
        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

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
        rProbability = threat["threatlikelihood"] - (
            threat["threatlikelihood"] * threatOffset
        )

        lower_limit = threat["threatMinCost"]
        upper_limit = threat["threatMaxCost"]

        for x in randomProbability:
            if x <= rProbability:
                mean = (np.log(lower_limit) + np.log(upper_limit)) / 2.0
                std_dv = (np.log(upper_limit) - np.log(lower_limit)) / 3.29

                residualProbValue.append(x)
                residualCalculatedLosses.append(np.random.lognormal(mean, std_dv))

    iLec = inherentCalculatedLosses.sort(reverse=True)
    rLec = residualCalculatedLosses.sort(reverse=True)

    riProbValue = inherentProbValue.sort(reverse=True)
    rrProbValue = residualProbValue.sort(reverse=True)

    inherentCalculatedLosses.sort()
    residualCalculatedLosses.sort()

    inherentProbValue.sort()
    residualProbValue.sort()

    ##########################################################################################
    # Probability Distribution
    ##########################################################################################

    figPD = go.Figure()

    figPD.add_trace(
        go.Histogram(
            x=residualCalculatedLosses, name="Residual Probability Distribution"
        )
    )
    figPD.add_trace(
        go.Histogram(
            x=inherentCalculatedLosses, name="Inherent Probability Distribution"
        )
    )

    # The two histograms are drawn on top of another
    figPD.update_layout(barmode="stack")

    figPD.write_image("images/" + msg + "-PD.png")

    ##########################################################################################
    # Probability Curve
    ##########################################################################################

    figPC = go.Figure()

    figPC.add_trace(
        go.Scatter(
            x=residualCalculatedLosses,
            y=residualProbValue,
            mode="lines",
            name="Residual Probability",
        )
    )

    figPC.add_trace(
        go.Scatter(
            x=inherentCalculatedLosses,
            y=inherentProbValue,
            mode="lines",
            name="Inherent",
        )
    )

    figPC.write_image("images/" + msg + "-PC.png")

    ##########################################################################################
    # LEC Curve
    ##########################################################################################

    # Sort the Probability Array

    sortedRandomProbability = np.sort(randomProbability)

    # Sort the probabilities and costs in ascending order of costs
    inherentSortedIndices = np.argsort(inherentCalculatedLosses)
    inherentSortedProbabilities = np.array(sortedRandomProbability)[
        inherentSortedIndices
    ]
    inherentSortedCosts = np.array(inherentCalculatedLosses)[inherentSortedIndices]

    # Calculate exceedance probabilities
    inherentExceedanceProbs = 1 - inherentSortedProbabilities

    ##########################################################################################
    # Residual
    ##########################################################################################
    residualSortedIndices = np.argsort(residualCalculatedLosses)
    residualSortedProbabilities = np.array(sortedRandomProbability)[
        residualSortedIndices
    ]
    residualSortedCosts = np.array(residualCalculatedLosses)[residualSortedIndices]

    # Calculate exceedance probabilities
    residualExceedanceProbs = 1 - residualSortedProbabilities

    figLEC = go.Figure()

    figLEC.add_trace(
        go.Scatter(
            x=inherentSortedCosts,
            y=inherentExceedanceProbs,
            mode="lines",
            name="Inherent",
        )
    )

    figLEC.add_trace(
        go.Scatter(
            x=residualSortedCosts,
            y=residualExceedanceProbs,
            mode="lines",
            name="Residual",
        )
    )

    figLEC.write_image("images/" + msg + "-LEC.png")

    context = {
        "riskData": riskData,
        "RiskDist": figPD.to_html(
            full_html=False,
        ),
        "ProabilityCurve": figPC.to_html(
            full_html=False,
        ),
        "epCurve": figLEC.to_html(
            full_html=False,
        ),
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
