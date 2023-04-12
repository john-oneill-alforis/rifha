from git import Repo
import os
from os.path import exists


def sync_veris():
    cdir = os.getcwd()
    print("Current Directory: ", cdir)
    print("Parent Directory: ", os.path.dirname(cdir))

    os.path.exists("veris-data/.git")

    repo = Repo("veris-data")
    origin = repo.remote(name="origin")
    origin.pull()


sync_veris()
