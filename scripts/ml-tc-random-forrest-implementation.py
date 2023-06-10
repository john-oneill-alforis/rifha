import mysql.connector
import os
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib
import re
import time


def classify():
    load_dotenv()
    # Database Connection to Pull Existing Meta Values

    mydb = mysql.connector.connect(
        user=(os.getenv("db_user")),
        password=(os.getenv("db_password")),
        host="localhost",
        database="thesis_vert",
    )

    cur = mydb.cursor()

    # Load the trained random forest model
    model = joblib.load("random_forest_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    # Retrieve the unclassified text entries from the database
    cur.execute("SELECT entryId, text FROM polls_trainingcorpus WHERE textLabel_id = 1")
    results = cur.fetchall()

    for entryId, text in results:
        # Preprocess the text by removing newline characters and other unwanted characters
        new_text = re.sub(r"\n", " ", text)
        processed_text = new_text.replace("'", "")
        # Add any additional preprocessing steps as necessary

        if processed_text.strip():  # Skip empty or whitespace-only text
            # Vectorize the text using the same vectorizer used during training
            text_vector = vectorizer.transform([processed_text])

            # Make predictions using the model
            prediction = model.predict(text_vector)
            confidence = model.predict_proba(text_vector).max()

            new_cat = prediction.item()

            # Update the database if confidence is above 90%
            if confidence >= 0.7:
                sql = """UPDATE polls_trainingcorpus SET textLabel_id = %s WHERE entryId = %s"""

                # Commit the changes if necessary

                val = (
                    new_cat,
                    entryId,
                )

                cur.execute(sql, val)
                mydb.commit()

            if confidence >= 0.7:
                # Print the results or perform any other desired actions
                print(
                    "Entry {entryId}: Predicted label {prediction} with confidence {confidence}"
                )

                # time.sleep(1)  # Seconds


classify()
