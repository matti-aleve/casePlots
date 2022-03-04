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


def incrementPHUCount (regionCountMain,PHU,date,age):

	if PHU in regionCountMain:
		if len(date) >= 0:
			if date in regionCountMain[PHU]:
				if age in regionCountMain[PHU][date]:
					regionCountMain[PHU][date][age] = regionCountMain[PHU][date][age] + 1
				else:
					regionCountMain[PHU][date][age] = 1
			else:
				update_dict = {date : {age : 1}}
				regionCountMain[PHU].update(update_dict)
	else:
		update_dict = {PHU : {date : {age : 1}}}
		regionCountMain.update(update_dict)
	
	return regionCountMain
	
def DayCountPHU (regionCountMain, PHU, date):
	dayCount = 0
	
	for i,j in regionCountMain.items():
		if i == PHU:
			for k,l in j.items():
				if k == date:
					for m,n in l.items():
						dayCount = dayCount + n
	return dayCount

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
			theChart.append(float(DayCountPHU(regionCountMain,healthUnit , i)/(PHU_Pop[healthUnit]/100000)))
	return theChart

def chartingDataMax (HealthUnit,refDateStr,provincialCount,regionCountMain,theChart):
	maxCount = 0.0
	maxDateStr = "2022-02-24"

	for i in sorted(provincialCount):
		if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(maxDateStr,'%Y-%m-%d')):
			dailyCount = float(DayCountPHU(regionCountMain,healthUnit , i)/(PHU_Pop[healthUnit]/100000))
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
	
	


webChartFile = '/Users/matti/GitHub/casePlots/PHU/Ontario_Chart1.png'
webChartFile2 = '/Users/matti/GitHub/casePlots/PHU/Ontario_Chart2.png'
webChartFile3 = '/Users/matti/GitHub/casePlots/PHU/Ontario_Chart3.png'

phus = "All"
filename = ""
filename2 = ""
summaryfile = ""

strToday = datetime.today().strftime('%Y-%m-%d')

if len(sys.argv) == 3:
	filename = "/Users/matti/Desktop/Covid/conposcovidloc_20" + sys.argv[1] + ".csv" 
	filename2 = "/Users/matti/Desktop/Covid/conposcovidloc_20" + sys.argv[2] + ".csv"
	summaryfile = "/Users/matti/Desktop/Covid/covidtesting_20" + sys.argv[1] + ".csv" 
elif len(sys.argv) == 4:
	phus = sys.argv[3]
	filename = "/Users/matti/Desktop/Covid/conposcovidloc_20" + sys.argv[1] + ".csv" 
	filename2 = "/Users/matti/Desktop/Covid/conposcovidloc_20" + sys.argv[2] + ".csv"
	summaryfile = "/Users/matti/Desktop/Covid/covidtesting_20" + sys.argv[1] + ".csv" 
else: 
	filename = "/Users/matti/Desktop/Covid/conposcovidloc_"+strToday+".csv"
	filename2 = ""
	summaryfile = ""

if len(sys.argv)>=3:
	first = datetime.strptime(sys.argv[1],'%y-%m-%d')
	second = datetime.strptime(sys.argv[2],'%y-%m-%d')

	duration = first - second
	num_days = duration.total_seconds()/60/60/24

hostInfo = os.uname()

if "Matti-MacBook-Pro.local" not in hostInfo:
	os.system("curl https://data.ontario.ca/dataset/f4112442-bdc8-45d2-be3c-12efae72fb27/resource/455fd63b-603d-4608-8216-7d8647f43350/download/conposcovidloc.csv > ~/Desktop/Covid/conposcovidloc_" + strToday + ".csv")
	os.system("curl https://data.ontario.ca/dataset/f4f86e54-872d-43f8-8a86-3892fd3cb5e6/resource/ed270bb8-340b-41f9-a7c6-e8ef587e6d11/download/covidtesting.csv > ~/Desktop/Covid/covidtesting_"+strToday+".csv")
	os.system("curl https://files.ontario.ca/moh-covid-19-report-en-" + strToday + ".pdf > ~/Desktop/Covid/moh-covid-19-report-en-"+strToday+".pdf")
	os.system("curl https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv > ~/Desktop/Covid/schoolcovidsummary_"+strToday+".csv")
	os.system("curl https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/8b6d22e2-7065-4b0f-966f-02640be366f2/download/schoolsactivecovid.csv > ~/Desktop/Covid/schoolsactivecovid_"+strToday+".csv")
	os.system("curl https://data.ontario.ca/dataset/cbb4d08c-4e56-4b07-9db6-48335241b88a/resource/ce9f043d-f0d4-40f0-9b96-4c8a83ded3f6/download/response_framework.csv > ~/Desktop/Covid/response_framework_"+strToday+".csv")
	os.system("curl https://data.ontario.ca/dataset/a2dfa674-a173-45b3-9964-1e3d2130b40f/resource/07bc0e21-26b5-4152-b609-c1958cb7b227/download/testing_metrics_by_phu.csv > ~/Desktop/Covid/testing_metrics_by_phu_"+strToday+".csv")
	#cases and rates by vax status
	os.system("curl https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/eed63cf2-83dd-4598-b337-b288c0a89a16/download/cases_by_vac_status.csv > ~/Desktop/Covid/cases_by_vac_status_"+strToday+".csv")
	#hosp by vax status
	os.system("curl https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/274b819c-5d69-4539-a4db-f2950794138c/download/vac_status_hosp_icu.csv > ~/Desktop/Covid/vac_status_hosp_icu_"+strToday+".csv")
	#vax by phu
	os.system("curl https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/2a362139-b782-43b1-b3cb-078a2ef19524/download/vaccines_by_age_phu.csv > ~/Desktop/Covid/vaccines_by_age_phu_"+strToday+".csv")
	#vax data
	os.system("curl https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/8a89caa9-511c-4568-af89-7f2174b4378c/download/vaccine_doses.csv > ~/Desktop/Covid/vaccine_doses_"+strToday+".csv")
	#vax by age
	os.system("curl https://data.ontario.ca/dataset/752ce2b7-c15a-4965-a3dc-397bf405e7cc/resource/775ca815-5028-4e9b-9dd4-6975ff1be021/download/vaccines_by_age.csv > ~/Desktop/Covid/vaccines_by_age_"+strToday+".csv")
	#case status by PHU
	os.system("curl https://data.ontario.ca/dataset/1115d5fe-dd84-4c69-b5ed-05bf0c0a0ff9/resource/d1bfe1ad-6575-4352-8302-09ca81f7ddfc/download/cases_by_status_and_phu.csv > ~/Desktop/Covid/cases_by_status_and_phu_"+strToday+".csv")
	#effective Re 
	os.system("curl https://data.ontario.ca/dataset/8da73272-8078-4cbd-ae35-1b5c60c57796/resource/1ffdf824-2712-4f64-b7fc-f8b2509f9204/download/re_estimates_on.csv > ~/Desktop/Covid/re_estimates_on_"+strToday+".csv")
	#ongoing outbreaks
	os.system("curl https://data.ontario.ca/dataset/5472ffc1-88e2-48ca-bc9f-4aa249c1298d/resource/66d15cce-bfee-4f91-9e6e-0ea79ec52b3d/download/ongoing_outbreaks.csv > ~/Desktop/Covid/ongoing_outbreaks_"+strToday+".csv")
	#outbreaks by PHU
	os.system("curl https://data.ontario.ca/dataset/5472ffc1-88e2-48ca-bc9f-4aa249c1298d/resource/36048cc1-3c47-48ff-a49f-8c7840e32cc2/download/ongoing_outbreaks_phu.csv > ~/Desktop/Covid/ongoing_outbreaks_phu_"+strToday+".csv")

fd=open(filename,'r')
today=fd.readlines() # Read entire contents of file
fd.close()

if (len(filename2)>1):
	fd=open(filename2,'r')
	yesterday=fd.readlines() # Read entire contents of file
	fd.close()

if (len(summaryfile)>1):
	fd=open(summaryfile,'r')
	summaryData=fd.readlines() # Read entire contents of file
	fd.close()

if len(sys.argv)>2:
	start_date = sys.argv[2]
	end_date = sys.argv[1]
else:
	start_date = strToday[-8:]
	end_date = strToday[-8:]


count = 1
case_reported_date = 2
specimen_date = 4
age_group = 5
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

PHU_Pop = {"Peel Public Health":1542001,"Toronto Public Health":2965712,
"York Region Public Health Services":1181486,"Hamilton Public Health Services":574263,
"Niagara Region Public Health Department":479183,
"Halton Region Health Department":596363,"Region of Waterloo, Public Health":595465,
"Windsor-Essex County Health Unit":428556,"Ottawa Public Health":1028514,
"Durham Region Health Department":697355,"Brant County Health Unit":151034,
"Lambton Public Health":132243,"Chatham-Kent Health Unit":106091,
"Huron Perth District Health Unit":144801,"Southwestern Public Health":215401,
"Middlesex-London Health Unit":506008,"Wellington-Dufferin-Guelph Public Health":308963,
"Eastern Ontario Health Unit":213064,"Haldimand-Norfolk Health Unit":119146,
"Simcoe Muskoka District Health Unit":594494,"Peterborough Public Health":147908,
"Timiskaming Health Unit":33800,"Haliburton, Kawartha, Pine Ridge District Health Unit":189982,
"Leeds, Grenville and Lanark District Health Unit":177605,"Grey Bruce Health Unit":173372,
"Renfrew County and District Health Unit":107955,"Hastings and Prince Edward Counties Health Unit":170793,
"Thunder Bay District Health Unit":158165,"Kingston, Frontenac and Lennox & Addington Public Health":208613,
"Northwestern Health Unit":81472,"North Bay Parry Sound District Health Unit":129642,
"Algoma Public Health Unit":117036,"Sudbury & District Health Unit":204640,"Porcupine Health Unit":85422}


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
				if atoken == "Reporting_PHU":
					reporting_PHU = subindex
				subindex = subindex + 1
		else:
			if line[reporting_PHU] in regionCount:
				regionCount[line[reporting_PHU]] = regionCount[line[reporting_PHU]] + 1
				#print ("%i" % regionCount[line[reporting_PHU]])
			else:
				regionCount[line[reporting_PHU]] = 1

			#print (tokens[age_group])
			if line[age_group] in ageCount:
				ageCount[line[age_group]] = ageCount[line[age_group]] + 1
			else:
				ageCount[line[age_group]] = 1

			if line[age_group] in under40:
				under40Count = under40Count + 1
			else:
				over40Count = over40Count + 1
				
			thedate = line[case_reported_date]	
			if(len(thedate)==0):
				continue

			if thedate in provincialCount:
				provincialCount[thedate] = provincialCount[thedate] + 1
			else:
				provincialCount[thedate] = 1


			regionCountMain = incrementPHUCount(regionCountMain,line[reporting_PHU],line[case_reported_date],line[age_group])


	
		count = count + 1

count = 0
subindex = 0



for i in sorted(provincialCount):
	refDateStr = "2020-07-30"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		chartX.append(i[-5:])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]


print (chartX[-14:])

##### PEEL #####
# num_series = pd.Series(peelChart)
# windows = num_series.rolling(7)
# mov_avg = windows.mean()
# 
# mov_avg_list = mov_avg.tolist()
# 
# plt.plot(chartX[-14:],peelChart[-14:],'r+')
# plt.plot(chartX[-14:],mov_avg_list[-14:])
# plt.title('Peel')
# 
# plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
# plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
# plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
# 
# 
# plt.savefig('/Users/matti/Downloads/Peel.png')
# plt.clf()


##### MASTER PLOT ######

spRow = 3
spCol = 5
yLimMin = 0
yLimMax = 50
ytickSize = 6
yTickColor = 'black'

plotDays = -42
plotDays = -21
xtickRotation = 60
xtickFont = 4
markerStyle = '.'
markerColor = '#DEDEDE'
xtickInterval = 7
rollingAvg = 7


for i in sorted(provincialCount):
	lastdate = i

print(lastdate)	
	
yLimMax = 0
for hu in PHU_PositionC1:

	healthUnit = hu

	maxValue = chartingDataMax(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	if maxValue > yLimMax:
		yLimMax = maxValue

outString = "yLimMax = " + str(yLimMax)
print (outString)

for hu in PHU_PositionC1:

	healthUnit = hu

	plotChart = chartingData(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	plotPos = PHU_PositionC1[hu]
	plotTitle = PHU_Short_Name[hu]

	if PHU_Scale[hu] > 1:
		mySubPlot (plotChart,plotPos,plotTitle,yLimMax*PHU_Scale[hu],'red')
	else:
		mySubPlot (plotChart,plotPos,plotTitle,yLimMax*PHU_Scale[hu],yTickColor)




plt.suptitle('Daily Cases Per 100k by PHU By Case Reported Date -' + lastdate)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.8, wspace=0.4, hspace=0.8)

dailyChartFile = '/Users/matti/Desktop/Covid/Ontario_Chart-'+strToday+'.png'

#plt.show()
plt.savefig(dailyChartFile,dpi=200)
#plt.savefig('/Users/matti/Downloads/Ontario.png')
plt.clf()

try:
	shutil.copy2(dailyChartFile, webChartFile)
except:
	print ("File Not copied to onedrive")

yLimMax = 0
for hu in PHU_PositionC2:

	healthUnit = hu

	maxValue = chartingDataMax(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	if maxValue > yLimMax:
		yLimMax = maxValue


for hu in PHU_PositionC2:

	healthUnit = hu

	maxValue = chartingDataMax(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)


	plotChart = chartingData(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	plotPos = PHU_PositionC2[hu]
	plotTitle = PHU_Short_Name[hu]

	if maxValue > yLimMax:
		mySubPlot (plotChart,plotPos,plotTitle,maxValue,'red')
	else:
		mySubPlot (plotChart,plotPos,plotTitle,yLimMax,yTickColor)



plt.suptitle('Daily Cases Per 100k by PHU By Case Reported Date -' + lastdate)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.8, wspace=0.4, hspace=0.8)

dailyChartFile = '/Users/matti/Desktop/Covid/Ontario_Chart2-'+strToday+'.png'

#plt.show()
plt.savefig(dailyChartFile,dpi=200)
#plt.savefig('/Users/matti/Downloads/Ontario.png')
plt.clf()

try:
	shutil.copy2(dailyChartFile, webChartFile2)
except:
	print("File not copied to onedrive")



yLimMax = 0
for hu in PHU_PositionC3:

	healthUnit = hu

	maxValue = chartingDataMax(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	if maxValue > yLimMax:
		yLimMax = maxValue


for hu in PHU_PositionC3:

	healthUnit = hu

	maxValue = chartingDataMax(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)


	plotChart = chartingData(healthUnit,refDateStr,provincialCount,regionCountMain,theChart)
	plotPos = PHU_PositionC3[hu]
	plotTitle = PHU_Short_Name[hu]

	if maxValue > yLimMax:
		mySubPlot (plotChart,plotPos,plotTitle,maxValue,'red')
	else:
		mySubPlot (plotChart,plotPos,plotTitle,yLimMax,yTickColor)


plt.suptitle('Daily Cases Per 100k by PHU By Case Reported Date -' + lastdate)
plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.8, wspace=0.4, hspace=0.8)

dailyChartFile = '/Users/matti/Desktop/Covid/Ontario_Chart3-'+strToday+'.png'

#plt.show()
plt.savefig(dailyChartFile,dpi=200)
#plt.savefig('/Users/matti/Downloads/Ontario.png')
plt.clf()

try:
	shutil.copy2(dailyChartFile, webChartFile3)
except:
	print("file not copied to onedrive")

for unit in MAIN:
	spRow = 3
	spCol = 3

	healthUnit = unit
	
	chartX[-14:]
	maxY = 0
	idx = 1
	for group in ageCount:

		if idx >=10:  #Skip Unknown
			break
		plotChart = chartingDataAge(healthUnit,refDateStr,provincialCount,regionCountMain,theChart,group)
		if max(plotChart[-14:])>maxY:
			maxY = max(plotChart[-14:])
		idx += 1
	
	
	idx = 1
	for group in ageCount:

		if idx >=10:  #Skip Unknown
			break
		plotChart = chartingDataAge(healthUnit,refDateStr,provincialCount,regionCountMain,theChart,group)
		plotPos = idx
		plotTitle = group
		mySubPlot (plotChart,plotPos,plotTitle,maxY,yTickColor)
		idx += 1

	words = healthUnit.split(" ")
	plt.suptitle(unit +' By Case Reported Date -' + strToday)
	plt.subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.8, wspace=0.4, hspace=0.8)
	
	print(unit)
	print(words[0])
	dailyChartFile = '/Users/matti/GitHub/casePlots/ByAge/Ontario_'+PHU_Short_Name[unit]+'.png'
	


	plt.savefig(dailyChartFile,dpi=200)
	plt.clf()





if len(filename2)>1:
	print ("%s" % filename2)
	with open(filename2, newline='') as csvfile:
		activityReader = csv.reader(csvfile, delimiter=',', quotechar='\"')

		for line in activityReader:

			if (count == 0):
				for iteration, atoken in enumerate(line):
					if atoken == "Reporting_PHU":
						reporting_PHU = subindex
					subindex = subindex + 1

			else:
				#print ("%s" % line[reporting_PHU])
				if line[reporting_PHU] in regionCount:
					regionCount[line[reporting_PHU]] = regionCount[line[reporting_PHU]] - 1
				else:
					regionCount[line[reporting_PHU]] = 0

				if line[age_group] in ageCount:
					ageCount[line[age_group]] = ageCount[line[age_group]] - 1
				else:
					ageCount[line[age_group]] = 0

				if line[age_group] in under40:
					under40Count = under40Count - 1
				else:
					over40Count = over40Count - 1


			count = count + 1


	print (" ")
	print (" ")
	print ("Daily Averages")
	print (" ")
	print ("Case\tCases")
	print ("Count\tper 100k\tPHU")
	if phus == "MAIN":
		for i in regionCount:
			if i in sorted(MAIN):
				print(int(regionCount[i]/num_days),"\t",int((regionCount[i]/(PHU_Pop[i]/100000))/num_days),"\t",i)
	else:
		for i in sorted(regionCount):
			print(int(regionCount[i]/num_days),"\t",int(((regionCount[i]/(PHU_Pop[i]/100000))/num_days)*10)/10,"\t",i)



	# for i in sorted(peelRegionCount):
	# 	speelRegionCount[i] = peelRegionCount[i]
	# 	print(i,",",str(peelRegionCount[i]))		
	# 
	# for i in speelRegionCount):
	# 	speelRegionCount[i] = peelRegionCount[i]
	# 	print(i,",",str(peelRegionCount[i]))		


	startFound = 0
	testscompleted = 0
	hospitalized = 0
	inICU = 0
		
	for line in summaryData:
		tokens = line.split(',')
		try:
			hospitalized = int(tokens[12]) 
			inICU = int(tokens[13])
		except: 
			hopitalized = 0
			inICU = 0
		if tokens[0] == start_date:
			startFound = 1
			continue
		if (startFound == 0):
			continue
		try:
			backlog = int(tokens[11])
			testscompleted = int(tokens[9]) + testscompleted
		except:
			continue
		

	print (" ")
	print ("By Age (Ontario Wide)")
	print (" ")

	for i in ageCount:
		print(int(ageCount[i]/num_days),",",i)

	print (" ")

	positivity = 0.0
	totalCount = under40Count + over40Count
	try:
		positivity = (totalCount/num_days)/(testscompleted/num_days)*100
	except:
		positivity = float("NaN")

	print ("Ontario Wide")
	print ("Under 40: %i" % int(under40Count/num_days))
	print ("Over 40: %i" % int(over40Count/num_days))
	print ("Total: %i" % int(totalCount/num_days))

	try:
		print ("Backlog: %i" % backlog)
	except:
		print ("Backlog: NA")
	
	print ("TestsCompleted: %i" % testscompleted)
	print ("Positivity: %f pct" % positivity)
	print ("Hospitalized: %i" % hospitalized)
	print ("In ICU: %i" % inICU)
	
strToday = datetime.today().strftime('%Y-%m-%d')

filename = "/Users/matti/Desktop/Covid/covidtesting_"+strToday+".csv"



reported_date = 0
pctPos = 10
tests = 9


	
count = 0
fullline = ""
PctPosLastDay = {}
TestsLastDay = {}




print ("%s" % filename)
with open(filename, newline='') as csvfile:
	activityReader = csv.reader(csvfile, delimiter=',', quotechar='\"')

	for line in activityReader:

		if (count == 0):
			count = count + 1
		else:
			print(line[pctPos])
			try:
				PctPosLastDay[line[reported_date]] = float(line[pctPos])
			except:
				PctPosLastDay[line[reported_date]] = 0
			try:
				TestsLastDay[line[reported_date]] = float(line[tests])
			except:
				TestsLastDay[line[reported_date]] = 0

## PctPos

chartPoint = []
chartX = []
for i in sorted(PctPosLastDay):
	refDateStr = "2021-12-01"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		chartX.append(i[-5:])
		chartPoint.append(PctPosLastDay[i])
		print(i)
		print(PctPosLastDay[i])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

num_series = pd.Series(chartPoint)
windows = num_series.rolling(7)
mov_avg = windows.mean()

mov_avg_list = mov_avg.tolist()

daysToPlot = -15


#plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
plt.plot(chartX,chartPoint,'r.')
plt.title('Percent Positivity -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.xlabel('Date')
plt.ylabel('%')


plt.savefig('/Users/matti/GitHub/casePlots/pos.png')
plt.clf()

## Tests

chartPoint = []
chartX = []
for i in sorted(TestsLastDay):
	refDateStr = "2021-09-01"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		chartX.append(i[-5:])
		chartPoint.append(TestsLastDay[i])
		print(i)
		print(TestsLastDay[i])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

num_series = pd.Series(chartPoint)
windows = num_series.rolling(7)
mov_avg = windows.mean()

mov_avg_list = mov_avg.tolist()

daysToPlot = -15


#plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
plt.plot(chartX,chartPoint,'r.')
plt.plot(chartX,mov_avg_list)
plt.title('Tests Completed -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.xlabel('Date')
plt.ylabel('Tests')


plt.savefig('/Users/matti/GitHub/casePlots/tests.png')
plt.clf()
