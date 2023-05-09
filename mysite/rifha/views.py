from django.shortcuts import render
from django.db.models import Count, DateTimeField
from datetime import date, datetime, timedelta
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.db.models.functions import Trunc, TruncYear
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def dashboard(request):
    date_today = date.today().strftime("%Y-%m-%d")

    context = {
        "date": date_today,
    }
    template = loader.get_template("rifha/index.html")
    return HttpResponse(template.render(context, request))
