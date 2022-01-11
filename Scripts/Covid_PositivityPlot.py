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
	refDateStr = "2021-12-01"
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
plt.title('Tests Completed -' + strToday)

plt.setp(plt.gca().xaxis.get_majorticklabels(),rotation=60)
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=3))
plt.gca().xaxis.set_minor_locator(mdates.DayLocator())
plt.xlabel('Date')
plt.ylabel('%')


plt.savefig('/Users/matti/GitHub/casePlots/tests.png')
plt.clf()
