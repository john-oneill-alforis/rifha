from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd
import sqlalchemy as db
import os
from dotenv import load_dotenv
from sqlalchemy import insert
from sqlalchemy.orm import Session
import sys
import datetime


def process_veris_information():
    load_dotenv()
    # Load up the database
    try:
        engine = db.create_engine(
            "mysql+mysqldb://"
            + (os.getenv("db_user"))
            + ":"
            + (os.getenv("db_password"))
            + "@localhost/thesis_vert"
        )
        conn = engine.connect()
        metadata = db.MetaData()

        # Load the Database Tables we will need for the insertion
        veris = db.Table("veris_test", metadata, autoload_with=engine)
        veris_action = db.Table("veris_test_action", metadata, autoload_with=engine)
        veris_action_meta = db.Table(
            "veris_test_action_meta", metadata, autoload_with=engine
        )
        veris_victim = db.Table("veris_test_victim", metadata, autoload_with=engine)
        veris_victim_meta = db.Table(
            "veris_test_victim_meta", metadata, autoload_with=engine
        )

        veris_actor = db.Table("veris_test_actor", metadata, autoload_with=engine)
        veris_actor_meta = db.Table(
            "veris_test_actor_meta", metadata, autoload_with=engine
        )

        veris = metadata.tables["veris_test"]
        veris_action = metadata.tables["veris_test_action"]

        veris_victim = metadata.tables["veris_test_victim"]
        veris_victim_meta = metadata.tables["veris_test_victim_meta"]

        veris_actor = metadata.tables["veris_test_actor"]
        veris_actor_meta = metadata.tables["veris_test_actor_meta"]

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

    cursor = conn.cursor()
    cursor.execute("SELECT text FROM polls_trainingcorpus")
    articles = cursor.fetchall()

    # Step 2: Text preprocessing (assuming basic preprocessing steps)
    preprocessed_articles = [
        article[0].lower() for article in articles
    ]  # Convert to lowercase

    # Step 3: Vectorize the text
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(preprocessed_articles)

    # Step 4: Compute similarity matrix
    similarity_matrix = cosine_similarity(vectors)

    # Step 5: Visualize the similarity matrix
    plt.imshow(similarity_matrix, cmap="hot", interpolation="nearest")
    plt.colorbar()
    plt.title("Article Similarity")
    plt.xlabel("Article ID")
    plt.ylabel("Article ID")
    plt.show()


process_veris_information()
