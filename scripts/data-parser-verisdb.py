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

    Session = sessionmaker(bind=engine)
    session = Session()

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
            modified_time_str = data["plus"]["modified"][0:10]
            created_date_obj = datetime.strptime(created_time_str, "%Y-%m-%d")
            modified_date_obj = datetime.strptime(modified_time_str, "%Y-%m-%d")

            query = insert(veris).values(
                incident_id=incident_uuid,
                security_incident=data["security_incident"],
                source_id=data.get(("source_id"), "None"),
                summary=data["summary"],
                analysis_status=data.get("plus", {}).get("analysis_status", "None"),
                created=created_date_obj,
                master_id=data["plus"]["master_id"].lower(),
                modified=modified_date_obj,
            )

            conn.execute(query)
            conn.commit()

            parse_incident_details(incident_uuid, data)

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

        def parse_incident_details(incident_identifier, json_data):
            # print(incident_identifier, json_data)

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
            polls_veris_action_malware_results = db.Table(
                "polls_veris_action_malware_results", metadata, autoload_with=engine
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
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_malware_variety
                                ).values(
                                    variety=x,
                                    name=malware_name,
                                    vam_Id_id=vam_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["malware"]:
                            for x in data["action"]["malware"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(
                                    polls_veris_action_malware_vector
                                ).values(
                                    vector=x,
                                    vam_Id_id=vam_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["malware"]:
                            for x in data["action"]["malware"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_malware_results
                                ).values(
                                    result=x,
                                    vam_Id_id=vam_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident action - 'hacking' data
            ###########################################################

            polls_veris_action_hacking = db.Table(
                "polls_veris_action_hacking", metadata, autoload_with=engine
            )

            polls_veris_action_hacking_variety = db.Table(
                "polls_veris_action_hacking_variety", metadata, autoload_with=engine
            )
            polls_veris_action_hacking_vector = db.Table(
                "polls_veris_action_hacking_vector", metadata, autoload_with=engine
            )
            polls_veris_action_hacking_results = db.Table(
                "polls_veris_action_hacking_results", metadata, autoload_with=engine
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "hacking":
                        cve = data["action"]["hacking"].get("cve", "No CVE Data")
                        notes = data["action"]["hacking"].get("notes", "No Notes Data")

                        query = insert(polls_veris_action_hacking).values(
                            incident_id=incident_uuid,
                            cve=cve,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vah_id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["hacking"]:
                            for x in data["action"]["hacking"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_hacking_variety
                                ).values(
                                    variety=x,
                                    vah_Id_id=vah_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["hacking"]:
                            for x in data["action"]["hacking"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(
                                    polls_veris_action_hacking_vector
                                ).values(
                                    vector=x,
                                    vah_Id_id=vah_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["hacking"]:
                            for x in data["action"]["hacking"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_hacking_results
                                ).values(
                                    results=x,
                                    vah_Id_id=vah_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident action - 'social' data
            ###########################################################

            polls_veris_action_social = db.Table(
                "polls_veris_action_social", metadata, autoload_with=engine
            )

            polls_veris_action_social_variety = db.Table(
                "polls_veris_action_social_variety", metadata, autoload_with=engine
            )
            polls_veris_action_social_vector = db.Table(
                "polls_veris_action_social_vector", metadata, autoload_with=engine
            )
            polls_veris_action_social_results = db.Table(
                "polls_veris_action_social_results", metadata, autoload_with=engine
            )
            polls_veris_action_social_target = db.Table(
                "polls_veris_action_social_target", metadata, autoload_with=engine
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "social":
                        notes = data["action"]["social"].get("notes", "No Notes Data")

                        query = insert(polls_veris_action_social).values(
                            incident_id=incident_uuid,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vas_id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["social"]:
                            for x in data["action"]["social"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_social_variety
                                ).values(
                                    variety=x,
                                    vas_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["social"]:
                            for x in data["action"]["social"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(polls_veris_action_social_vector).values(
                                    vector=x,
                                    vas_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["social"]:
                            for x in data["action"]["social"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_social_results
                                ).values(
                                    results=x,
                                    vas_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "target" in data["action"]["social"]:
                            for x in data["action"]["social"]["target"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(polls_veris_action_social_target).values(
                                    target=x,
                                    vas_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident action - 'misue' data
            ###########################################################

            polls_veris_action_misuse = db.Table(
                "polls_veris_action_misuse", metadata, autoload_with=engine
            )

            polls_veris_action_misuse_variety = db.Table(
                "polls_veris_action_misuse_variety", metadata, autoload_with=engine
            )
            polls_veris_action_misuse_vector = db.Table(
                "polls_veris_action_misuse_vector", metadata, autoload_with=engine
            )
            polls_veris_action_misuse_results = db.Table(
                "polls_veris_action_misuse_results", metadata, autoload_with=engine
            )
            polls_veris_action_misuse_target = db.Table(
                "polls_veris_action_misuse_target", metadata, autoload_with=engine
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "misuse":
                        notes = data["action"]["misuse"].get("notes", "No Notes Data")

                        query = insert(polls_veris_action_misuse).values(
                            incident_id=incident_uuid,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vas_id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["misuse"]:
                            for x in data["action"]["misuse"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_misuse_variety
                                ).values(
                                    variety=x,
                                    vamis_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["misuse"]:
                            for x in data["action"]["misuse"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(polls_veris_action_misuse_vector).values(
                                    vector=x,
                                    vamis_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["misuse"]:
                            for x in data["action"]["misuse"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_misuse_results
                                ).values(
                                    results=x,
                                    vamis_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "target" in data["action"]["misuse"]:
                            for x in data["action"]["misuse"]["target"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(polls_veris_action_misuse_target).values(
                                    target=x,
                                    vamis_Id_id=vas_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident action - 'Physical' data
            ###########################################################

            polls_veris_action_physical = db.Table(
                "polls_veris_action_physical", metadata, autoload_with=engine
            )

            polls_veris_action_physical_variety = db.Table(
                "polls_veris_action_physical_variety", metadata, autoload_with=engine
            )
            polls_veris_action_physical_vector = db.Table(
                "polls_veris_action_physical_vector", metadata, autoload_with=engine
            )
            polls_veris_action_physical_location = db.Table(
                "polls_veris_action_physical_location", metadata, autoload_with=engine
            )
            polls_veris_action_physical_result = db.Table(
                "polls_veris_action_physical_result", metadata, autoload_with=engine
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "physical":
                        notes = data["action"]["physical"].get("notes", "No Notes Data")

                        query = insert(polls_veris_action_physical).values(
                            incident_id=incident_uuid,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vap_id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["physical"]:
                            for x in data["action"]["physical"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_physical_variety
                                ).values(
                                    variety=x,
                                    vap_Id_id=vap_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["physical"]:
                            for x in data["action"]["physical"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(
                                    polls_veris_action_physical_vector
                                ).values(
                                    vector=x,
                                    vap_Id_id=vap_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "target" in data["action"]["physical"]:
                            for x in data["action"]["physical"]["location"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_physical_location
                                ).values(
                                    location=x,
                                    vap_Id_id=vap_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["physical"]:
                            for x in data["action"]["physical"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_physical_result
                                ).values(
                                    result=x,
                                    vap_Id_id=vap_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident action - 'Error' data
            ###########################################################

            polls_veris_action_error = db.Table(
                "polls_veris_action_error", metadata, autoload_with=engine
            )

            polls_veris_action_error_variety = db.Table(
                "polls_veris_action_error_variety", metadata, autoload_with=engine
            )
            polls_veris_action_error_vector = db.Table(
                "polls_veris_action_error_vector", metadata, autoload_with=engine
            )

            polls_veris_action_error_result = db.Table(
                "polls_veris_action_error_result", metadata, autoload_with=engine
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "error":
                        notes = data["action"]["error"].get("notes", "No Notes Data")

                        query = insert(polls_veris_action_error).values(
                            incident_id=incident_uuid,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vae_Id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["error"]:
                            for x in data["action"]["error"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(polls_veris_action_error_variety).values(
                                    variety=x,
                                    vae_Id_id=vae_Id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "vector" in data["action"]["error"]:
                            for x in data["action"]["error"]["vector"]:
                                # print(x + " " + incident_uuid + " - vector")
                                query = insert(polls_veris_action_error_vector).values(
                                    vector=x,
                                    vae_Id_id=vae_Id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "target" in data["action"]["error"]:
                            for x in data["action"]["error"]["location"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_error_location
                                ).values(
                                    location=x,
                                    vae_Id_id=vae_Id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "result" in data["action"]["error"]:
                            for x in data["action"]["error"]["result"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(polls_veris_action_error_result).values(
                                    result=x,
                                    vae_Id_id=vae_Id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ################################################################
            # Code block to write the incident action - 'Environmental' data
            ################################################################

            polls_veris_action_environmental = db.Table(
                "polls_veris_action_environmental", metadata, autoload_with=engine
            )

            polls_veris_action_environmental_variety = db.Table(
                "polls_veris_action_environmental_variety",
                metadata,
                autoload_with=engine,
            )

            try:
                for attack_method in data["action"].keys():
                    if attack_method == "environmental":
                        notes = data["action"]["environmental"].get(
                            "notes", "No Notes Data"
                        )

                        query = insert(polls_veris_action_environmental).values(
                            incident_id=incident_uuid,
                            notes=notes,
                        )

                        result = conn.execute(query)
                        vaenv_Id = result.inserted_primary_key[0]
                        conn.commit()

                        if "variety" in data["action"]["environmental"]:
                            for x in data["action"]["environmental"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(
                                    polls_veris_action_environmental_variety
                                ).values(
                                    variety=x,
                                    vaenv_Id_id=vaenv_Id,
                                )

                            result = conn.execute(query)
                            conn.commit()

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

            ###########################################################
            # Code block to write the incident actor data
            ###########################################################

            veris_actor = db.Table("polls_veris_actor", metadata, autoload_with=engine)

            veris_actor_motive = db.Table(
                "polls_veris_actor_motive", metadata, autoload_with=engine
            )
            veris_actor_variety = db.Table(
                "polls_veris_actor_variety", metadata, autoload_with=engine
            )
            veris_actor_origin = db.Table(
                "polls_veris_actor_origin", metadata, autoload_with=engine
            )

            try:
                for actor_info in data["actor"].keys():
                    if actor_info == "internal":
                        # print("internal")
                        actor_type = "internal"

                        query = insert(veris_actor).values(
                            incident_id=incident_uuid,
                            actor_type=actor_info,
                        )

                        result = conn.execute(query)
                        vat_id = result.inserted_primary_key[0]
                        conn.commit()
                        print(vat_id)

                        if "variety" in data["actor"]["internal"]:
                            for x in data["actor"]["internal"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_variety).values(
                                    variety=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "country" in data["actor"]["internal"]:
                            for x in data["actor"]["internal"]["country"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_origin).values(
                                    origin=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "motive" in data["actor"]["internal"]:
                            for x in data["actor"]["internal"]["motive"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_motive).values(
                                    motive=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                    elif actor_info == "external":
                        # print("external")

                        region = data["actor"]["external"].get("region", "None")
                        industry = data["actor"]["external"].get("industry", "None")
                        notes = data["actor"]["external"].get("notes", "None")

                        query = insert(veris_actor).values(
                            incident_id=incident_uuid,
                            actor_type=actor_info,
                        )

                        result = conn.execute(query)
                        vat_id = result.inserted_primary_key[0]
                        conn.commit()
                        print(vat_id)

                        if "variety" in data["actor"]["external"]:
                            for x in data["actor"]["external"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_variety).values(
                                    variety=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "country" in data["actor"]["external"]:
                            for x in data["actor"]["external"]["country"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_origin).values(
                                    origin=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "motive" in data["actor"]["external"]:
                            for x in data["actor"]["external"]["motive"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_motive).values(
                                    motive=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                    elif actor_info == "partner":
                        # print("partner")

                        query = insert(veris_actor).values(
                            incident_id=incident_uuid,
                            actor_type=actor_info,
                        )

                        result = conn.execute(query)
                        vat_id = result.inserted_primary_key[0]
                        conn.commit()
                        print(vat_id)

                        if "variety" in data["actor"]["partner"]:
                            for x in data["actor"]["partner"]["variety"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_variety).values(
                                    variety=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "country" in data["actor"]["partner"]:
                            for x in data["actor"]["partner"]["country"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_origin).values(
                                    origin=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        if "motive" in data["actor"]["partner"]:
                            for x in data["actor"]["partner"]["motive"]:
                                # print(x + " " + incident_uuid + " - variety")
                                query = insert(veris_actor_motive).values(
                                    motive=x,
                                    vat_Id_id=vat_id,
                                )

                            result = conn.execute(query)
                            conn.commit()

                        else:
                            pass

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(
                    incident_uuid,
                    exc_type,
                    exc_obj,
                    fname,
                    exc_tb.tb_lineno,
                    datetime.now(),
                )
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
            # Code block to write the incident asset data
            ###########################################################

            veris_asset = db.Table("polls_veris_asset", metadata, autoload_with=engine)

            veris_asset_accessibility = db.Table(
                "polls_veris_asset_accessibility", metadata, autoload_with=engine
            )
            veris_asset_cloud = db.Table(
                "polls_veris_asset_cloud", metadata, autoload_with=engine
            )
            veris_asset_hosting = db.Table(
                "polls_veris_asset_hosting", metadata, autoload_with=engine
            )
            veris_asset_management = db.Table(
                "polls_veris_asset_management", metadata, autoload_with=engine
            )
            veris_asset_ownership = db.Table(
                "polls_veris_asset_ownership", metadata, autoload_with=engine
            )
            veris_asset_variety = db.Table(
                "polls_veris_asset_variety", metadata, autoload_with=engine
            )

            try:
                notes = data["asset"].get("notes", "None")

                query = insert(veris_asset).values(
                    incident_id=incident_uuid,
                    notes=notes,
                )

                result = conn.execute(query)
                vass_id = result.inserted_primary_key[0]
                conn.commit()
                # print(vass_id)

                for entry in data["asset"].keys():
                    if entry == "assets":
                        for x in data["asset"]["assets"]:
                            query = insert(veris_asset_variety).values(
                                variety=x["variety"], vass_Id_id=vass_id
                            )

                            result = conn.execute(query)
                            conn.commit()

                    elif entry == "ownership":
                        for x in data["asset"]["ownership"]:
                            query = insert(veris_asset_ownership).values(
                                ownership=x, vass_Id_id=vass_id
                            )

                            result = conn.execute(query)
                            conn.commit()

                    elif entry == "management":
                        for x in data["asset"]["management"]:
                            query = insert(veris_asset_management).values(
                                management=x, vass_Id_id=vass_id
                            )

                            result = conn.execute(query)
                            conn.commit()

                    elif entry == "hosting":
                        for x in data["asset"]["hosting"]:
                            query = insert(veris_asset_hosting).values(
                                hosting=x, vass_Id_id=vass_id
                            )

                            result = conn.execute(query)
                            conn.commit()

                    elif entry == "hosting":
                        for x in data["asset"]["hosting"]:
                            query = insert(veris_asset_hosting).values(
                                hosting=x, vass_Id_id=vass_id
                            )

                            result = conn.execute(query)
                            conn.commit()

                        else:
                            pass

            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(
                    incident_uuid,
                    exc_type,
                    exc_obj,
                    fname,
                    exc_tb.tb_lineno,
                    datetime.now(),
                )
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
