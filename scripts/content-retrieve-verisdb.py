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
        Repo.clone_from("https://github.com/vz-risk/VCDB.git", "veris-data/")


sync_veris()
