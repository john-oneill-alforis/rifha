from django.shortcuts import render
from datetime import date
import mysql.connector
import os

from django.http import HttpResponse


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

    return HttpResponse(records)

    mycursor.close()

    # today = date.today()
