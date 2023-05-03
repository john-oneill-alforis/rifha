import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv
import requests
import hashlib
from sqlalchemy import insert, func, select
from sqlalchemy.orm import Session, sessionmaker
import sys
import os
import sqlalchemy as db


def update_web_scraper_log():
    load_dotenv()
    engine = db.create_engine(
        "mysql://"
        + (os.getenv("db_user"))
        + ":"
        + (os.getenv("db_password"))
        + "@localhost/thesis_vert"
    )
    conn = engine.connect()
    metadata = db.MetaData()

    web_scraper_log = db.Table("polls_web_scraper_log", metadata, autoload_with=engine)
    web_scraper_log = metadata.tables["polls_web_scraper_log"]

    polls_trainingcorpus = db.Table(
        "polls_trainingcorpus", metadata, autoload_with=engine
    )
    polls_trainingcorpus = metadata.tables["polls_trainingcorpus"]

    #################################################################
    # Get all the training corpus entries
    #################################################################

    Session = sessionmaker(bind=engine)
    session = Session()

    print(polls_trainingcorpus.entryId)


update_web_scraper_log()
