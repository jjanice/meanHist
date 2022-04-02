"""
================================================================================
meanHist utilities

make pv lists needed by meanHist
Some stolen from CMIM's Utility.py - thanks, Zack!
Also getData which returns means, stds, and archive data for a selected group of signals
J Nelson 2 April 2022
================================================================================
"""
import numpy as np
import datetime
import matplotlib.dates as mdates
from lcls_tools.data_analysis.archiver import Archiver, ArchiverData

# ==============================================================================
# GLOBAL CONFIGURATION
# ==============================================================================

#TIMERANGES=["last24h","last3days","last4days","last7days","last2weeks","lastmonth"]
#TIMEDAYS=[1 3 4 7 14 30]
TIMERANGES=["last24h","last3days","last4days","last7days","last1h"]
TIMEDAYS=[1,3,4,7,0.05]
PLOTS=['Insul Vac', 'Scav Vac', 'Cplr Vac', 'Beamline Vac', 'US HOMs', 
       'DS HOMs', 'STEPTEMPs', 'CPLRTEMP1s', 'CPLRTEMP2s', 'He Ves Temps',
       'Line A','Line B1','Line B2','Line C','Line D','Line E',
       'Line F','Shield','Liquid Levels','CM Pressures']
# ==============================================================================
# GETTERS
# ==============================================================================

def timeranges(): return TIMERANGES
def timedays(): return TIMEDAYS
def plots(): return PLOTS

def getData(statusLabel, progressBar, pvl, starttime, stoptime):
  # inputs Qlabel to write status to, list of PVs to fetch, 
  #  start and stop times in datetimes for archiver data pull
  # outputs means, stds, pvlist, and archiveData for vac sys
  #

  # initialize lists to receive PVs for what to plot
  alldata=[]
  means=[]
  stds=[]
  results={}

  # Initialize archiver class
  archiver=Archiver("lcls")

  if len(pvl)==0:
    print('Need a list of PVs to fetch data for')
    return [], [], [], []

  # show progress bar and warn user
  progressBar.show()
  statusLabel.setText("Fetching {} PVs.".format(len(pvl)))
  #statusLabel.repaint()

  # save start time to report later
  begin=datetime.datetime.now()
  for id,pv in enumerate(pvl):
  # for each pv get archived data from start to stop and store in results[]
  # use id to draw progressBar
    try:
      onedata=archiver.getValuesOverTimeRange([pv],starttime,stoptime)
      result={"times":[],"values":[]}
      result["values"]=onedata.values[pv]
      result["times"]=onedata.timeStamps[pv]
      results[pv]=result
      progressBar.setValue(round(100*id/len(pvl)))
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
    statusLabel.setText("Fetched {0} pvs in {1} seconds".format( len(pvl),
                                                               (donetime-begin).total_seconds()))
  # Hey! We got something!
  # Calculate and gather up means and stds
  if len(results)>0:
    for pv in pvl:
      if len(results[pv]['values'])>1:
        means.append(np.mean(results[pv]['values']))
        stds.append(np.std(results[pv]['values']))
      else:
        means.append(0)
        stds.append(0)
  # We're done!
  progressBar.setValue(100)

  return means, stds, pvl, results

