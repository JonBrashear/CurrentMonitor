from numpy import concatenate, array
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from time import gmtime,time
from calendar import timegm
from glob import glob
from pandas import read_csv
from pandas.errors import EmptyDataError
TimesToFind=[]
TimeStruct=gmtime()
TimeList=list(TimeStruct)


for i in range(0,4):
    if TimeList[i] <10:
        TimeList[i]="0"+str(TimeList[i])
Date=str(TimeList[0])+"-"+str(TimeList[1])+"-"+str(TimeList[2])+"--"+str(TimeList[3])
TimesToFind.append(Date)
HourBefore=timegm(TimeStruct)-3600
TimeStruct=gmtime(HourBefore)
TimeList=list(TimeStruct)
for i in range(0,4):
    if TimeList[i] <10:
        TimeList[i]="0"+str(TimeList[i])


Date=str(TimeList[0])+"-"+str(TimeList[1])+"-"+str(TimeList[2])+"--"+str(TimeList[3])
TimesToFind.append(Date)


Time=array([])
Data=[]
for i in range(10):
    Data.append(array([]))
Reports=[]
for e in TimesToFind:
    Name="/home/pi/MonitorPi/Reports/Recent/*"+e+"*"
    Reports=Reports+glob(Name)


for e in Reports:
    try:
        df=read_csv(e,header=None,delimiter=',',names=["t",'CH1','CH2',"CH3",'CH4','CH5','CH6','CH7','CH8','CH9','CH10'],skiprows=3)
        D=[df.CH1.values,df.CH2.values,df.CH3.values,df.CH4.values,df.CH5.values,df.CH6.values,df.CH7.values,df.CH8.values,df.CH9.values,df.CH10.values]
        Time=concatenate((Time,df.t.values))
        for i in range(0,10):
            Data[i]=concatenate((Data[i],D[i]))
    except EmptyDataError:
        ""
StartTime=HourBefore
def FindIndices(Time):
    i=-1
    while True: 
        try:
            if round(Time[i],0) >= StartTime:
                i-=1
            else:
                i+=1
                break
        except IndexError:
                i=0
                break   
    return i

Ticks=[]
Locs=[]
T=HourBefore
for a in range(0,7):
    TS=gmtime(T)
    TS=list(TS)
    if TS[4] < 10:
        TS[4]="0"+str(TS[4])
        
        
    Tick=str(TS[3])+":"+str(TS[4])
    Ticks.append(Tick)
    Locs.append(T)
    T+=600


# Now Generate plots
L=AutoMinorLocator(4)
for i in range(0,10):

    plt.figure(figsize=(8,6))
    a=plt.plot(Time,Data[i],'ro',markersize=.25)
    plt.axes().yaxis.set_minor_locator(L)
    plt.grid(1)
    plt.xlabel('Time')
    plt.ylabel("Current (A)")
    plt.xticks(Locs,Ticks)
    plt.ylim([9,18])
    plt.xlim([HourBefore,(T-600)])
    string="Graph of Current vs Time for CH "+str(i+1)
    plt.title(string)
    name="WebServer/RPI1/HourLongPlots/CH"+str(i+1)+".png"
    plt.savefig(name)
    plt.cla()







