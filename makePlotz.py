from createVacPVs import createVacPVs
import os
import meme.names

class PlotType:
  def __init__(self,name,pvList=None,xLabelPart=1,yLabel='',starttime=None,
               stoptime=None,means=None,stds=None,archiveData=None,getData=True):
    # name is the name of the group of PVs
    # pvList is the list of PVs
    # xLabelPart is whether to show CMxx or LxB:MMcc
    # yLabel is the label for the y axis
    # starttime is the start time for the archiver data fetch
    # stoptime is the stop time for the archiver data fetch
    # means is the list of the mean of each PV's archiver data
    # stds is the list of the std dev of each PV's archiver data
    # archiveData is the dict of the archiveData that was fetched
    # getData is a flag to request a new fetch from the archiver (True) or show old data

    self.name = name
    if pvList is None:
      pvList=[]
    self.pvList = pvList
    self.xLabelPart = xLabelPart
    self.yLabel = yLabel
    self.starttime = starttime
    self.stoptime = stoptime
    if means is None:
      means=[]
    self.means = means
    if stds is None:
      stds=[]
    self.stds = stds
    if archiveData is None:
      archiveData={}
    self.archiveData = archiveData
    self.getData = getData

def makePlotz():
  caAddrList=os.environ['EPICS_CA_ADDR_LIST']
  if 'mcc-dmz' not in caAddrList:
    print('Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc)')

  Plotz=[]

# Call createPVList to sort out the vacuum signals
  pvins, pvscav, pvcplr, pvbl = createVacPVs()

  Plotz.append(PlotType(name='Insul Vac',
                        pvList=pvins,
                        xLabelPart=2,
                        yLabel='Pressure (Torr)'))

  Plotz.append(PlotType(name='Scav Vac',
                        pvList=pvscav,
                        xLabelPart=2,
                        yLabel='Pressure (Torr)'))

  Plotz.append(PlotType(name='Cplr Vac',
                        pvList=pvcplr,
                        xLabelPart=2,
                        yLabel='Pressure (Torr)'))

  Plotz.append(PlotType(name='Beamline Vac',
                      pvList=pvbl,
                      xLabelPart=2,
                      yLabel='Pressure (Torr)'))

  pvl=meme.names.list_pvs('CTE:%:UH:TEMP')
  Plotz.append(PlotType(name='US HOMS',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:DH:TEMP')
  Plotz.append(PlotType(name='DS HOMS',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('ACCL:%:%:STEPTEMP')
  Plotz.append(PlotType(name='STEPTEMPs',
                      pvList=pvl,
                      xLabelPart=2,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('ACCL:%:%:CPLRTEMP1')
  Plotz.append(PlotType(name='CPLRTEMP1s',
                      pvList=pvl,
                      xLabelPart=2,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('ACCL:%:%:CPLRTEMP2')
  Plotz.append(PlotType(name='CPLRTEMP2s',
                      pvList=pvl,
                      xLabelPart=2,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:V%:TEMP')
  Plotz.append(PlotType(name='He Ves Temps',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:A1:TEMP')
  Plotz.append(PlotType(name='Line A',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:B1:TEMP')
  Plotz.append(PlotType(name='Line B1',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:B2:TEMP')
  Plotz.append(PlotType(name='Line B2',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:C1:TEMP')
  Plotz.append(PlotType(name='Line C',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:D1:TEMP')
  Plotz.append(PlotType(name='Line D',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:E1:TEMP')
  Plotz.append(PlotType(name='Line E',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:F1:TEMP')
  Plotz.append(PlotType(name='Line F',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:%:S1:TEMP')
  Plotz.append(PlotType(name='Shield',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CLL:CM%:%:%:LVL')
  Plotz.append(PlotType(name='Liquid Levels',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Liquid Level (%)'))

  pvl=meme.names.list_pvs('CPT:CM%:%:%S:PRESS')
  Plotz.append(PlotType(name='CM Pressures',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Two-phase line pressure (bara)'))

  pvl=meme.names.list_pvs('CPV:%:3001:JT:POS_RBV')
  Plotz.append(PlotType(name='JTs',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Valve Percentage Open (%)'))

  pvl=meme.names.list_pvs('CTE:%:2514:CD:TEMP')
  Plotz.append(PlotType(name='CD Line 1',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('CTE:%:2515:CD:TEMP')
  Plotz.append(PlotType(name='CD Line 2',
                      pvList=pvl,
                      xLabelPart=1,
                      yLabel='Temperature ($^\circ$K)'))

  pvl=meme.names.list_pvs('RADM:SYS0:100:%:GAMMAAVE')
  Plotz.append(PlotType(name='Decarad 1 Aves',
                      pvList=pvl,
                      xLabelPart=4,
                      yLabel='Dose Rate (mR/hr)'))

  pvl=meme.names.list_pvs('RADM:SYS0:200:%:GAMMAAVE')
  Plotz.append(PlotType(name='Decarad 2 Aves',
                      pvList=pvl,
                      xLabelPart=4,
                      yLabel='Dose Rate (mR/hr)'))

  return Plotz
