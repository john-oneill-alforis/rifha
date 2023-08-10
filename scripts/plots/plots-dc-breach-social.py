import mysql.connector
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from pathlib import Path


def classify():
    load_dotenv()

    # Path data to save to the plots folder
    toplevel_path = Path(__file__).parents[2]


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
        """SELECT polls_trainingcorpus.entryId, polls_trainingcorpus.text FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (18);"""
    )

    records = cur.fetchall()

    record_ids = [record[0] for record in records]
    record_texts = [record[1] for record in records]    

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(record_texts)

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Create a heatmap
    plt.figure(figsize=(8, 6))
    heatmap = plt.imshow(cosine_similarities, cmap="YlGnBu")

    # Set x and y labels with record IDs
    plt.xticks(range(len(record_ids)), record_ids, rotation=90, fontsize=8)
    plt.yticks(range(len(record_ids)), record_ids, fontsize=8)

    plt.title("Breach Incidents Similarity - Social Engineering Involvement")
    plt.colorbar(heatmap)
    plt.tight_layout()

    plt.savefig(toplevel_path / "plots/comparison_matrix_breach_social.png")
    plt.show()


    







    # Close the database connection
    cur.close()
    mydb.close()


classify()
