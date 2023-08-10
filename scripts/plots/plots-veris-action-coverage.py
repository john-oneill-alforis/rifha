from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


def process_veris_information():
    # Creat a list to hold entries for later count
    action_attribution_true = []
    action_attribution_false = []

    # build some paths to find the veris data

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[2]

    # Concat paths for both the submitted and validated folders
    # veris_submitted_data = toplevel_path / "veris_data/data/json/submitted"
    veris_validated_data = toplevel_path / "veris-data/data/json/validated"

    # Grab the data from the validated reports
    for p in veris_validated_data.rglob("*.json"):
        # Load the data from the json file
        json_file = veris_validated_data / p.name

        try:
            data = json.loads(json_file.read_bytes())
            if data["action"]["unknown"]:
                action_attribution_false.append(["incident_id"])
               

        except:
            action_attribution_true.append(["incident_id"])



    print(len(action_attribution_true))
    print(len(action_attribution_false))

process_veris_information()
