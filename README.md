I don't know how to do the fancy markup.

This is a pydm GUI. The user chooses from a pulldown which group of signals
to fetch, then the time scale, then pushes Go! The programs fetches the 
archived data for all the PVs for that time range and calculates the means 
and stdevs of each. It then plots those as dots with error bars on a top
plot. If the user clicks a dot, the fetched data for that PV is shown
on the bottom plot and the PV name is put on the clipboard for pasting
into the archiver viewer etc.

Button to print to lcls2elog just saves the matplotlib figure as 
meanHist.ps then lpr -Pphysics-lcls2elog meanHist.ps

Window and plot will resize.

