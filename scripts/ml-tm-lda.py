import mysql.connector
import os
from dotenv import load_dotenv
import re
import string
import numpy as np
import pandas as pd
import gensim
from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess


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

    query = """SELECT * FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (SELECT textLabel_id FROM polls_trainingcorpus GROUP BY textLabel_id HAVING COUNT(*) > 100)  AND textLabel_id <> 1;"""

    df = pd.read_sql(query, mydb)

    # Define the number of topics for LDA
    num_topics = 10

    # Preprocess the text column
    data = df["text"].map(simple_preprocess)

    # Create a dictionary from the preprocessed text
    dictionary = corpora.Dictionary(data)

    # Create a corpus from the dictionary and preprocessed text
    corpus = [dictionary.doc2bow(doc) for doc in data]

    # Train the LDA model
    lda_model = LdaModel(
        corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=42
    )

    # Get the accuracy prediction
    accuracy = lda_model.log_perplexity(corpus)
    print(f"Accuracy: {accuracy}")


classify()
