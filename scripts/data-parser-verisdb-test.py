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

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[1]

    ############################################################
    # Concat paths for both the submitted and validated folders
    ############################################################
    veris_validated_data = toplevel_path / "veris-data/data/json/validated"

    # Grab the data from the validated reports

    incident_id = ""
    for p in veris_validated_data.rglob("*.json"):
        # Load the data from the json file
        json_file = veris_validated_data / p.name

        data = json.loads(json_file.read_bytes())

        ########################################################
        # Code block to write the initial incident data
        ########################################################

        try:
            query = (
                insert(veris)
                .prefix_with("ignore")
                .values(
                    incident_id=data["incident_id"].lower(),
                    security_incident=data["security_incident"],
                    source_id=data.get(("source_id"), "None"),
                    summary=data["summary"],
                    analysis_status=data.get("plus", {}).get("analysis_status", "None"),
                    created=data["plus"]["created"],
                    master_id=data["plus"]["master_id"].lower(),
                    modified=data["plus"]["modified"],
                )
            )
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

        try:
            # print(query)
            conn.execute(query)
            conn.commit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

        ########################################################
        # Code block to write the incident action data to the DB
        ########################################################

        try:
            for attack_method in data["action"].keys():
                # print(x)
                query = insert(veris_action).values(
                    incident_id=data["incident_id"].lower(),
                    action=attack_method,
                )

                result = conn.execute(query)
                method_id = result.lastrowid
                conn.commit()

                # Code block to write the attack methods decsriptions to a table
                for k, v in data["action"][attack_method].items():
                    if type(v) == list:
                        for meta in v:
                            # print(method_id, k, meta)
                            query = insert(veris_action_meta).values(
                                veris_test_action_ref=method_id,
                                key=k,
                                data=meta,
                            )
                    else:
                        query = insert(veris_action_meta).values(
                            veris_test_action_ref=method_id,
                            key=k,
                            data=v,
                        )

                    result = conn.execute(query)
                    conn.commit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

        ########################################################
        # Code block to write the incident victim data to the DB
        ########################################################

        try:
            if "victim_id" in data["victim"]:
                query = insert(veris_victim).values(
                    incident_id=data["incident_id"].lower(),
                    victim=data["victim"]["victim_id"],
                )

            else:
                query = insert(veris_victim).values(
                    incident_id=data["incident_id"].lower(),
                    victim="anonymous",
                )

            result = conn.execute(query)
            actor_id = result.lastrowid
            conn.commit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(
                exc_type,
                exc_obj,
                fname,
                exc_tb.tb_lineno,
                datetime.datetime.now(),
                data["incident_id"].lower(),
            )

        ########################################################
        # Code block to write the actor data to the DB
        ########################################################

        try:
            for actor_type in data["actor"].keys():
                # print(x)
                query = insert(veris_actor).values(
                    incident_id=data["incident_id"].lower(),
                    actor=actor_type,
                )

                result = conn.execute(query)
                actor_id = result.lastrowid
                conn.commit()

                # Code block to write the attack methods decsriptions to a table
                for k, v in data["actor"][actor_type].items():
                    if type(v) == list:
                        # print("list")
                        for meta in v:
                            # print(method_id, k, meta)
                            query = insert(veris_actor_meta).values(
                                veris_test_actor_ref=actor_id,
                                key=k,
                                data=meta,
                            )
                    else:
                        query = insert(veris_actor_meta).values(
                            veris_test_actor_ref=actor_id,
                            key=k,
                            data=v,
                        )

                    result = conn.execute(query)
                    conn.commit()

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())


process_veris_information()
