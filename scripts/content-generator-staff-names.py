import random
import sys
import os
import mysql.connector
import sqlalchemy as db
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import insert
import uuid


def generate_staff_information():
    # Connect to the Database to creat the DB engine
    engine = db.create_engine(
        "mysql://"
        + (os.getenv("db_user"))
        + ":"
        + (os.getenv("db_password"))
        + "@localhost/thesis_vert"
    )

    conn = engine.connect()
    metadata = db.MetaData()

    # Load the table which will hold the staff information
    staff_table = db.Table("rifha_staff", metadata, autoload_with=engine)
    staff_table = metadata.tables["rifha_staff"]

    # Creat some lists to hold the contents of the names taken from the txt files
    first_name_pool = []
    surname_pool = []

    # Loop through the files - add the entry to the list, cleaned first with the strip
    # function
    with open(os.path.join(sys.path[0], "firstNames.txt"), "r") as firstNames_file:
        contents = firstNames_file.readlines()

        for x in contents:
            first_name_pool.append(x.strip())

    with open(os.path.join(sys.path[0], "lastNames.txt"), "r") as lastNames_file:
        contents = lastNames_file.readlines()

        for x in contents:
            surname_pool.append(x.strip())

    # Generate 35 Names in the database and assign them the default job role

    for _ in range(35):
        first_name = random.choice(first_name_pool)
        surname = random.choice(surname_pool)
        full_name = first_name + " " + surname
        email = (first_name + "." + surname + "@noemail.org").replace("’", "").lower()

        prefix = "+3538"
        first_digit = str(random.choice([5, 6, 7, 9]))
        remaining_digits = "".join([str(random.randint(0, 9)) for i in range(7)])
        random_mobile_number = prefix + first_digit + remaining_digits

        Session = sessionmaker(bind=engine)
        session = Session()

        query = insert(staff_table).values(
            staffId=uuid.uuid4(),
            firstName=first_name,
            lastName=surname,
            email=email,
            contactNumber=random_mobile_number,
            jobTitle_id="040f86432c8246b39cd46e095b74b9f9",
        )

        conn.execute(query)
        conn.commit()


generate_staff_information()
