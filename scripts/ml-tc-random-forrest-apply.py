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
        "SELECT text, textlabel_id FROM polls_trainingcorpus where polls_trainingcorpus.textLabel_id IN (SELECT textLabel_id FROM polls_trainingcorpus GROUP BY textLabel_id HAVING COUNT(*) > 100) and textlabel_id <> 1"
    )
    rows = cur.fetchall()

    # Separate text and labels
    X = [row[0] for row in rows]
    y = [str(row[1]) for row in rows]  # Convert labels to strings

    # Vectorize the text data using TF-IDF
    vectorizer = TfidfVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    # Train the Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_vectorized, y)

    # Save the trained model
    joblib.dump(rf_model, "random_forest_model.pkl")
    joblib.dump(vectorizer, "vectorizer.pkl")

    # Load the trained model and vectorizer
    rf_model = joblib.load("random_forest_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    # Fetch new and unclassified text from the database
    cur.execute("SELECT text FROM polls_trainingcorpus where textlabel_id = 1")
    rows = cur.fetchall()

    # Separate the text from the rows
    new_texts = [row[0] for row in rows]

    # Vectorize the new text data using the fitted TF-IDF vectorizer
    X_new_vectorized = vectorizer.transform(new_texts)

    # Apply the model to new data and filter by score threshold
    scores = rf_model.predict_proba(X_new_vectorized)
    predicted_labels = rf_model.classes_[scores.argmax(axis=1)]
    predicted_scores = scores.max(axis=1)
    threshold = 0.9  # Set the desired score threshold

    # Filter instances based on score threshold
    filtered_texts = [
        text for text, score in zip(new_texts, predicted_scores) if score >= threshold
    ]
    filtered_labels = [
        label
        for label, score in zip(predicted_labels, predicted_scores)
        if score >= threshold
    ]

    # Print the filtered text and predicted labels
    for text, label in zip(filtered_texts, filtered_labels):
        print("Text:", text)
        print("Predicted Label:", label)
        print()

    # Close the database connection
    cur.close()
    mydb.close()


classify()
