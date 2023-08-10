import mysql.connector
import os
from dotenv import load_dotenv
from transformers import (
    BertTokenizer,
    TFBertForSequenceClassification,
)
import pandas as pd
import torch
import numpy as np
from transformers import BertTokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


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

    query = """SELECT text, label FROM polls_trainingcorpus JOIN polls_textlabels ON polls_trainingcorpus.textLabel_id = polls_textlabels.entryId WHERE polls_trainingcorpus.textLabel_id IN (2,8,11);"""

    df = pd.read_sql(query, mydb)

    # Split data into training and validation sets
    train_df = df.sample(frac=0.8, random_state=42)
    val_df = df.drop(train_df.index)

    # Load BERT tokenizer
    tokenizer = BertTokenizer.from_pretrained("bert-base-uncased", do_lower_case=True)

    # Tokenize text and convert labels to integers
    train_encodings = tokenizer(
        train_df["text"].tolist(), truncation=True, padding=True
    )
    val_encodings = tokenizer(val_df["text"].tolist(), truncation=True, padding=True)
    train_labels = train_df["label"].astype(int).tolist()
    val_labels = val_df["label"].astype(int).tolist()

    # Create TensorFlow datasets
    train_dataset = tf.data.Dataset.from_tensor_slices(
        (dict(train_encodings), train_labels)
    )
    val_dataset = tf.data.Dataset.from_tensor_slices((dict(val_encodings), val_labels))

    # Load pre-trained BERT model
    model = TFBertForSequenceClassification.from_pretrained(
        "bert-base-uncased", num_labels=2
    )

    # Compile model
    optimizer = tf.keras.optimizers.Adam(
        learning_rate=3e-5, epsilon=1e-08, clipnorm=1.0
    )
    model.compile(optimizer=optimizer, loss=model.compute_loss, metrics=["accuracy"])

    # Train model
    history = model.fit(
        train_dataset.batch(32), epochs=3, validation_data=val_dataset.batch(32)
    )

    # Evaluate model on validation set
    results = model.evaluate(val_dataset.batch(32))
    print("Validation accuracy: {:.2f}%".format(results[1] * 100))


classify()
