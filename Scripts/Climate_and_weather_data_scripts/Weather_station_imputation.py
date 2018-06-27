#!/usr/bin/python
import pandas as pd
from fancyimpute import SoftImpute, MICE, KNN

'''
Takes multiple weather station data files as monthly values, imputes missing cases, and then outputs filled data sets. Requires Pandas and Fancyimpute. Install these packages before running this script.

All must be same dimension, and currently expect rows to be years, and columns to be monthly data,
Jan through Dec. Single column sequential monthly data can be reshaped thusly with "monthlies_transposer.py."

Missing cases should be coded as 'NaN'.

Edit the header below (read the inline comments for help) and execute on the command line:

    >>python  Weather_station_imputation.py

Author: Isaac I. Ullah, PhD. 
iullah@sdsu.edu
'''

####### Edit these values #######
station1 = "Bova_Superiore_rain_days_1902_2018.csv" # Input csv files of weather data. All must be same dimension, and currently expect rows to be years, and columns to be monthly data, Jan through Dec. Single column sequential monthly data can be reshaped thusly with "transposer.py" Missing cases should be coded as 'NaN'.
station2 = "Motta_San_Giovanni_rain_days_1902_2018.csv"
station3 = "Reggio_Calabria_rain_days_1902_2018.csv"
station4 = "Palermo_GHCN_rain_days_1902_2018.csv"
Round = True # Should the imputed values be rounded to nearest integer? Good for integer values like rain days.
method = "MICE" # The imputation method to use. Should be one of "KNN," "MICE", or "SoftImpute".
n = 12 # Number of columns (we are doing months, but you can edit this to match anything)
names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"] # Names of columns for output. Should be same number of names as value "n".
#################################

# Import csv files to dataframes and stack to get all values into one column.
station1df = pd.read_csv(station1, index_col = 0).stack(dropna=False).reset_index()
station1df.columns = ['Year','Month','Value']
station2df = pd.read_csv(station2, index_col = 0).stack(dropna=False).reset_index()
station2df.columns = ['Year','Month','Value']
station3df = pd.read_csv(station3, index_col = 0).stack(dropna=False).reset_index()
station3df.columns = ['Year','Month','Value']
station4df = pd.read_csv(station4, index_col = 0).stack(dropna=False).reset_index()
station4df.columns = ['Year','Month','Value']

# Wrangle all data into one dataframe
allstations = pd.concat([station1df["Value"],station2df["Value"],station3df["Value"],station4df["Value"]], axis = 1)
allstations.columns = ["station1", "station2", "station3", "station4"]

# Run the selected imputation routine to fill all missing cases
if method == "SoftImpute":
    allstations_complete = pd.DataFrame(data=SoftImpute().complete(allstations), columns=allstations.columns, index=allstations.index)
elif method == "KNN":
    allstations_complete = pd.DataFrame(data=KNN().complete(allstations), columns=allstations.columns, index=allstations.index)
elif method == "MICE":
    allstations_complete = pd.DataFrame(data=MICE().complete(allstations), columns=allstations.columns, index=allstations.index)
else:
    print "Sorry, the imputation method %s is not available, try MICE, KNN, or SoftImpute" % method

# Unstack the data to get values back in monthly columns, and then Output the filled datasets with appended prefixes to the input filenames. Round data values to nearest integer if asked.
if Round is True:
    pd.DataFrame(allstations_complete["station1"].values.reshape(-1, n), columns=names).round(0).astype("int32").to_csv("%sfilled_%s" % (method, station1))
    pd.DataFrame(allstations_complete["station2"].values.reshape(-1, n), columns=names).round(0).astype("int32").to_csv("%sfilled_%s" % (method, station2))
    pd.DataFrame(allstations_complete["station3"].values.reshape(-1, n), columns=names).round(0).astype("int32").to_csv("%sfilled_%s" % (method, station3))
    pd.DataFrame(allstations_complete["station4"].values.reshape(-1, n), columns=names).round(0).astype("int32").to_csv("%sfilled_%s" % (method, station4))
else:
    pd.DataFrame(allstations_complete["station1"].values.reshape(-1, n), columns=names).round(1).to_csv("%sfilled_%s" % (method, station1))
    pd.DataFrame(allstations_complete["station2"].values.reshape(-1, n), columns=names).round(1).to_csv("%sfilled_%s" % (method, station2))
    pd.DataFrame(allstations_complete["station3"].values.reshape(-1, n), columns=names).round(1).to_csv("%sfilled_%s" % (method, station3))
    pd.DataFrame(allstations_complete["station4"].values.reshape(-1, n), columns=names).round(1).to_csv("%sfilled_%s" % (method, station4))

# All done!
exit(0)
