from git import Repo
import os
from os.path import exists


def sync_veris():
    try:
        cdir = os.getcwd()

        os.path.exists(cdir + "/veris-data/.git")

        repo = Repo(cdir + "/veris-data")
        origin = repo.remote(name="origin")
        origin.pull()

    except:
        print("Git Pull Failed")


sync_veris()
