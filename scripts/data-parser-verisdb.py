from pathlib import Path
import json
import sqlalchemy as db
import os
from dotenv import load_dotenv
from sqlalchemy import insert
from sqlalchemy.orm import Session, sessionmaker
import sys
from datetime import datetime


def process_veris_information():
    load_dotenv()
    # Load up the database

    engine = db.create_engine(
        "mysql+mysqldb://"
        + (os.getenv("db_user"))
        + ":"
        + (os.getenv("db_password"))
        + "@localhost/thesis_vert"
    )
    conn = engine.connect()
    metadata = db.MetaData()

    Session = sessionmaker(bind=engine)

    ############################################################
    # Load the Database Tables we will need for the insertion
    ############################################################

    veris = db.Table("polls_veris_incident_details", metadata, autoload_with=engine)
    veris = metadata.tables["polls_veris_incident_details"]

    veris_error_capture = db.Table("polls_errorcapture", metadata, autoload_with=engine)
    veris_error_capture = metadata.tables["polls_errorcapture"]

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[1]

    ############################################################
    # Concat paths for both the submitted and validated folders
    ############################################################
    veris_validated_data = toplevel_path / "veris-data/data/json/validated"

    # Grab the data from the validated reports

    malware_couter = []

    for p in veris_validated_data.rglob("*.json"):
        # Load the data from the json file
        json_file = veris_validated_data / p.name

        data = json.loads(json_file.read_bytes())

        incident_uuid = data["incident_id"].lower()

        ########################################################
        # Code block to write the initial incident data
        ########################################################

        try:
            created_time_str = data["plus"]["created"][0:10]
            created_date_obj = datetime.strptime(created_time_str, "%Y-%m-%d")

            query = (
                insert(veris)
                .prefix_with("ignore")
                .values(
                    incident_id=incident_uuid,
                    security_incident=data["security_incident"],
                    source_id=data.get(("source_id"), "None"),
                    summary=data["summary"],
                    analysis_status=data.get("plus", {}).get("analysis_status", "None"),
                    created=created_date_obj,
                    master_id=data["plus"]["master_id"].lower(),
                    modified=data["plus"]["modified"],
                )
            )

            conn.execute(query)
            conn.commit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.now())
            query = insert(veris_error_capture).values(
                execution_type=exc_type,
                execution_object=exc_obj,
                file_name=fname,
                file_line=exc_tb.tb_lineno,
                date=datetime.now(),
            )

            conn.execute(query)
            conn.commit()

        ###########################################################
        # Code block to write the incident action - 'malware' data
        ###########################################################

        polls_veris_action_malware = db.Table(
            "polls_veris_action_malware", metadata, autoload_with=engine
        )
        polls_veris_action_malware_notes = db.Table(
            "polls_veris_action_malware_notes", metadata, autoload_with=engine
        )
        polls_veris_action_malware_variety = db.Table(
            "polls_veris_action_malware_variety", metadata, autoload_with=engine
        )
        polls_veris_action_malware_vector = db.Table(
            "polls_veris_action_malware_vector", metadata, autoload_with=engine
        )

        try:
            for attack_method in data["action"].keys():
                if attack_method == "malware":
                    malware_couter.append(incident_uuid)

                    malware_name = data["action"]["malware"].get(
                        "name", "No Malware Name"
                    )
                    cve = data["action"]["malware"].get("cve", "No CVE Data")
                    notes = data["action"]["malware"].get("notes", "No Notes Data")

                    query = insert(polls_veris_action_malware).values(
                        incident_id=incident_uuid,
                        name=malware_name,
                        cve=cve,
                        notes=notes,
                    )

                    result = conn.execute(query)
                    vam_id = result.inserted_primary_key[0]
                    conn.commit()

                    if "variety" in data["action"]["malware"]:
                        for x in data["action"]["malware"]["variety"]:
                            print(x + " " + incident_uuid + " - variety")
                            query = insert(polls_veris_action_malware_variety).values(
                                variety=x,
                                name=malware_name,
                                vam_Id_id=vam_id,
                            )

                        result = conn.execute(query)
                        conn.commit()

                    """if "vector" in data["action"]["malware"]:
                        for x in data["action"]["malware"]["vector"]:
                            #print(x + " " + incident_uuid + " - vector")"""

                else:
                    pass

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.now())
            query = insert(veris_error_capture).values(
                execution_type=exc_type,
                execution_object=exc_obj,
                file_name=fname,
                file_line=exc_tb.tb_lineno,
                date=datetime.now(),
            )

            conn.execute(query)
            conn.commit()


process_veris_information()
