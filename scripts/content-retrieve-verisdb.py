from git import Repo
import os
from os.path import exists


def sync_veris():
    try:
        os.path.exists("veris-data/.git")

        repo = Repo("veris-data")

        origin = repo.remote(name="origin")
        origin.pull()

    except:
        print("Repo Does Not Exsist")
        current_working_directory = os.getcwd()
        print(current_working_directory)


sync_veris()
