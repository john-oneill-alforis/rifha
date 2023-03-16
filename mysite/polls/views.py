from django.shortcuts import render
from datetime import date
from django.template import loader
from django.http import HttpResponse

import mysql.connector
import os

data_dict = {}


def index(request):
    # Database Connection to Pull Existing Meta Values
    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    sql = """SELECT source, publishedDate, dateAdded, link, linkHash 
            FROM polls_trainingcorpus
            ORDER BY dateAdded;"""

    mycursor = mydb.cursor()
    mycursor.execute(sql)

    records = mycursor.fetchall()

    # return HttpResponse(records)

    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964,
        "brand": "Nissan",
        "model": "Almera",
        "year": 2002,
    }

    template = loader.get_template("polls/index.html")
    return HttpResponse(template.render(thisdict, request))
