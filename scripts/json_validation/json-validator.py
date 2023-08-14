from pathlib import Path
import json
import sqlalchemy as db
import os
from dotenv import load_dotenv
from sqlalchemy import insert
from sqlalchemy.orm import Session, sessionmaker
import sys
from datetime import datetime
import pathlib


def process_veris_information():
    

    invalid_json_files = []
    valid_json_files = []

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[2]

    ############################################################
    # Concat paths for both the submitted and validated folders
    ############################################################
    veris_validated_data = toplevel_path / "veris-data/data/json/validated"

    #print(veris_validated_data)

    for filename in os.listdir(veris_validated_data):
        extension = pathlib.Path(filename).suffix
        if extension == '.json' or extension == '.JSON':
           #print(filename)
           
           try:
               with open(veris_validated_data/filename) as f:
                    valid_json_files.append(filename)
           except ValueError as e:
               invalid_json_files.append(filename)

        

    print(len(valid_json_files),len(invalid_json_files))

    
process_veris_information()
