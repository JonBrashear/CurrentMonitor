#!/bin/bash
#THe Plots are stored in ram, so we must recreate the filesystem at each reboot
mkdir /home/pi/WebServer/RPI1
mkdir /home/pi/WebServer/RPI1/FiveMinutePlots
mkdir /home/pi/WebServer/RPI1/HourLongPlots
mkdir /home/pi/WebServer/RPI1/DayLongPlots 
mkdir /home/pi/WebServer/RPI1/WeekLongPlots
#Each Pi holds only its plots, so I commented out the code for creating
#a directory for plots from a second pi
#mkdir /home/pi/WebServer/RPI2
#mkdir /home/pi/WebServer/RPI2/FiveMinutePlots
#mkdir /home/pi/WebServer/RPI2/HourLongPlots
#mkdir /home/pi/WebServer/RPI2/DayLongPlots 
#mkdir /home/pi/WebServer/RPI2/WeekLongPlots
#the hourly plots and five minute plots are created freqently. 
# The day Long and Week long plots are not, so their scripts are run to generate
#plots for their otherwise empty directories
python3 /home/pi/MonitorPi/Python/DayPlot.py
python3 /home/pi/MonitorPi/Python/WeekPlot.py
