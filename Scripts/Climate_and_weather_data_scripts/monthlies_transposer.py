#!/usr/bin/python
import pandas as pd
import numpy as np
import os

#transposes a climate file

####### Edit these values #######
f = "Monthly_rain_days_GHCN_Palermo_precip_dailies_1797-2008.csv" # Input csv file
n = 12 # Number of new columns
names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] # Names of new columns
#################################

cwd = os.getcwd()
#csv = pd.read_csv(cwd + os.sep() + f)
csv = pd.read_csv(f, skiprows=1, header=None)
print csv.shape[0]
print len(csv)
transposed = pd.DataFrame(csv[1].values.reshape(-1, n), columns=names)
#transposed = pd.DataFrame(np.reshape(csv.values,(csv.shape[0]/n,n)), columns=names)
#transposed.to_csv(cwd + os.sep() + f)
transposed.to_csv("transposed_%s" % f)
exit(0)
