"""
================================================================================
meanHist utilities

make pv lists needed by meanHist
Some stolen from CMIM's Utility.py - thanks, Zack!
Also getData which returns means, stds, and archive data for a selected group of signals
J Nelson 2 April 2022
================================================================================
Mods:
20 Apr 2022 J Nelson
  added kludge to check if pv fetched from archiver is ds:press to divide
    the returned values by 1000 to convert mbara to bara with apologies.

"""
import numpy as np
import datetime
import matplotlib.dates as mdates
from lcls_tools.data_analysis.archiver import Archiver, ArchiverData

# ==============================================================================
# GLOBAL CONFIGURATION
# ==============================================================================

TIMERANGES=["last24h","last3days","last4days","last7days","last1h"]
TIMEDAYS=[1,3,4,7,0.05]

def getData(statusLabel, progressBar, plotz):
  # inputs Qlabel to write status to, list of PVs to fetch, 
  #  start and stop times in datetimes for archiver data pull
  #  start and stop times hiding in plotType variable named plotz
  # outputs means, stds, pvlist, and archiveData in the plotType variable
  #

  # initialize lists to receive PVs for what to plot
  alldata=[]
  means=[]
  stds=[]
  results={}

  # Initialize archiver class
  archiver=Archiver("lcls")

  if len(plotz.pvList)==0:
    print('Need a list of PVs to fetch data for')
    return [], [], [], []

  # show progress bar and warn user
  progressBar.show()
  statusLabel.setText("Fetching {} PVs.".format(len(plotz.pvList)))
  #statusLabel.repaint()

  # save start time to report later
  begin=datetime.datetime.now()
  for id,pv in enumerate(plotz.pvList):

  # for each pv get archived data from start to stop and store in results[]
  # use id to draw progressBar
    try:
      onedata=archiver.getValuesOverTimeRange([pv],
                                              plotz.starttime,
                                              plotz.stoptime)
      result={"times":[],"values":[]}
      if 'DS:PRESS' in pv:
        scaleFactor=.001
        result["values"]=[value*scaleFactor for value in onedata.values[pv]]
      else:
        result["values"]=onedata.values[pv]
      result["times"]=onedata.timeStamps[pv]
      results[pv]=result
      progressBar.setValue(round(100*id/len(plotz.pvList)))
    # Sometimes archiver barfs, put in empty lists
    except:
      result={"times":[],"values":[]}
      results[pv]=result

  # Get finish time and report to user how it went - either in window (debug)
  #  or on statusLabel on GUI
  donetime=datetime.datetime.now()
  if statusLabel == None:
    print("Data is fetched. Elapsed time: {} seconds".format((donetime-begin).total_seconds()))
  else:
    statusLabel.setText("Fetched {0} pvs in {1} seconds".format( len(plotz.pvList),
                                                               (donetime-begin).total_seconds()))

  # Hey! We got something!
  # Calculate and gather up means and stds
  if len(results)>0:
    for pv in plotz.pvList:
      if len(results[pv]['values'])>1:
        means.append(np.mean(results[pv]['values']))
        stds.append(np.std(results[pv]['values']))
      else:
        means.append(0)
        stds.append(0)
  # We're done!
  progressBar.setValue(100)

  plotz.means=means
  plotz.stds=stds
  plotz.archiveData=results

  return plotz

