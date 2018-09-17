#This script generates a log of current measurements. It is run in crontab and at reboot.
from piplates.DAQCplate import getADC
from time import sleep,time,gmtime
from calendar import timegm
from os import environ
#It is Possible to set the conversion parameters to the precise values for each hall channel by changing the values in these lists
Plate0SLOPE=[5.4002,5.2515,5.3952,5.3425,5.334,5.3954,5.4191,5.4001]
Plate0OFFSET=[-2.6358,-2.5612,-2.6089,-2.5983,-2.5946,-2.5876,-2.6230,-2.6061]

Plate1SLOPE=[5.3791,5.3377]
Plate1OFFSET=[-2.6131,-2.6379]

# getCurrent uses getADC to measure all 10 ADC channels, and converts the voltages to a current.
#It is passed the time in seconds, as This is also recorded with the measured currents
#A string with a time and all 10 measurements is the return value
def getCurrent(Time):
        #the first column is the time meaurement
        String=str(round(Time,3))
        # the first 8 channels measured are on the bottom piplate, with adress 0        
        for i in range(0,8):
            V=getADC(0,i)
            I=round((V*Plate0SLOPE[i]+Plate0OFFSET[i]),2)
            String+=","+str(I)
            # THe current measurements are added to the string
        for i in range(0,2):
            V=getADC(1,i)
            I=round((V*Plate1SLOPE[i]+Plate1OFFSET[i]),2)
            String+=","+str(I)
            #Final two channels are on the top piplate, with adress 1
        String+="\n"
        #so output looks like Time,Hall1,Hall2,Hall3......
        return String


#The reports are assigned a number, and a timestamp. The number is kept in a counter file (counter.txt)
#The counter is incremented for each report that is created.
# It is read in and updated below
with open("/home/pi/MonitorPi/counter.txt",'r+') as f:
    n=int(f.read())
    N=n+1 #Updated counter
    f.seek(0)
    f.write(str(N)+"\n")
#A timestamp is alos assigned to the file name. this makes it easy to search for a certain date



Date=gmtime() #gmtime contains a tuple containing information about the system time eg. (year, month, day, hour, minute, second)

# We want the report to end at the turn of the hour
#The timegm function is the invers of gmtime. It converts time tuples to a time in seconds since the epoch
# the first 4 elements of the Date tuple are passed to timegm
#timegm will then output a time in seconds corresponding to the begining of the hour the report was made
#Adding 3600 to this gives the time at which the report should end
EndTime=timegm((Date[0],Date[1],Date[2],Date[3],0,0))+3600

# The Date must then be formatted properly. the tuple returned by gmtime has integer elements
# if these were used, the date could look like 2018-7-9--0:0:1
# The code below replaces the integer elements in the tuple that are less than 10 with a string of the form 0#
# that way the date would look like 2018-07-09--00:00:01
Date=list(Date)
for i in range(1,6):
    if Date[i]<10:
        Date[i]="0"+str(Date[i])

#Start Date
Date=str(Date[0])+"-"+str(Date[1])+"-"+str(Date[2])+"--"+str(Date[3])+":"+str(Date[4])+":"+str(Date[5])
#File Name: combines counter and start date
Name="/home/pi/MonitorPi/Reports/Recent/Report"+str(n)+"--"+Date

#Now create the file
with open(Name,'w+') as f:
    f.write("Current Measurements for "+Date+"\n")
    f.write("Time is measured since 00:00:00 01/01/1970, Current is measured in Amperes\n")
    f.write("||Time(s)||HALL1||HALL2||HALL3||HALL4||HALL5||HALL6||HALL7||HALL8||HALL9||HALL10||\n")
    f.flush()
    # THe measurement frequency can be specified as an environment variable called FREQ.
    # it is read in below
    FREQUENCY=int(environ["FREQ"])
    SleepTime=1/FREQUENCY
    Time=time()
    # in the loop below, get current is used to take measurements
    #The loop is exited when the Time surpasses the EndTime (At the turn of the hour)
    while Time < EndTime:
        
        String=getCurrent(Time)
        f.write(String)
        f.flush()
        # getCurrent takes ~ .009 seconds to execute, so this is subtracted from the time taken between measurements
        sleep((SleepTime-.009))
        Time=time()






