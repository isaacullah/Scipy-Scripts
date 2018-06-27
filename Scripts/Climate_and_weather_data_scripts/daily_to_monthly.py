#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 10:19:55 2018

Convert daily precipitation data to monthly summaries of total rainfal and
number of rain days.
Expects a multindex csv file where first column is integer "year", second is integer "month", and
third is integer "day."

@author: iullah
"""

import pandas as pd
import os

cwd = os.getcwd() # get current working directory
csv = "%s%sGHCN_Palermo_precip_dailies_1797-2008.csv" % (cwd, os.sep) # name of input csv file
df = pd.read_csv(csv, skiprows=6, na_values=-9999, parse_dates= [[0,1,2]], index_col="year_month_day") # import from csv, and convert to a date time index data frame
monthlyprecip = df.groupby(pd.Grouper(freq='M')).sum()  # sum precip by month

monthlyraindays = df.mask(df.PRCP.eq(0)).groupby(pd.Grouper(freq='M')).count() #count non-zero rainfal days per month
# write out files
monthlyprecip.to_csv("%s%sMonthly_Precip_tots_%s" % (cwd, os.sep, csv.split(os.sep)[-1]))
monthlyraindays.to_csv("%s%sMonthly_rain_days_%s" % (cwd, os.sep, csv.split(os.sep)[-1]))
exit(0)
