# 
# meanHist
# J. Nelson
# 2 Apr 2022
#
# pydm class to go with meanHist.ui
#
# This loads up the time frame combo boxes on the ui then
# when Go! is pushed, it reads out what type of plot to make,
# fetches the data, then plots means & stds in the top subplot. If someone
# clicks a data point, it draws the history in the bottom subplot.
#

import time
from os import path, system, environ
from pydm import Display
import datetime

# util functions for this class
import meanHistUtil as util
from makePlotz import makePlotz, PlotType

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

#for the clipboard
from PyQt5.QtWidgets import QApplication

class MyDisplay(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(MyDisplay, self).__init__(parent=parent, args=args, macros=macros)

    # need to be on a machine on the mccdmz to use meme.names & get
    #  archiver data
    caAddrList=environ['EPICS_CA_ADDR_LIST']
    if 'mcc-dmz' not in caAddrList:
      print('Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc)')
      self.ui.StatusLabel.setStyleSheet("color: red;")
      self.ui.StatusLabel.setText("Need to be on an mccdmz machine (srv01, mcclogin, lcls-prod02, etc")

      # set the list of pv lists for the types of plots
      self.plotz=[]
    else:
      # get the list of pv lists for the types of plots and which 
      #  part(s) of the pv name to use for x tick labels
      self.plotz = makePlotz()

    # Get variables from utility file
    self.tranges = util.TIMERANGES
    self.tdays = util.TIMEDAYS


    # initialize matplotlib click connections
    self.ax=0
    self.ax2=0

    # connect spinner boxes to functions - these are passes for now
    self.ui.TimeComboBox.activated.connect(self.ChangeTime)
    self.ui.SysComboBox.activated.connect(self.ChangeSys)

    #Fill in ui components
    self.ui.progressBar.setValue(0)

    # system-to-plot selector
    for plotsys in self.plotz:
      self.ui.SysComboBox.addItem(plotsys.name)

    # time range selector
    for trange in self.tranges:
      self.ui.TimeComboBox.addItem(trange)

    # put a canvas for the plot in the gridlayout
    self.figure=Figure()
    self.canvas=FigureCanvas(self.figure)
    self.ui.PlotArea.addWidget(self.canvas)

    # Connect go & print buttons to functions
    self.ui.GoButton.clicked.connect(self.Go)
    self.ui.printPushButton.clicked.connect(self.printPlot)

    # Make clipboard to hold PV name - stolen from zack's CMIM
    self.cb = QApplication.clipboard()
    self.cb.clear(mode=self.cb.Selection)

    # empty the status text area
    self.ui.StatusLabel.setText("")

    # hide the progress bar until needed
    self.ui.progressBar.hide()
#    self.ui.printPushButton.hide()

  def printPlot(self):
    self.figure.savefig('meanHist.ps')
    cmd='lpr -Pphysics-lcls2log meanHist.ps'
    system(cmd)

  def Go(self):
  # function to respond to go button push
  # fetches data for the pvs requested over requested time range
  #  and plots means & stds in top plot
  #  and responds to mouse click in top plot to draw bottom plot
  #  with that dot's data (that went into calculating the mean & std

    # which set of pvs to plot (plot index)
    pidx = self.ui.SysComboBox.currentIndex()

    # time range requested?
    tidx = self.ui.TimeComboBox.currentIndex()
    self.plotz[pidx].stoptime=datetime.datetime.now()
    self.plotz[pidx].starttime=self.plotz[pidx].stoptime-datetime.timedelta(days=self.tdays[tidx])

    # if on a dmz machine, get the data - pass in statuslabel to 
    #  pass messages, progress bar to show progress, list of pvs to get,
    #  and start/stop times for fetching the data

    # Not on a dmz machine
    if self.plotz==[]:
      self.plotz[pidx].means=[]
      self.plotz[pidx].stds=[]
      self.plotz[pidx].pvList=[]
      self.plotz[pidx].archiveData=[]
    # Yay! dmz machine!
    else:
      if self.plotz[pidx].getData:
        (self.plotz[pidx]) = util.getData(self.ui.StatusLabel,
                                        self.ui.progressBar,
                                        self.plotz[pidx])
    self.ui.progressBar.hide()

    # The program starts with axes set to ints so we can tell if
    #  something has been drawn before and if so to delete it before
    #  plotting new data
    if type(self.ax)!=int:
      self.figure.delaxes(self.ax)
      self.canvas.draw()
    if type(self.ax2)!=int:
      self.figure.delaxes(self.ax2)
      self.canvas.draw()

    # add top and bottom plots/axes
    self.ax=self.figure.add_subplot(2,1,1)
    self.ax2=self.figure.add_subplot(2,1,2)
    self.ax.clear()

    # if get data fails, it sends back and empty means array - usually means
    #  user is not a machine with access to the archiver, thus the error message
    if self.plotz[pidx].means==[]:
      print('Need to be on an mccdmz machine: srv01, mcclogin, lcls-prod02, etc')
      errmsg='Use on an mccdmz machine: srv01, mcclogin, lcls-prod02, ...'
      self.ax.set_title(errmsg,loc='left',y=.85,x=.02,fontsize='small')
      self.ax.plot([1,2,3],'bo')
      self.canvas.draw()
      return
    # plot means & stds
    self.ax.errorbar(range(len(self.plotz[pidx].means)),self.plotz[pidx].means,
                     yerr=self.plotz[pidx].stds,ls='none',ecolor='black',
                     elinewidth=0.5)

    # the first 4 plots-types are vacuum so use semilog to plot the means
    #  otherwise just straight up plot
    if pidx<4:
      self.ax.semilogy(self.plotz[pidx].means,'o',color='tab:blue')
    else:
      self.ax.plot(self.plotz[pidx].means,'o',color='tab:blue')
    #  Other color choices matplotlib.org/3.5.0/gallery/color/named_colors.html

    # add a grid title, draw the canvas, and make sure the 
    #  printPushButton is showing
    self.ax.grid()
    titletext=self.plotz[pidx].name+'    '
    titletext += self.plotz[pidx].starttime.strftime('%Y-%b-%-d %-H:%M:%S')
    emdash=u'\u2014'
    titletext += ' {0} '.format(emdash)
    titletext += self.plotz[pidx].stoptime.strftime('%Y-%b-%-d %-H:%M:%S')
    self.ax.set_title(titletext,loc='left',fontsize='small')

    # <xTickShenanigans>
    # limit plot to only 5 ticks - need room for pv names
    self.ax.xaxis.set_major_locator(plt.MaxNLocator(5))
    # get xtick locations - this returns a numpy array
    tickSpots=self.ax.get_xticks().tolist()
    # try to silence a warning, skip first and last
    self.ax.xaxis.set_ticks(tickSpots[1:-1])
    xTickLabels=[]
    for val in tickSpots[1:-1]:
      if val.is_integer():
        if int(val)<len(self.plotz[pidx].pvList):
          if self.plotz[pidx].xLabelPart==2:
            # get the two middle chunks of pv name
            pvnParts=self.plotz[pidx].pvList[int(val)].split(':')[1:3]
            # rejoin them with a : if there's more than one
            pvn=':'.join(pvnParts)
          else:
            # use just the 2nd chunk (plotz.xLabelPart should be 1
            pvn=self.plotz[pidx].pvList[int(val)].split(':')[1]
          xTickLabels.append(pvn)
        else:
#          print('valstr {}'.format(val))
          xTickLabels.append('')
      else:
#        print('valstr {}'.format(val))
        xTickLabels.append('')
    # actually set the xticklabels now
    self.ax.set_xticklabels(xTickLabels)
    #</xTickShenanigans>

    # set y axis labels too
    self.ax.set_ylabel(self.plotz[pidx].yLabel)

    self.canvas.draw()
    self.ui.printPushButton.show()

    def onclick(event):
    # This function responds if user clicks somewhere on the upper plot
    #  and draws the archived data for that PV in the lower plot
#
#       print('%s click: button %d, x %d y %d xdata %f ydata %e' %
#             ('double' if event.dblclick else 'single', event.button,
#              event.x, event.y, event.xdata, event.ydata))
       self.ax2.clear()
       self.ax2.grid()
       # get index (x position) of click
       try:
         idx=round(event.xdata)
       except:
         idx=None

       # on the odd chance the click response is weird make sure 
       #  it's within the number of PVs we fetched
       if idx!=None and idx<len(self.plotz[pidx].pvList):
         # put pvname onto clipboard
         self.cb.setText(self.plotz[pidx].pvList[idx],mode=self.cb.Selection)

         # get the data to plot
         timi=self.plotz[pidx].archiveData[self.plotz[pidx].pvList[idx]]["times"]
         valus=self.plotz[pidx].archiveData[self.plotz[pidx].pvList[idx]]["values"]

         # yes we want to plot this vacuum data if there's more than 
         #  one positive value find number of positive points
         npos=len([x for x in valus if x>0])

         # if it's a vacuum plot without at least one
         #  positive point do nothing
         # otherwise plot as semilog (vacuum pidx<4) or normal
         if pidx<4 and npos<1:
           titlet='No positive values to plot on log scale'
           self.ax2.set_title(titlet,loc='left',y=.85,x=.02)
           dataPlotted=0
         elif pidx<4:
           self.ax2.semilogy(timi,valus,color='tab:blue')
           dataPlotted=1
         else:
           self.ax2.plot(timi,valus,color='tab:blue')
           dataPlotted=1

         # set x label as pv name
         xlabelt=self.plotz[pidx].pvList[idx]
         self.ax2.set_xlabel(xlabelt,fontsize='small')

         if dataPlotted:
           # This makes for pretty dates on the x-axis
           self.ax2.xaxis.set_major_formatter(
             mdates.ConciseDateFormatter(self.ax2.xaxis.get_major_locator()))

         # set y axis labels too
         self.ax2.set_ylabel(self.plotz[pidx].yLabel)

         self.canvas.draw()

    cid=self.canvas.mpl_connect('button_press_event',onclick)



  def ChangeTime(self):
#    print("changeTime")
    pass

  def ChangeSys(self):
  #
  # If we already have data for a given system, show it
  #
    pidx = self.ui.SysComboBox.currentIndex()
    if len(self.plotz[pidx].means)>0:
      self.plotz[pidx].getData=False
      self.Go()
      self.plotz[pidx].getData=True
    pass

  def ui_filename(self):
    return 'meanHist.ui'

  def ui_filepath(self):
    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

