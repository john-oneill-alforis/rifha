import gensim
from gensim import corpora, models
import mysql.connector
import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from string import punctuation


from dotenv import load_dotenv




def topic_generate():

    nltk.download('punkt')
    nltk.download('stopwords')

    load_dotenv()


    wordList = []

    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",  
        user=(os.getenv("db_user")),  
        password=(os.getenv("db_password")),  
        database="thesis_vert",  
    )

    # Create a cursor to interact with the database
    cursor = cnx.cursor()

    # Execute the query for the first data series
    query1 = """SELECT secondary_answer_text FROM polls_transcriptcapture
                WHERE question_id = 3;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    responseData = cursor.fetchall()

    newStopwords = ["I","%","s","m","We","suppose","yeah","60","So","d","'s","The","n't","'re"]

    stpwrd = stopwords.words('english')

    stpwrd.extend(newStopwords)

    for x in responseData:
        text = x[0]
        tokenisedText = word_tokenize(text)
        for item in tokenisedText:
            if item not in stpwrd:
                wordList.append(item)



    print(wordList)




    


topic_generate()
    

    