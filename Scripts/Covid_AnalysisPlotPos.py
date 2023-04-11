#!/usr/bin/env python

#Version 1.0

import sys
import datetime
import os
import time
import shutil
import csv

import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime as dt
import matplotlib.ticker as tkr

from subprocess import call
from datetime import datetime, timedelta

theChart = []
plotChart = []
chartX = []
refDateStr = "2020-07-30"


def incrementPHUCount (regionCountMain,PHU,date,pct):

	outstring = PHU + "," + date + "," + pct
	#print ("%s" % outstring)

	if PHU in regionCountMain:
		regionCountMain[PHU][date] = pct
	else:
		print(PHU)
		regionCountMain[PHU] = {}
		regionCountMain[PHU][date] = pct
	return regionCountMain


	
	
def chartingData (HealthUnit,refDateStr,provincialCount,regionCountMain,theChart):

	for i in sorted(provincialCount):
		if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
			theChart.append(float(DayCountPHU(regionCountMain,healthUnit , i)))
	return theChart

def chartingDataMax (HealthUnit,refDateStr,provincialCount,regionCountMain,theChart):
	maxCount = 0.0
	maxDateStr = "2022-02-24"

	for i in sorted(provincialCount):
		if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(maxDateStr,'%Y-%m-%d')):
			dailyCount = float(DayCountPHU(regionCountMain,healthUnit , i))
			if dailyCount > maxCount :
				maxCount = dailyCount
				outString = "New Max = " + str(maxCount)
				print (outString)
	return maxCount






def xfmt(x,pos=None):
    ''' custom date formatting '''
    x = mdates.num2date(x)
    label = x.strftime('%m/%d')
    label = label.lstrip('0')
    return label

	
	

sys.exit()

webChartFile = '/Users/matti/GitHub/casePlots/PHU/Ontario_ChartPos1.png'
webChartFile2 = '/Users/matti/GitHub/casePlots/PHU/Ontario_ChartPos2.png'
webChartFile3 = '/Users/matti/GitHub/casePlots/PHU/Ontario_ChartPos3.png'

phus = "All"
filename = ""
filename2 = ""
summaryfile = ""

strToday = datetime.today().strftime('%Y-%m-%d')

filename = "/Users/matti/Desktop/Covid/testing_metrics_by_phu_"+strToday+".csv"
filename2 = ""
summaryfile = ""



fd=open(filename,'r')
today=fd.readlines() # Read entire contents of file
fd.close()



start_date = strToday[-8:]
end_date = strToday[-8:]


count = 1
case_reported_date = 0
pct_pos = 3
aquisition_info = 7
reporting_PHU = 10 

PHU = set()
regionCount = {}
regionCountMain = {"PHU1" : {"2021-01-01" : {"50s" : 0}}}
ageCount = {"<20":0,"20s":0,"30s":0,"40s":0,"50s":0,"60s":0,"70s":0,"80s":0,"90+":0}
provincialCount = {}

#regionCounts = {peelRegionCount,torontoRegionCount,yorkRegionCount,hamiltonRegionCount,haltonRegionCount}





PHU_Short_Name = {"Peel Public Health":"Peel","Toronto Public Health":"Toronto",
"York Region Public Health Services":"York","Hamilton Public Health Services":"Hamilton",
"Niagara Region Public Health Department":"Niagara",
"Halton Region Health Department":"Halton","Region of Waterloo, Public Health":"Waterloo",
"Windsor-Essex County Health Unit":"Windsor","Ottawa Public Health":"Ottawa",
"Durham Region Health Department":"Durham","Brant County Health Unit":"Brant",
"Lambton Public Health":"Lambton","Chatham-Kent Health Unit":"Chat-Kent",
"Huron Perth District Health Unit":"Huron","Southwestern Public Health":"Southwestern",
"Middlesex-London Health Unit":"London","Wellington-Dufferin-Guelph Public Health":"Guelph",
"Eastern Ontario Health Unit":"Eastern","Haldimand-Norfolk Health Unit":"Hald-Nor",
"Simcoe Muskoka District Health Unit":"Simcoe","Peterborough Public Health":"Peterborough",
"Timiskaming Health Unit":"Timiskaming","Haliburton, Kawartha, Pine Ridge District Health Unit":"Hal-Kawartha",
"Leeds, Grenville and Lanark District Health Unit":"Leeds","Grey Bruce Health Unit":"Grey Bruce",
"Renfrew County and District Health Unit":"Renfrew","Hastings and Prince Edward Counties Health Unit":"Hastings",
"Thunder Bay District Health Unit":"Thunder Bay","Kingston, Frontenac and Lennox & Addington Public Health":"Kingston",
"Northwestern Health Unit":"Northwastern","North Bay Parry Sound District Health Unit":"North Bay",
"Algoma Public Health Unit":"Algoma","Sudbury & District Health Unit":"Sudbury","Porcupine Health Unit":"Porcupine"}


	
	
start_date = "20" + start_date
end_date = "20" + end_date

theStartDate = datetime.strptime(end_date,'%Y-%m-%d')

	
count = 0
under40Count = 0
over40Count = 0
subindex = 0

fullline = ""

print ("%s" % filename)
with open(filename, newline='') as csvfile:
	activityReader = csv.reader(csvfile, delimiter=',', quotechar='\"')

	for line in activityReader:

		if (count == 0):
			for iteration, atoken in enumerate(line):
				if atoken == "PHU_name":
					reporting_PHU = subindex
				subindex = subindex + 1
		else:
			if line[reporting_PHU] in regionCount:
				regionCount[line[reporting_PHU]] = regionCount[line[reporting_PHU]] + 1
				#print ("%i" % regionCount[line[reporting_PHU]])
			else:
				regionCount[line[reporting_PHU]] = 1

				
			thedate = line[case_reported_date]	
			if(len(thedate)==0):
				continue

			if thedate in provincialCount:
				provincialCount[thedate] = provincialCount[thedate] + 1
			else:
				provincialCount[thedate] = 1


			regionCountMain = incrementPHUCount(regionCountMain,line[reporting_PHU],line[case_reported_date],line[pct_pos])


	
		count = count + 1

count = 0
subindex = 0

print (regionCountMain["Peel Regional Health Unit"])

for PHU in regionCountMain:
	print (PHU)
	lastDate = ""
	## PctPos

	chartPoint = []
	chartX = []
	for i in sorted(regionCountMain[PHU]):
		refDateStr = "2021-06-01"
		if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
			chartX.append(i[-5:])
			chartPoint.append(float(regionCountMain[PHU][i])*100)
			lastDate = i
			#chartX.append(i)
		

	print(chartPoint)
	xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

	num_series = pd.Series(chartPoint)
	windows = num_series.rolling(7)
	mov_avg = windows.mean()

	mov_avg_list = mov_avg.tolist()

	daysToPlot = -15


	#plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')

	plt.plot(chartX,chartPoint,'r.')
	plt.title(PHU + '-' + lastDate)

	plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))
	plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
	plt.xlabel('Date')
	plt.ylabel('%')

	pngFile = '/Users/matti/GitHub/casePlots/Pos/' + PHU + '.png'
	plt.savefig(pngFile)
	plt.clf()







