from django.shortcuts import render
from django.db.models import Count, DateTimeField
from datetime import date, datetime, timedelta
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Count
from .models import staff
from django.db.models.functions import Trunc, TruncYear
from django.contrib.auth.decorators import login_required
from .forms import peopleAddForm
from .forms import peopleEditForm
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
def assetsHome(request):
    date_today = date.today().strftime("%Y-%m-%d")
    context = {
        "date": "Hello World!",
    }
    template = loader.get_template("assetsDashboard.html")
    return HttpResponse(template.render(context, request))


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
