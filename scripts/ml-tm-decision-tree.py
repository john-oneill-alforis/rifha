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
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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

    # query = """SELECT * FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (
    #        SELECT textLabel_id FROM polls_trainingcorpus GROUP BY textLabel_id HAVING COUNT(*) > 100);"""

    query = """SELECT * FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (SELECT textLabel_id FROM polls_trainingcorpus GROUP BY textLabel_id HAVING COUNT(*) > 100)  AND textLabel_id <> 1;"""

    df = pd.read_sql(query, mydb)

    # Split the dataset into train and test sets
    train_data, test_data, train_labels, test_labels = train_test_split(
        df["text"], df["label"], test_size=0.3, random_state=42
    )

    # Create a TF-IDF vectorizer object
    vectorizer = TfidfVectorizer()

    # Vectorize the train and test sets
    train_vectors = vectorizer.fit_transform(train_data)
    test_vectors = vectorizer.transform(test_data)

    # Train a decision tree classifier on the vectorized data
    classifier = DecisionTreeClassifier()
    classifier.fit(train_vectors, train_labels)

    # Predict the labels for the test set
    predicted_labels = classifier.predict(test_vectors)

    # Calculate the accuracy of the classifier
    accuracy = accuracy_score(test_labels, predicted_labels)
    print("Accuracy:", accuracy)


classify()
