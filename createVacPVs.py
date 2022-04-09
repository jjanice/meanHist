import os
import meme.names

def createVacPVs():
  # creates a list of lists - each smaller one is a list of PVs for 
  # a given requested plot like insulating vacuum, Line A temps, etc.
  # The big list is in order of the pulldown on the GUI.
  # The items in the smaller lists are sorted by unit number
  # Beware: CM H1 & H2 come at the end. I'm not clever enough to fix

  #  need to be on a machine with mcc-dmz in EPICS_CA_ADDR_LIST for 
  #  meme.names to work

  # Going to double up the duty here and have it pass back a list of 
  #  which is the interesting parts of the pv name 
  #  for the xaxis named juicyBits
  #  If juicyBits = 1, then just use the 2nd field of PVN, if it's 2
  #  then use the 2nd and 3rd fields
  #  with apologies to anyone trying to read this.

  # Triple duty...
  #  Add ylabel for that plot type

  # thoughts about how to sort the Hs between cm03 and cm04
  # specials=['abc','def','ghi','jkl']
  # to-be-sorted=['abc','ghi','xyz','qrs']
  # temp2=set(to-be-sorted).difference(specials)
  # sorted_cols = [a for a in specials if a in to-be-sorted} + sorted(list(temp2))
  # sorted_cols=['abc','ghi','xyz','qrs']
  # make specials be cm01, cm02, ch03, h1, and h2
  # https://stackoverflow.com/questions/47158267/sort-list-and-force-certain-elements-to-be-first

  # Start with the vacuum lists

  #these will be lists of pvs for vac devices in the following systems:
  #   coupler, beamline, insulating, and scavenger pump, respectively.
  pvcplr=[]
  pvbl=[]
  pvins=[]
  pvscav=[]
  pvls=[]
  juicyBits=[]
  yLabels=[]

  # Double check that we're on the dmz network
  caAddrList=os.environ['EPICS_CA_ADDR_LIST']
  if 'mcc-dmz' not in caAddrList:
    print('Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc)')
    return []

  # this is the 2nd part of the PV name in rough Z order (thanks DIAG0!)
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
    # remove empty strings i.e. VGCC and VGPR that are covered by a VGXX
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

    # sort by unit number - feels awfully clever
    pvl.sort(key=sortThird)

    # figure out if device is for
    #    beamline, coupler, insulating vacuum, or scav pump system
    coupler=['09', '14', '19', '39', '49']

    for pv in pvl:
      # split the pv at the colons and scrutinize the unit number (field [2])
      pvspl=pv.split(':')
      # find four digit unit numbers
      if len(pvspl[2])==4:
        # put in right list based on last two digits
        if pvspl[2][-2:] in coupler:
          pvcplr.append(pv)
        # insulating vac devices
        elif pvspl[2][-2:]=='96':
          pvins.append(pv)
        # scav pump system
        elif pvspl[2][-2:]=='95':
          pvscav.append(pv)
        # beamline devices
        else:
          pvbl.append(pv)
      # if not a 4-digit number, then it's a beamline device
      else:
        pvbl.append(pv)

  return pvins,pvscav,pvcplr,pvbl

