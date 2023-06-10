import mysql.connector
import os
from dotenv import load_dotenv
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib


def classify():
    load_dotenv()
    # Database Connection to Pull Existing Meta Values

    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    # Cursor to execute SQL queries
    cur = mydb.cursor()

    # Fetch data from the database
    cur.execute(
        """SELECT text, textLabel_id FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (2,8,11,16);"""
    )
    rows = cur.fetchall()

    # Separate text and labels
    X = [row[0] for row in rows]
    y = [row[1] for row in rows]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Vectorize the text data using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    # Train the Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train_vectorized, y_train)

    # Make predictions on the test set
    y_pred = rf_model.predict(X_test_vectorized)

    # Generate the classification report
    report = classification_report(y_test, y_pred)

    print(report)

    joblib.dump(rf_model, "random_forest_model_cat2.pkl")
    joblib.dump(vectorizer, "vectorizer_cat2.pkl")

    # Close the database connection
    cur.close()
    mydb.close()


classify()
