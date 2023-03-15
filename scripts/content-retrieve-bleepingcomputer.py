import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector
import os
from dotenv import load_dotenv
import requests
import hashlib


def get_rss():
    load_dotenv()
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

    for x in rss_data["entries"]:
        response = requests.get(x["id"], headers=headers)

        source = "Bleeping Computer"
        publishedDate = x["published"]
        author = x["author"]
        link = x["link"]
        dateAdded = now
        linkHash = hashlib.sha256(link.encode()).hexdigest()

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
        print(intial_text)

        # Database writes

        sql = """INSERT IGNORE INTO polls_trainingcorpus (source , author, publishedDate, dateAdded, link, text, linkHash) 
                            values (%s, %s, %s, %s, %s, %s, %s);"""
        val = (
            (source),
            (author),
            (publishedDate),
            (dateAdded),
            (link.strip()),
            (intial_text.strip()),
            (linkHash),
        )

        mycursor = mydb.cursor()
        mycursor.execute(sql, val)

        mydb.commit()


get_rss()
