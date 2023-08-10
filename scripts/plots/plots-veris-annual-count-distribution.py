from pathlib import Path
import json
import matplotlib.pyplot as plt
import pandas as pd


def process_veris_information():
    # Creat a list to hold entries for later count
    veris_count = []

    # build some paths to find the veris data

    # VERIS Data should be located on the same folder
    # level as the scripts folder
    toplevel_path = Path(__file__).parents[2]

 
    # Concat paths for both the submitted and validated folders
    # veris_submitted_data = toplevel_path / "veris-data/data/json/submitted"

    veris_validated_data = toplevel_path / "veris-data/data/json/validated"
    print(veris_validated_data)

    # Grab the data from the validated reports
    for p in veris_validated_data.rglob("*.json"):
        # Load the data from the json file
        json_file = veris_validated_data / p.name


        try:
            data = json.loads(json_file.read_bytes())
            veris_count.append(int(data["plus"]["created"][0:4]))
            veris_count.sort()

        except:
            print(p.name)

    # Grab the data from the submitted reports
    # for p in veris_submitted_data.rglob("*.json"):
    #    # Load the data from the json file
    #    json_file = veris_submitted_data / p.name

    #    try:
    #        data = json.loads(json_file.read_bytes())
    #        veris_count.append(int(data["plus"]["created"][0:4]))
    #        veris_count.sort()

    #    except:
    #        print(p.name)

    # df = pd.DataFrame(veris_count, columns=["Year"])

    # The count of the entries per year. This is a count so wont
    # have an index on it by default hence the reset index
    df = pd.DataFrame(veris_count, columns=["Year"])
    df = df.groupby(["Year"])["Year"].count().reset_index(name="Count")

    print(df)
    df.plot.line(x="Year", y="Count")
    plt.title("Contributed Veris Incidents Over Time")
    plt.savefig(toplevel_path / "plots/veris-entry-distribution-over-time.png")


process_veris_information()
