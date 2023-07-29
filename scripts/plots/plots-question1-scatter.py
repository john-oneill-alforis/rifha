import mysql.connector
import matplotlib.pyplot as plt
import os
from pathlib import Path


def create_scatter():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",  # Replace with the appropriate host
        user=(os.getenv("db_user")),  # Replace with your MySQL username
        password=(os.getenv("db_password")),  # Replace with your MySQL password
        database="thesis_vert",  # Replace with your database name
    )

    # Path data to save to the plots folder
    toplevel_path = Path(__file__).parents[1]

    # Create a cursor to interact with the database
    cursor = cnx.cursor()

    # Execute the query for the first data series
    query1 = """SELECT i.interviewee_id, r.positivity_score FROM polls_interviewee AS i
                JOIN polls_intervieweeresponse AS r ON i.interviewee_id = r.interviewee_id_id
                WHERE r.question_id_id = 1;"""

    cursor.execute(query1)

    # Fetch the data for the first data series
    rows1 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the first data series
    x_values1 = [row[0] for row in rows1]  # Assuming x values are in the first column
    y_values1 = [row[1] for row in rows1]  # Assuming y values are in the second column

    # Execute the query for the second data series
    query2 = """SELECT i.interviewee_id, r.neutrality_score FROM polls_interviewee AS i
                JOIN polls_intervieweeresponse AS r ON i.interviewee_id = r.interviewee_id_id
                WHERE r.question_id_id = 1;"""

    cursor.execute(query2)

    # Fetch the data for the second data series
    rows2 = cursor.fetchall()

    # Extract the x and y coordinates from the fetched data for the second data series
    x_values2 = [row[0] for row in rows2]  # Assuming x values are in the first column
    y_values2 = [row[1] for row in rows2]  # Assuming y values are in the second column

    # Create a scatter plot with the first data series
    plt.scatter(x_values1, y_values1, label="Positivity")

    # Add the second data series as another scatter plot
    plt.scatter(x_values2, y_values2, label="Neutrality")

    # Set the labels and title
    plt.xlabel("Interviewee ID")
    plt.ylabel("Score")
    plt.title("Process Confidence")

    # Display legend
    plt.legend()

    # Remove x-axis tick labels
    plt.xticks([])

    # Show the plot
    plt.savefig(toplevel_path / "plots/1.png")

    # Close the cursor and database connection
    cursor.close()
    cnx.close()


create_scatter()
