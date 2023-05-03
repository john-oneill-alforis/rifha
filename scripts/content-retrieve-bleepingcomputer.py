import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv
import requests
import hashlib
from sqlalchemy import insert
from sqlalchemy.orm import Session, sessionmaker
import sys
import os
import sqlalchemy as db


def get_rss():
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

    veris_error_capture = db.Table("polls_errorcapture", metadata, autoload_with=engine)
    veris_error_capture = metadata.tables["polls_errorcapture"]

    polls_trainingcorpus = db.Table(
        "polls_trainingcorpus", metadata, autoload_with=engine
    )
    polls_trainingcorpus = metadata.tables["polls_trainingcorpus"]

    try:
        now = datetime.now().replace(microsecond=0).isoformat()

        # Database Connection to Pull Existing Meta Values
        mydb = mysql.connector.connect(
            user=(os.getenv("db_user")),
            password=(os.getenv("db_password")),
            host="localhost",
            database="thesis_vert",
        )

        # Provide a user agent as good practice
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36"
        }

        rss_url = "https://www.bleepingcomputer.com/feed/"

        rss_data = feedparser.parse(rss_url)
        item_count = []

        for x in rss_data["entries"]:
            response = requests.get(x["id"], headers=headers)

            source = "Bleeping Computer"
            publishedDate = x["published"]
            author = x["author"]
            link = x["link"]
            dateAdded = now
            linkHash = hashlib.sha256(link.encode()).hexdigest()
            # print(linkHash)

            # Convert The Date Published TimeStamp

            date_time_str = publishedDate
            date_time_str = date_time_str[:-15]

            publishedDate = datetime.strptime(date_time_str, "%a, %d %b %Y")

            # parse the HTML content of the page with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Ugly way of doing this - need to find something a little more efficient
            # than three seperate loops
            for x in soup.find_all("div", {"class": "cz-related-article-wrapp"}):
                x.decompose()

            for x in soup.find_all("h3"):
                x.decompose()

            for x in soup.find_all("h2"):
                x.decompose()

            intial_text = soup.findAll("div", {"class": "articleBody"})[0].text
            # print(intial_text)

            # Database writes

            sql = """INSERT IGNORE INTO polls_trainingcorpus (source , author, publishedDate, dateAdded, link, text, linkHash, textLabel_Id) 
                                values (%s, %s, %s, %s, %s, %s, %s, %s);"""

            val = (
                (source),
                (author),
                (publishedDate),
                (dateAdded),
                (link.strip()),
                (intial_text.strip()),
                (linkHash),
                (1),
            )

            mycursor = mydb.cursor()
            mycursor.execute(sql, val)

            mydb.commit()
            mydb.get_row

        Session = sessionmaker(bind=engine)
        session = Session()

        today = datetime.today().strftime("%Y-%m-%d")
        count = (
            session.query(polls_trainingcorpus)
            .filter_by(dateAdded=today, source="Bleeping Computer")
            .count()
        )
        print(count)

        query = insert(web_scraper_log).values(
            source=source,
            article_count=count,
            date=datetime.now(),
        )

        conn.execute(query)
        conn.commit()

    except:
        # print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.now())
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        query = insert(veris_error_capture).values(
            execution_type=exc_type,
            execution_object=exc_obj,
            file_name=fname,
            file_line=exc_tb.tb_lineno,
            date=datetime.now(),
        )

        conn.execute(query)
        conn.commit()


get_rss()
