import argparse
import matplotlib.pyplot as plt
from time import gmtime,time
from matplotlib.ticker import AutoMinorLocator
from calendar import timegm
from numpy import array,concatenate
from pandas import read_csv
from pandas.errors import EmptyDataError
from glob import glob
#Use argparse library to handle date inputs
parser=argparse.ArgumentParser(prog='plot',description="Generates plots of all measurements taken between provided date")
parser.add_argument("-s",'--start',required=False,help="Start Date. Default is current time.")
parser.add_argument("-e",'--end',required=False,help="End Date. Default is current time.")
parser.add_argument("-a",required=False,help='Extend search to archived reports.',action='store_true') 
parser.add_argument("-c",'--channel',required=False,help='Specify ADC channels to plot, default is all 10.')
parser.add_argument("-f","--path",required=False,help="Path name of directory where the plots should be placed. default is in /home/pi/MonitorPi/Plots/UserPlots")
args=parser.parse_args()
#Now check date inputs for errors

def check(Date,SE):
    error=True
    Message="There is an error in the "+SE+" date!\nUse the format specified in the usage information."
    ReEnter="Re-enter the "+SE+" date: "
    while error:
        #Check the string has the right length
        if len(Date) != 13:
            print(Message)
            Date=str(input(ReEnter))
        #Make sure slashes are in the raight place
        #This catches simple typos
        elif Date[4:5] != "/" and Date[4:5] != "-":
            print(Message)
            Date=str(input(ReEnter))
        elif Date[7:8] != "/" and Date[7:8] != "-":
            print(Message)
            Date=str(input(ReEnter))
        elif Date[10:11] != "/" and Date[10:11] != "-":
            print(Message)
            Date=str(input(ReEnter))
        else:
            #Now check that the 4 parts of the date are numbers
            try:
                Y=int(Date[0:4]);M=int(Date[5:7]);D=int(Date[8:10]);H=int(Date[11:])
                Date=(Y,M,D,H,0,0)
                break
            except ValueError:
                print(Message)
                print("0!")
                Date=str(input(ReEnter))
    return Date

if args.start != None:
    Start=check(args.start,"start")
else:
    Start=gmtime()

if args.end != None:
    if args.end != "S" and args.end != "Start":
        End=check(args.end,"end")
    else:
        End=Start
else:
    End=gmtime()


#Now check Channel Choices:
if args.channel != None:
    CH=args.channel
    while True:
        CH=CH.split(',')
        #remove duplicates, maybe take this out later
        CH=list(set(CH))  
        #We check that all entries are integers between 1-10
        try:
            for i in range(len(CH)):
                CH[i]=int(CH[i])
                if CH[i] not in [1,2,3,4,5,6,7,8,9,10]:
                    raise KeyboardInterrupt
            break
        except ValueError:
            print('Error in the entered channels')
            CH=str(input("Re-enter the channel string: "))
        except KeyboardInterrupt:
            print('One or more entered channels was an invalid channel number')
            CH=str(input("Re-enter the channel string: "))
#if no channel string given, all channels will be plotted
else:
    CH=[1,2,3,4,5,6,7,8,9,10]

#Now find files:
#To save time, we will check the date of each day in between the start and end dates 
#and figure out wht directory to look in.
#First, find the current date 
Date=gmtime()
Y=str(Date[0])
if Date[1] < 10:
    M="0"+str(Date[1])
else:
    M=str(Date[1])
Month=Y+"-"+M
#Next, find last Month:
M=int(M)-1
if M <1:
    M="12"
    Y=str((Y-1))
else:
    if M < 10:
        M="0"+str(M)
    else:
        M=str(M)
LastMonth=Y+"-"+M
#If a date falls in these two months, we search the Recent directory


Start=list(Start[0:4]+(0,0))
End=list(End[0:4]+(0,0))
StartSeconds=timegm(Start)
EndSeconds=timegm(End)
for i in range(1,4):
    if Start[i] < 10:
        Start[i]="0"+str(Start[i])
for i in range(1,4):
    if End[i] < 10:
        End[i]="0"+str(End[i])

Date=str(Start[0])+"-"+str(Start[1])+"-"+str(Start[2])
#If the start and end times are on the same date, we only need to use glob once
if Date == str(End[0])+"-"+str(End[1])+"-"+str(End[2]):
    print(0)
        # if in last two months, reports are in Recent/
    if Date[0:7] == Month or Date[0:7] == LastMonth:
        Dir="Recent/"
    #Otherwise, they are in an archived directory
    else:
        Dir=Date[2:5]+"-"+Date[5:7]+"/"

    ReportName="/home/pi/MonitorPi/Reports/"+Dir+"*"+Date+"*"
    List=glob(ReportName)
    ToLoad=[]
    StartHour=int(Start[3])
    EndHour=int(End[3])
    for e in List:
        if int(e[-8:-6]) >= StartHour and int(e[-8:-6]) <= EndHour:
            ToLoad.append(e)
#otherwise, we find relevant reports on start date, end date, and all the reports on days in between
else:
    print(1) 
    # if in last two months, reports are in Recent/
    if Date[0:7] == Month or Date[0:7] == LastMonth:
         Dir="Recent/"
    #Otherwise, they are in an archived directory
    else:
        Dir=Date[2:5]+"-"+Date[5:7]+"/"

    ReportName="/home/pi/MonitorPi/Reports/"+Dir+"*"+Date+"*"
    List=glob(ReportName)
    ToLoad=[]
    Hour=int(Start[3])
    for e in List:
        if int(e[-8:-6]) >= Hour:
            ToLoad.append(e)
    Times=StartSeconds
    Times+= 86400
    #Now, We loop through the rest of the Dates. We must also only load reports up to the end hour
    #so we stop before we reach the end date
    EndLoopTime=timegm([int(End[0]),int(End[1]),int(End[2]),0,0,0])
    while Times < EndLoopTime:
        TimeList=list(gmtime(Times))
        for i in range(1,4):
            if TimeList[i] < 10:
                TimeList[i]="0"+str(TimeList[i])
        Date=str(TimeList[0])+"-"+str(TimeList[1])+"-"+str(TimeList[2])
        # if in last two months, reports are in Recent/
        if Date[0:7] == Month or Date[0:7] == LastMonth:
            Dir="Recent/"
        #Otherwise, they are in an archived directory
        else:
            Dir=Date[2:5]+"-"+Date[5:7]+"/"

        ReportName="/home/pi/MonitorPi/Reports/"+Dir+"*"+Date+"*"
        ToLoad+=glob(ReportName)
        Times+=86400


    Date=str(End[0])+"-"+str(End[1])+"-"+str(End[2])
    # if in last two months, reports are in Recent/
    if Date[0:7] == Month or Date[0:7] == LastMonth:
        Dir="Recent/"
    #Otherwise, they are in an archived directory
    else:
        Dir=Date[2:5]+"-"+Date[5:7]+"/"

    ReportName="/home/pi/MonitorPi/Reports/"+Dir+"*"+Date+"*"
    List=glob(ReportName)
    Hour=int(End[3])
    for e in List:
        if int(e[-8:-6]) <= Hour:
            ToLoad.append(e)

Time=array([])
Data=[]
for i in range(10):
    Data.append(array([]))
for e in ToLoad:
    try:
        df=read_csv(e,header=None,delimiter=',',names=["t",'CH1','CH2',"CH3",'CH4','CH5','CH6','CH7','CH8','CH9','CH10'],skiprows=3)
        D=[df.CH1.values,df.CH2.values,df.CH3.values,df.CH4.values,df.CH5.values,df.CH6.values,df.CH7.values,df.CH8.values,df.CH9.values,df.CH10.values]
        Time=concatenate((Time,df.t.values))
        for i in range(0,10):
            Data[i]=concatenate((Data[i],D[i]))
    except EmptyDataError:
        ""
DeltaT=timegm([int(End[0]),int(End[1]),int(End[2]),0,0,0])+3600-StartSeconds
#Settings
#MarkEvery --
MarkEvery=[1,5,10,17]
#TickSettings
DT=[600,1800,3600,43200,86400,302400,"ByMonth"]
if DeltaT <= 7200: 
    DT=600
elif DeltaT <= 21600:
    DT=1800
elif DeltaT <= 86400:
    DT=3600
elif DeltaT <= 172800:
    DT=7200


# Now Generate plots
L=AutoMinorLocator(4)
for i in CH:
    plt.figure(figsize=(15,8))
    a=plt.plot(Time,Data[(i-1)],'bo',markersize=.01,markevery=5)
    plt.axes().yaxis.set_minor_locator(L)
    plt.grid(True)
    plt.xlabel('Time')
    plt.ylabel("Current (A)")
    #plt.xticks(Locs,Ticks,rotation=30,size='small')
    plt.ylim([9,18])
    #plt.xlim([WeekBefore,(T-43200)])
    string="Graph of Current vs Time for CH "+str(i)
    plt.title(string)
    name="/home/pi/CH"+str(i)+".png"
    
    plt.savefig(name)
    plt.cla()

