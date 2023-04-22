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


def classify():
    load_dotenv()
    # Database Connection to Pull Existing Meta Values

    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    query = """SELECT text,textLabel_id, label FROM polls_trainingCorpus inner join polls_textlabels ON polls_textlabels.entryId = polls_trainingcorpus.textLabel_id where polls_trainingcorpus.textLabel_id IN (8, 16, 15)"""

    df = pd.read_sql(query, mydb)

    def process_text(text):
        text = str(text).lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
        text = " ".join(text.split())
        return text

    df["clean_text"] = df.text.map(process_text)
    print(df.head())

    df_train, df_test = train_test_split(
        df, test_size=0.3, random_state=123, stratify=df.label
    )

    vec = CountVectorizer(
        ngram_range=(1, 3),
        stop_words="english",
    )

    X_train = vec.fit_transform(df_train.clean_text)
    X_test = vec.transform(df_test.clean_text)

    y_train = df_train.label
    y_test = df_test.label

    nb = MultinomialNB()
    nb.fit(X_train, y_train)

    preds = nb.predict(X_test)
    print(classification_report(y_test, preds))


classify()
