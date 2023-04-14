#!/usr/bin/env python

#Version 1.0

import sys
import datetime
import os
import time
import shutil
import csv
from mastodon import Mastodon

from datetime import datetime as dt

from subprocess import call
from datetime import datetime, timedelta

baseURL = "https://www.publichealthontario.ca/-/media/Images/OPHESAC-Science-Table/COVID-19-Wastewater-Signals/en/"
ontario = "province-wastewater-graphic"
northWest = "north-west-wastewater-graphic"
northEast = "north-east-wastewater-graphic"
eastern = "eastern-wastewater-graphic"
centralEast = "central-east-wastewater-graphic"
greaterToronto = "gta-wastewater-graphic"
southWest = "south-west-wastewater-graphic"
centralWest = "central-west-wastewater-graphic"

baseOutput = "~/GitHub/casePlots/WW/"

strToday = datetime.today().strftime('%Y-%m-%d')
os.system("curl " + baseURL + ontario + ".png > " + baseOutput + ontario + ".png")
os.system("curl " + baseURL + northWest + ".png > " + baseOutput + northWest + ".png")
os.system("curl " + baseURL + northEast + ".png > " + baseOutput + northEast + ".png")
os.system("curl " + baseURL + eastern + ".png > " + baseOutput + eastern + ".png")
os.system("curl " + baseURL + centralEast + ".png > " + baseOutput + centralEast +  ".png")
os.system("curl " + baseURL + greaterToronto + ".png > " + baseOutput + greaterToronto + ".png")
os.system("curl " + baseURL + southWest + ".png > " + baseOutput + southWest + ".png")
os.system("curl " + baseURL + centralWest + ".png > " + baseOutput + centralWest + ".png")

baseOutput = "~/Desktop/CovidWW/"

os.system("curl " + baseURL + ontario + ".png > " + baseOutput + ontario +"-"+ strToday + ".png")
os.system("curl " + baseURL + northWest + ".png > " + baseOutput + northWest +"-"+ strToday + ".png")
os.system("curl " + baseURL + northEast + ".png > " + baseOutput + northEast +"-"+ strToday + ".png")
os.system("curl " + baseURL + eastern + ".png > " + baseOutput + eastern +"-"+ strToday + ".png")
os.system("curl " + baseURL + centralEast + ".png > " + baseOutput + centralEast +"-"+ strToday + ".png")
os.system("curl " + baseURL + greaterToronto + ".png > " + baseOutput + greaterToronto +"-"+ strToday + ".png")
os.system("curl " + baseURL + southWest + ".png > " + baseOutput + southWest +"-"+ strToday + ".png")
os.system("curl " + baseURL + centralWest + ".png > " + baseOutput + centralWest +"-"+ strToday + ".png")


f = open("/Users/matti/Keys/tokensBotInSpaceGTA.secret", "r")
sToken = f.readline()
print(sToken)

#   Set up Mastodon
mastodon = Mastodon(
    access_token = sToken,
    api_base_url = 'https://botsin.space/'
)

pngFile = "/Users/matti/Desktop/CovidWW/" + greaterToronto + "-" + strToday + ".png"
postText = "Automated Post \rGreater Toronto Toronto Waste Water for  " + strToday
postText = postText + "\r\rhttps://www.publichealthontario.ca/en/Data-and-Analysis/Infectious-Disease/COVID-19-Data-Surveillance/Wastewater"
print(pngFile)
#mastodon.toot("Test Post via API...")
metadata = mastodon.media_post(pngFile, "image/png")
mastodon.status_post(postText, media_ids=metadata["id"])