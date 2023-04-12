from git import Repo
import os
from os.path import exists


def sync_veris():
    try:
        cdir = os.getcwd()
        # print("Current Directory: ", cdir)
        # print("Parent Directory: ", os.path.dirname(cdir))

        os.path.exists(cdir + "veris-data/.git")

        repo = Repo("veris-data")
        origin = repo.remote(name="origin")
        origin.pull()

    except:
        cdir = os.getcwd()
        print("Current Directory: ", cdir)


sync_veris()
