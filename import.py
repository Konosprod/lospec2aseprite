from bs4 import BeautifulSoup
import sys
import os
import urllib3.request
import certifi
import hashlib
import json
import pathlib

from progressbar import DataTransferBar
from requests_download import download, HashTracker, ProgressTracker

user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'}
http = urllib3.PoolManager(cert_reqs="CERT_REQUIRED", ca_certs=certifi.where(), headers=user_agent)


hasher = HashTracker(hashlib.sha256())
progress = ProgressTracker(DataTransferBar())

PALETTES_PATH = pathlib.Path.home().joinpath("AppData").joinpath("Roaming").joinpath("Aseprite").joinpath("extensions").joinpath("lospec-palettes")
JSON_FILE_PATH =  PALETTES_PATH.joinpath("package.json")

def importLospec(url):
    url = url.replace("-32x.png", ".gpl")
    filename = os.path.basename(url)


    download(url, PALETTES_PATH.joinpath(filename), trackers=(hasher, progress))

    f = open(JSON_FILE_PATH, "r")
    conf = json.load(f)
    f.close()

    name = ""
    
    for elem in filename.replace(".gpl", "").split("-"):
        name += elem.capitalize() + " "

    name = name[:-1] 

    conf["contributes"]["palettes"].append({"id":name, "path":filename})

    f = open(JSON_FILE_PATH, "w")
    json.dump(conf, f, indent=4, sort_keys=True)
    f.close()



if __name__ == "__main__":
    
    importLospec(sys.argv[1])