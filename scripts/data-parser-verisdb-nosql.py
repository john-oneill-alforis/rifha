from pymongo import MongoClient
import os
import sys
import datetime
from pathlib import Path
import json


def load_veris():
    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[1]

    # Concat paths for both the submitted and validated folders
    # veris_submitted_data = toplevel_path / "veris-data/data/json/submitted"
    veris_validated_data = toplevel_path / "veris-data/data/json/validated"

    # Grab the data from the validated reports
    countlist = []
    for p in veris_validated_data.rglob("*.json"):
        try:
            # Load the data from the json file
            json_file = veris_validated_data / p.name
            data = json.loads(json_file.read_bytes())

            print(data["action"].keys())
            countlist.append(data["action"])

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, exc_obj, fname, exc_tb.tb_lineno, datetime.datetime.now())

    print(len(countlist))


load_veris()
