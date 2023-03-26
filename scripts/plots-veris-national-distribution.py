from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


def process_veris_information():
    # Creat a list to hold entries for later count
    veris_geo_count = []

    # build some paths to find the veris data

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[1]

    # Concat paths for both the submitted and validated folders
    # veris_submitted_data = toplevel_path / "veris_data/data/json/submitted"
    veris_validated_data = toplevel_path / "veris-data/VCDB/data/json/validated"

    # Grab the data from the validated reports
    for p in veris_validated_data.rglob("*.json"):
        # Load the data from the json file
        json_file = veris_validated_data / p.name

        try:
            data = json.loads(json_file.read_bytes())
            for x in data["victim"]["country"]:
                print(x)
                veris_geo_count.append(x)

        except:
            print(p.name)

    # Grab the data from the submitted reports
    # for p in veris_submitted_data.rglob("*.json"):

    # Load the data from the json file
    # json_file = veris_submitted_data / p.name

    # try:
    #    data = json.loads(json_file.read_bytes())
    #    for x in data["victim"]["country"]:
    #        print(x)
    #        veris_geo_count.append(x)

    # except:
    #    print(p.name)

    df = pd.DataFrame(veris_geo_count, columns=["Location"])

    # The count of the entries per year. This is a count so wont
    # have an index on it by default hence the reset index
    df = df.groupby(["Location"])["Location"].count().reset_index(name="Count")
    df = df.sort_values(by="Count", ascending=False).head(10)

    print(df)

    df.plot.bar(x="Location", y="Count")
    plt.savefig(toplevel_path / "plots/veris-national-distribution.png")


process_veris_information()
