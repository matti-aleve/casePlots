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

filename = "/Users/matti/Desktop/Covid/lcccovidsummary_"+strToday+".csv"


hostInfo = os.uname()



if "Matti-MacBook-Pro.local" not in hostInfo:
	os.system("curl https://data.ontario.ca/dataset/5bf54477-6147-413f-bab0-312f06fcb388/resource/74f9ac9f-7ca8-4860-b2c3-189a2c25e30c/download/lcccovidsummary.csv > ~/Desktop/Covid/lcccovidsummary_" + strToday + ".csv")

sys.exit()

fd=open(filename,'r')
today=fd.readlines() # Read entire contents of file
fd.close()



reported_date = 1
current_lcc_centres_w_cases = 2    
current_lcc_centres_closed = 3		
cumulative_lcc_related_child_cases = 24
cumulative_lcc_related_staff_cases = 25 
cumulative_lcc_related_unspecified_cases = 26


	
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
			schoolsWithCases[line[reported_date]] = int(line[current_lcc_centres_w_cases])
			schoolsClosed[line[reported_date]] = int(line[current_lcc_centres_closed])
			cumulativeStudentCases[line[reported_date]] = int(line[cumulative_lcc_related_child_cases])
			cumulativeStaffCases[line[reported_date]] = int(line[cumulative_lcc_related_staff_cases])
			try:
				cumulativeUnspecifiedCases[line[reported_date]] = int(line[cumulative_lcc_related_unspecified_cases])
			except:
				cumulativeUnspecifiedCases[line[reported_date]] = 0


## LCC with Cases

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

daysToPlot = -200


plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
#plt.plot(chartX[daysToPlot:],mov_avg_list[daysToPlot:])
plt.title('Licensed Child Care Centres With Cases -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())

plt.xlabel('Date')
plt.ylabel('Facilities')


plt.savefig('/Users/matti/GitHub/casePlots/LCC/LCC1.png')
plt.clf()


## LCC Closed

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



plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.')
plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:])
#plt.plot(chartX[daysToPlot:],mov_avg_list[daysToPlot:])
plt.title('Licensed Child Care Centres Closed -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())

plt.xlabel('Date')
plt.ylabel('Facilities')


plt.savefig('/Users/matti/GitHub/casePlots/LCC/LCC2.png')
plt.clf()

## New Student Cases

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



plt.plot(chartX[daysToPlot:],chartPoint[daysToPlot:],'r.',label="Children")
plt.plot(chartX[daysToPlot:],chartPoint2[daysToPlot:],'b.',label="Staff")
plt.plot(chartX[daysToPlot:],chartPoint3[daysToPlot:],'m.',label="Unspecified")
plt.title('Cumulative Child/Staff Cases -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=15))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())

plt.xlabel('Date')
plt.ylabel('Cases')
plt.legend(loc='best')

plt.savefig('/Users/matti/GitHub/casePlots/LCC/LCC3.png')
plt.clf()