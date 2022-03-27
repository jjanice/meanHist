"""
================================================================================
plotVacs utilities

list variables needed by plotVacs
Most stolen from CMIM's Utility.py - thanks, Zack!
Also getData which returns means, stds, and archive data for a selected vac sys
J Nelson 3/26/2022
================================================================================
"""
from createVacList import createVacList
import meme.archive
import numpy as np
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates
from lcls_tools.data_analysis.archiver import Archiver, ArchiverData

# ==============================================================================
# GLOBAL CONFIGURATION
# ==============================================================================

#TIMERANGES=["last24h","last3days","last4days","last7days","last2weeks","lastmonth"]
#TIMEDAYS=[1 3 4 7 14 30]
TIMERANGES=["last24h","last3days","last4days","last7days"]
TIMEDAYS=[1,3,4,7]
VACSYS=['Insulating','Scavenger','Coupler','Beamline']
# ==============================================================================
# GETTERS
# ==============================================================================

def timeranges(): return TIMERANGES
def timedays(): return TIMEDAYS
def vacsyses(): return VACSYS

def getData(statusLabel,progressBar,vidx, starttime, stoptime):
# inputs Qlabel to write status to, index for vac sys, 
#  start and stop times in datetimes for archiver data pull
# outputs means, stds, pvlist, and archiveData for vac sys
#
# initialize lists to receive PVs for vac systems
  pvls=[[] for ii in range(4)]
# if vidx is too big, this won't end well.
  if vidx>(len(pvls)-1):
    return [],[],[]
# initialize return variables
  alldata=[]
  means=[]
  stds=[]
  results={}
  archiver=Archiver("lcls")
# these correspond to ins scav cplr and bl vac respectively
  pvls[0],pvls[1],pvls[2],pvls[3] = createVacList()
  pvl=pvls[vidx]
#  try:
  begin=datetime.datetime.now()
  for id,pv in enumerate(pvl):
    try:
      onedata=archiver.getValuesOverTimeRange([pv],starttime,stoptime)
      result={"times":[],"values":[]}
      result["values"]=onedata.values[pv]
      result["times"]=onedata.timeStamps[pv]
      results[pv]=result
      progressBar.setValue(round(100*id/len(pvl)))
    except:
      result={"times":[],"values":[]}
      results[pv]=result
  donetime=datetime.datetime.now()
  if statusLabel == None:
    print("Data is fetched. Elapsed time: {} seconds".format((donetime-begin).total_seconds()))
  else:
    statusLabel.setText("Fetched {0} pvs in {1} seconds".format( len(pvl),
                                                               (donetime-begin).total_seconds()))

  if len(results)>0:
    for pv in pvl:
      if len(results[pv]['values'])>1:
        means.append(np.mean(results[pv]['values']))
        stds.append(np.std(results[pv]['values']))
      else:
        means.append(0)
        stds.append(0)

  progressBar.setValue(100)

  return means, stds, pvl, results # alldata

