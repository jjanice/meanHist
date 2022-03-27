# 
# plotVacs
# J. Nelson
# 26 March 2022
#
# pydm class to go with plotVacs.ui
#
# This loads up the time frame combo boxes on the ui then
# when Go! is pushed, it reads out the box and
# figures out the tab then makes a plot
#

import time
from os import path, system
from pydm import Display
import datetime
import plotVacsUtil as util
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from functools import partial

class MyDisplay(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(MyDisplay, self).__init__(parent=parent, args=args, macros=macros)

# Get variables from utility file
    self.tranges = util.timeranges()
    self.tdays = util.timedays()
    self.vacsyses = util.vacsyses()

# initialize matplotlib click connections
    self.ax=0
    self.ax2=0

# connect spinner boxes to functions
    self.ui.TimeComboBox.activated.connect(self.ChangeTime)
    self.ui.SysComboBox.activated.connect(self.ChangeSys)
#Fill in ui components
    self.ui.progressBar.setValue(0)
# vacuum system selector
    for vacsys in self.vacsyses:
      self.ui.SysComboBox.addItem(vacsys)

# time range selector
    for trange in self.tranges:
      self.ui.TimeComboBox.addItem(trange)

# put a plot in the gridlayout
    self.figure=Figure()
    self.canvas=FigureCanvas(self.figure)
    self.ui.PlotArea.addWidget(self.canvas)

# Connect go button to function
    self.ui.GoButton.clicked.connect(self.Go)

# empty the status text area
    self.ui.StatusLabel.setText("")

  def Go(self):
    if type(self.ax)!=int:
      self.figure.delaxes(self.ax)
      self.canvas.draw()
    if type(self.ax2)!=int:
      self.figure.delaxes(self.ax2)
      self.canvas.draw()
    self.ax=self.figure.add_subplot(2,1,1)
#    print(type(self.ax))
    self.ax2=self.figure.add_subplot(2,1,2)
    self.ax.clear()
    tidx = self.ui.TimeComboBox.currentIndex()
#    print(self.tranges[tidx])
    stoptime=datetime.datetime.now()
    starttime=stoptime-datetime.timedelta(days=self.tdays[tidx])

    vidx = self.ui.SysComboBox.currentIndex()
#    print(self.vacsyses[vidx])
    means, stds, pvl, archiveData=util.getData(self.ui.StatusLabel,
                              self.ui.progressBar,vidx,starttime,stoptime)
    self.ax.errorbar(range(len(means)),means,yerr=stds,
                ls='none',ecolor='black',elinewidth=0.5)
    self.ax.semilogy(means,'bo')
    self.ax.grid()
    self.canvas.draw()
    def onclick(event):
#       print('%s click: button %d, x %d y %d xdata %f ydata %e' %
#             ('double' if event.dblclick else 'single', event.button,
#              event.x, event.y, event.xdata, event.ydata))
       self.ax2.clear()
       self.ax2.grid()
       idx=round(event.xdata)
       if idx<len(pvl):
         timi=archiveData[pvl[idx]]["times"]
         valus=archiveData[pvl[idx]]["values"]
         if len([x for x in valus if x>=0])>1:
           titlet=pvl[idx]
           self.ax2.semilogy(timi,valus)
           self.ax2.set_title(titlet,loc='left',y=.85,x=.02,fontsize='small')
           self.ax2.xaxis.set_major_formatter(
             mdates.ConciseDateFormatter(self.ax2.xaxis.get_major_locator()))
           self.canvas.draw()

    cid=self.canvas.mpl_connect('button_press_event',onclick)



  def ChangeTime(self):
#    print("changeTime")
    pass

  def ChangeSys(self):
#    print("changeSys")
    pass

  def ui_filename(self):
    return 'plotVacs.ui'

  def ui_filepath(self):
    return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

#  def getData(vidx,starttime,stoptime):
    
