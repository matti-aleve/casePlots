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


	if PHU in regionCountMain:
		if len(date) >= 0:
			if date in regionCountMain[PHU]:
				regionCountMain[PHU][date] = pct
			else:
				regionCountMain[PHU][date] = pct
	else:
		regionCountMain[PHU] = {}
		regionCountMain[PHU][date] = pct
	
	return regionCountMain
	
def DayCountPHU (regionCountMain, PHU, date):
	dayCount = 0
	
	return regionCountMain[PHU][date]

def DayCountPHUAge (regionCountMain, PHU, date, age):
	dayCount = 0
	
	for i,j in regionCountMain.items():
		if i == PHU:
			for k,l in j.items():
				if k == date:
					for m,n in l.items():
						if(m==age):
							dayCount = dayCount + n
	return dayCount


def decrementPHUCount (regionCount,date):

	if len(date) >= 0:
		if date in regionCount:
			regionCount[date] = regionCount[date] - 1
		else:
			regionCount[date] = 0
	
	return regionCount
	
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




def chartingDataAge (HealthUnit,refDateStr,provincialCount,regionCountMain,theChart,Age):

	for i in sorted(provincialCount):
		if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
			theChart.append(float(DayCountPHUAge(regionCountMain,healthUnit , i,Age)))
	return theChart


def xfmt(x,pos=None):
    ''' custom date formatting '''
    x = mdates.num2date(x)
    label = x.strftime('%m/%d')
    label = label.lstrip('0')
    return label

def mySubPlot (plotChart,plotPos,plotTitle,yLimMax,yTickColor):

	num_series = pd.Series(plotChart)
	windows = num_series.rolling(rollingAvg)
	mov_avg = windows.mean()
	mov_avg_list = mov_avg.tolist()

	plt.subplot(spRow,spCol,plotPos)
	plt.title(plotTitle)
	plt.xticks(rotation=xtickRotation,fontsize=xtickFont)
	plt.yticks(fontsize=ytickSize,color=yTickColor)
	plt.plot(chartX[(plotDays-1):-1],plotChart[(plotDays-1):-1],color=markerColor,marker=markerStyle,linestyle='')
	plt.plot(chartX[(plotDays-1):-1],mov_avg_list[(plotDays-1):-1])
	plt.ylim(yLimMin,yLimMax)

	plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=xtickRotation)
	plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=xtickInterval))
	plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
	return
	
	


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



MAIN = {"Peel Public Health","Toronto Public Health","York Region Public Health Services",
"Hamilton Public Health Services","Niagara Region Public Health Department","Halton Region Health Department",
"Region of Waterloo, Public Health","Windsor-Essex County Health Unit","Ottawa Public Health","Durham Region Health Department"}



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


PHU_Scale = {"Peel Public Health":1,"Toronto Public Health":1,
"York Region Public Health Services":1,"Hamilton Public Health Services":1,
"Niagara Region Public Health Department":1,
"Halton Region Health Department":1,"Region of Waterloo, Public Health":1,
"Windsor-Essex County Health Unit":1,"Ottawa Public Health":1,
"Durham Region Health Department":1,"Brant County Health Unit":1,
"Lambton Public Health":1,"Chatham-Kent Health Unit":1,
"Huron Perth District Health Unit":1,"Southwestern Public Health":1,
"Middlesex-London Health Unit":1,"Wellington-Dufferin-Guelph Public Health":1,
"Eastern Ontario Health Unit":1,"Haldimand-Norfolk Health Unit":1,
"Simcoe Muskoka District Health Unit":1,"Peterborough Public Health":1,
"Timiskaming Health Unit":1,"Haliburton, Kawartha, Pine Ridge District Health Unit":1,
"Leeds, Grenville and Lanark District Health Unit":1,"Grey Bruce Health Unit":1,
"Renfrew County and District Health Unit":1,"Hastings and Prince Edward Counties Health Unit":1,
"Thunder Bay District Health Unit":1,"Kingston, Frontenac and Lennox & Addington Public Health":1,
"Northwestern Health Unit":1,"North Bay Parry Sound District Health Unit":1,
"Algoma Public Health Unit":1,"Sudbury & District Health Unit":1,"Porcupine Health Unit":1}


PHU_PositionC1 = {"Peel Public Health":1,"Toronto Public Health":2,
"York Region Public Health Services":5,"Hamilton Public Health Services":3,
"Niagara Region Public Health Department":6,
"Halton Region Health Department":4,"Region of Waterloo, Public Health":10,
"Windsor-Essex County Health Unit":15,"Ottawa Public Health":11,
"Brant County Health Unit":7,"Huron Perth District Health Unit":13,
"Middlesex-London Health Unit":14,"Wellington-Dufferin-Guelph Public Health":8,
"Grey Bruce Health Unit":12,"Durham Region Health Department":9
}

PHU_PositionC2 = {
"Lambton Public Health":1,"Chatham-Kent Health Unit":2,
"Southwestern Public Health":3,
"Eastern Ontario Health Unit":4,"Haldimand-Norfolk Health Unit":5,
"Simcoe Muskoka District Health Unit":9,"Peterborough Public Health":7,
"Timiskaming Health Unit":10,"Haliburton, Kawartha, Pine Ridge District Health Unit":11,
"Leeds, Grenville and Lanark District Health Unit":8,
"Renfrew County and District Health Unit":6,"Hastings and Prince Edward Counties Health Unit":12,
"Kingston, Frontenac and Lennox & Addington Public Health":13,
"Northwestern Health Unit":14,"North Bay Parry Sound District Health Unit":15,
}

PHU_PositionC3 = {"Algoma Public Health Unit":1,
"Sudbury & District Health Unit":2,"Porcupine Health Unit":3,
"Thunder Bay District Health Unit":4}


under40 = {"<20","20s","30s"}
	
	
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
		refDateStr = "2021-04-01"
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







