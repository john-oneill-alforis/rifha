from pymongo import MongoClient
import os
import sys
import datetime
from pathlib import Path
import json


def load_veris():
    try:
        myclient = MongoClient("mongodb://localhost:27017/")
        db = myclient["thesis_vert"]
        collection = db["veris_cdb"]

        # Create the database for our example (we will use the same database throughout the tutorial

        cursor = collection.find({})
        pass

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

    try:
        methods = []
        test = collection.distinct("action").count()
        for x in test:
            print(x)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())


load_veris()
