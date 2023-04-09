import mysql.connector
import os
from dotenv import load_dotenv
import joblib
import re
import string
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (
    accuracy_score,
    cohen_kappa_score,
    f1_score,
    classification_report,
)
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.naive_bayes import MultinomialNB

# Import the wordcloud library
from wordcloud import WordCloud


# This focus only on the Threat Actor Profile Category in order to try and get an understanding of threats


def classify():
    load_dotenv()
    # Database Connection to Pull Existing Meta Values

    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    query = """SELECT text, textLabel_id from polls_trainingcorpus where textLabel_id = 16"""

    df = pd.read_sql(query, mydb)

    def process_text(text):
        text = str(text).lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = " ".join(text.split())
        return text

    df["clean_text"] = df.text.map(process_text)
    print(df.head())

    # Join the different processed titles together.
    long_string = ",".join(list(df["clean_text"].values))  # Create a WordCloud object
    wordcloud = WordCloud(
        background_color="white",
        max_words=5000,
        contour_width=3,
        contour_color="steelblue",
    )  # Generate a word cloud
    wordcloud.generate(long_string)  # Visualize the word cloud
    wordcloud.to_file("plots/N.png")


classify()
