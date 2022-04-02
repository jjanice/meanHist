import os
import meme.names

def createVacList():
  # creates a list of vacuum pvs in areas L0B-SPH/D/S
  # sorted by z and divided by category:
  #   insulating, scavenger pump, coupler, and beamline respectively.
  # return pvins, pvscav, pvcplr, pvbl

  #  need to be on a machine with mcc-dmz in EPICS_CA_ADDR_LIST for 
  #  meme.names to work

  #these will be lists of pvs for vac devices in the following systems:
  #   coupler, beamline, insulating, and scavenger pump, respectively.
  pvcplr=[]
  pvbl=[]
  pvins=[]
  pvscav=[]
  pvls=[]

  caAddrList=os.environ['EPICS_CA_ADDR_LIST']
  if 'mcc-dmz' not in caAddrList:
    print('Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc)')
    return [], [], [], []

  areas=['L0B','HTR','COL0','DIAG0','L1B','BC1B','COL1','L2B','BC2B','EMIT2',
  'L3B','EXT','DOG']

  for nn in range(13,28):
    areas.append('BPN'+str(nn))
  areas.append('SPH')
  areas.append('SPD')
  areas.append('SPS')

  # cycle through areas
  for area in areas:
    # fetch list of vac PVs in area
    pvl=meme.names.list_pvs('V%:'+area+':%:P')
    #print('area {0} npvs {1}'.format(area,len(pvl)))
    #Check for vgcc/vgpr that feed into VGXX
    for pvxx in pvl:
      if 'VGXX' in pvxx:
        for idpv,pv in enumerate(pvl):
          if 'VGCC' in pv or 'VGPR' in pv:
            if pv[4:]==pvxx[4:]:
              pvl[idpv]=''
    # VGXX:L2B:1449 doesn't exist
    if area=='L2B':
      pvl.remove('VGXX:L2B:1449:P')
    # remove empty strings
    pvl=list(filter(None,pvl))

    # make VPIOs end with PMON
    # and VGXX end with COMBO_P
    for id,pv in enumerate(pvl):
      if 'VGXX' in pv:
        pvl[id]=pvl[id][:-1]+'COMBO_P'
      elif 'VPIO' in pv:
        pvl[id]=pvl[id]+'MON'

    # sort by unit number
    def sortThird(pvn):
      unitnostr=pvn.split(':')[2]
      try:
        unitno=int(unitnostr)
      except:
        try:
          unitnostr='1'+unitnostr[1:]
          unitno=int(unitnostr)
        except:
          unitno=9999
      return unitno

    pvl.sort(key=sortThird)

    # figure out if device is for
    #    beamline (3), coupler(2), insulating vacuum(0), or scav pump system(1)
    coupler=['09', '14', '19', '39', '49']

    for pv in pvl:
      pvspl=pv.split(':')
    # find four digit unit numbers
      if len(pvspl[2])==4:
    # sort by last two digits
        if pvspl[2][-2:] in coupler:
          pvcplr.append(pv)
        elif pvspl[2][-2:]=='96':
          pvins.append(pv)
        elif pvspl[2][-2:]=='95':
          pvscav.append(pv)
        else:
          pvbl.append(pv)
      else:
        pvbl.append(pv)

  # Packup return variable
  pvls.append(pvins)
  pvls.append(pvscav)
  pvls.append(pvcplr)
  pvls.append(pvbl)

# CRYO
  pvls.append(meme.names.list_pvs('CTE:%:UH:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:DH:TEMP'))
  pvls.append(meme.names.list_pvs('ACCL:%:%:STEPTEMP'))
  pvls.append(meme.names.list_pvs('ACCL:%:%:CPLRTEMP1'))
  pvls.append(meme.names.list_pvs('ACCL:%:%:CPLRTEMP2'))
  pvls.append(meme.names.list_pvs('CTE:%:%:V%:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:A1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:B1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:B2:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:C1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:D1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:E1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:F1:TEMP'))
  pvls.append(meme.names.list_pvs('CTE:%:%:S1:TEMP'))
  pvls.append(meme.names.list_pvs('CLL:CM%:%:%:LVL'))
  pvls.append(meme.names.list_pvs('CPT:CM%:%:%S:PRESS'))

  return pvls

