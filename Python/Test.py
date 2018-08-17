#This script generates a log of current measurements. It is run in crontab and at reboot.
from piplates.DAQCplate import getADC
from time import sleep,time,gmtime
from calendar import timegm
from os import environ
#It is Possible to set the conversion parameters to the precise values for each hall channel by changing the values in these lists
Plate0SLOPE=[.2,.2,.2,.2,.2,.2,.2,.2]
Plate0OFFSET=[.48,.48,.48,.48,.48,.48,.48,.48]

Plate1SLOPE=[.2,.2]
Plate1OFFSET=[.48,.48]

# getCurrent uses getADC to measure all 10 ADC channels, and converts the voltages to a current.
#It is passed the time in seconds, as This is also recorded with the measured currents
#A string with a time and all 10 measurements is the return value
def getCurrent(Time):
        #the first column is the time meaurement
        String=str(round(Time,3))
        # the first 8 channels measured are on the bottom piplate, with adress 0        
        for i in range(0,8):
            V=getADC(0,i)
            I=round((V-Plate0OFFSET[i])/Plate0SLOPE[i],2)
            String+=","+str(I)
            # THe current measurements are added to the string
        for i in range(0,2):
            V=getADC(1,i)
            I=round((V-Plate1OFFSET[i])/Plate1SLOPE[i],2)
            String+=","+str(I)
            #Final two channels are on the top piplate, with adress 1
        String+="\n"
        #so output looks like Time,Hall1,Hall2,Hall3......
        return String
a=time()
I=getCurrent(a)
b=time()
print(I)
print(b-a)
