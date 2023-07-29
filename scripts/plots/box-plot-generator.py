import matplotlib.pyplot as plt
from pathlib import Path
import os
import mysql.connector
from dotenv import load_dotenv




def box_plot_generate():

    load_dotenv()

    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",  
        user=(os.getenv("db_user")),  
        password=(os.getenv("db_password")),  
        database="thesis_vert",  
    )

    

    # Path data to save to the plots folder
    toplevel_path = Path(__file__).parents[2]

    # Create a cursor to interact with the database
    cursor = cnx.cursor()

    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 1;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 1;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 1;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 1;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="orange", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 1 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("orange")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-1.png")
    #plt.show()


    ########################################################################
    # Plots for Question Two 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 2;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 2;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 2;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 2;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 2 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-2.png")


    ########################################################################
    # Plots for Question Four 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 4;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 4;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 4;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 4;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 4 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-4.png")


    ########################################################################
    # Plots for Question Five 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 5;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 5;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 5;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 5;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 5 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-5.png")


    ########################################################################
    # Plots for Question Six 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 6;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 6;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 6;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 6;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 6 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-6.png")


    ########################################################################
    # Plots for Question Seven 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 7;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 7;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 7;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 7;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 7 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-7.png")

    ########################################################################
    # Plots for Question Eight 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 8;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 8;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 8;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 8;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 8 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-8.png")


    ########################################################################
    # Plots for Question Nine 
    ########################################################################


    # Execute the query for the first data series
    query1 = """SELECT positivity_score FROM polls_transcriptcapture
                WHERE question_id = 9;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    list1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    
    # Execute the query for the second data series
    query2 =  """SELECT neutrality_score FROM polls_transcriptcapture
                WHERE question_id = 9;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list2 = [row[0] for row in rows2]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query3 =  """SELECT negativity_score FROM polls_transcriptcapture
                WHERE question_id = 9;"""

    cursor.execute(query3)

    # Fetch the data for the second data series
    rows3 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list3 = [row[0] for row in rows3]  # Assuming x values are in the first column


    # Execute the query for the second data series
    query4 =  """SELECT compound_score FROM polls_transcriptcapture
                WHERE question_id = 9;"""

    cursor.execute(query4)

    # Fetch the data for the second data series
    rows4 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    list4 = [row[0] for row in rows4]  # Assuming x values are in the first column


     # Labels for each list
    labels = ["Positivity Score", "Neutrality Score", "Negativity Score", "Compound Score"]

    # Combine the lists into one list of lists
    data_lists = [list1, list2, list3, list4]

    print(list1,list2,list3,list4)


   # Create the horizontal box plot
    plt.figure(figsize=(12, 6))  # Optional: Adjust the figure size as needed

    box_props = dict(facecolor="blue", edgecolor="black")  # Customize box color and edge color

    # Fill the boxes with the specified color
    bplot = plt.boxplot(data_lists, vert=False, labels=labels, patch_artist=True, boxprops=box_props)

    plt.xlabel("Values")
    plt.ylabel("Sentiment")
    plt.title("Interview Question 9 - Response Values")

    # Custom legend for the filled boxes
    for patch in bplot['boxes']:
        patch.set_facecolor("blue")

        # Explicitly show the plot
        
    plt.savefig(toplevel_path / "mysite/static/plots/box-question-9.png")

box_plot_generate()
