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


def xfmt(x,pos=None):
    ''' custom date formatting '''
    x = mdates.num2date(x)
    label = x.strftime('%m/%d')
    label = label.lstrip('0')
    return label

phus = "All"
filename = ""

strToday = datetime.today().strftime('%Y-%m-%d')

filename = "/Users/matti/Desktop/Covid/schoolcovidsummary_"+strToday+".csv"


hostInfo = os.uname()

if "Matti-MacBook-Pro.local" not in hostInfo:
	os.system("curl https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7fbdbb48-d074-45d9-93cb-f7de58950418/download/schoolcovidsummary.csv > ~/Desktop/Covid/schoolcovidsummary_"+strToday+".csv")
	os.system("curl https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/8b6d22e2-7065-4b0f-966f-02640be366f2/download/schoolsactivecovid.csv > ~/Desktop/Covid/schoolsactivecovid_"+strToday+".csv")
	os.system("curl https://data.ontario.ca/dataset/b1fef838-8784-4338-8ef9-ae7cfd405b41/resource/7e644a48-6040-4ee0-9216-1f88121b21ba/download/schoolcovidsummary2021_2022.csv > ~/Desktop/Covid/schoolcovidsummary2021_2022_"+strToday+".csv"")

fd=open(filename,'r')
today=fd.readlines() # Read entire contents of file
fd.close()



reported_date = 1
current_schools_w_cases = 2
current_schools_closed = 3
cumulative_school_related_student_cases = 18
cumulative_school_related_staff_cases = 19 
cumulative_school_related_unspecified_cases = 20


	
count = 0

fullline = ""

schoolsWithCases = {}
schoolsClosed = {}
cumulativeStudentCases = {}
cumulativeStaffCases = {}
cumulativeUnspecifiedCases = {}



print ("%s" % filename)
with open(filename, newline='') as csvfile:
	activityReader = csv.reader(csvfile, delimiter=',', quotechar='\"')

	for line in activityReader:

		if (count == 0):
			count = count + 1
		else:
			schoolsWithCases[line[reported_date]] = int(line[current_schools_w_cases])
			schoolsClosed[line[reported_date]] = int(line[current_schools_closed])
			cumulativeStudentCases[line[reported_date]] = int(line[cumulative_school_related_student_cases])
			cumulativeStaffCases[line[reported_date]] = int(line[cumulative_school_related_staff_cases])
			try:
				cumulativeUnspecifiedCases[line[reported_date]] = int(line[cumulative_school_related_unspecified_cases])
			except:
				cumulativeUnspecifiedCases[line[reported_date]] = 0

## Schools with Cases

chartPoint = []
for i in sorted(schoolsWithCases):
	refDateStr = "2020-07-30"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		chartX.append(i[-5:])
		chartPoint.append(schoolsWithCases[i])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

num_series = pd.Series(chartPoint)
windows = num_series.rolling(7)
mov_avg = windows.mean()

mov_avg_list = mov_avg.tolist()

daysToPlot = -150


plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
#plt.plot(chartX[daysToPlot:],mov_avg_list[daysToPlot:])
plt.title('Schools With Cases -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.xlabel('Date')
plt.ylabel('Schools')


plt.savefig('/Users/matti/GitHub/casePlots/Schools/school1.png')
plt.clf()


## Schools Closed

chartPoint = []
for i in sorted(schoolsClosed):
	refDateStr = "2020-07-30"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		#chartX.append(i[-5:])
		chartPoint.append(schoolsClosed[i])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

num_series = pd.Series(chartPoint)
windows = num_series.rolling(7)
mov_avg = windows.mean()

mov_avg_list = mov_avg.tolist()

daysToPlot = -150


plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:])
#plt.plot(chartX[daysToPlot:],mov_avg_list[daysToPlot:])
plt.title('Schools Closed -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.xlabel('Date')
plt.ylabel('Schools')


plt.savefig('/Users/matti/GitHub/casePlots/Schools/school2.png')
plt.clf()

## Cumulative Cases

chartPoint = []
chartPoint2 = []
chartPoint3 = []

for i in sorted(cumulativeStudentCases):
	refDateStr = "2020-07-30"
	if(datetime.strptime(i,'%Y-%m-%d') > datetime.strptime(refDateStr,'%Y-%m-%d')):
		#chartX.append(i[-5:])
		chartPoint.append(cumulativeStudentCases[i])
		chartPoint2.append(cumulativeStaffCases[i])
		chartPoint3.append(cumulativeUnspecifiedCases[i])
		#chartX.append(i)
		

xdates = [dt.strptime(dstr,'%m-%d') for dstr in chartX]

num_series = pd.Series(chartPoint)
windows = num_series.rolling(7)
mov_avg = windows.mean()

mov_avg_list = mov_avg.tolist()

daysToPlot = -150


plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.',label='Students')
plt.plot(chartX[daysToPlot:],chartPoint2[daysToPlot:],'b.',label='Staff')
plt.plot(chartX[daysToPlot:],chartPoint3[daysToPlot:],'m.',label='Unspecified')
plt.title('Cumulative Student/Staff Cases -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=4))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())

plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend(loc='best')


plt.savefig('/Users/matti/GitHub/casePlots/Schools/school3.png')
plt.clf()