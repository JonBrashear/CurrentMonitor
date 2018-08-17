from numpy import loadtxt,concatenate,array
import matplotlib as mpl
mpl.use('agg')
from matplotlib.ticker import AutoMinorLocator
from time import gmtime,time
from calendar import timegm
import matplotlib.pyplot as plt
from glob import glob
TimesToFind=[]
TimeStruct=gmtime()
TimeList=list(TimeStruct)
FiveMinutesBefore=timegm(TimeStruct)-300
for i in range(0,4):
    if TimeList[i] <10:
        TimeList[i]="0"+str(TimeList[i])
Date=str(TimeList[0])+"-"+str(TimeList[1])+"-"+str(TimeList[2])+"--"+str(TimeList[3])
TimesToFind.append(Date)
if TimeStruct[4] < 5:
    HourBefore=timegm(TimeStruct)-3600
    TimeList=list(gmtime(HourBefore))
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
        t,CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10=loadtxt(e,delimiter=',',skiprows=3,usecols=(0,1,2,3,4,5,6,7,8,9,10),unpack=True)
        D=[CH1,CH2,CH3,CH4,CH5,CH6,CH7,CH8,CH9,CH10]
        Time=concatenate((Time,t))
        for i in range(0,10):
            Data[i]=concatenate((Data[i],D[i]))

    except IndexError:
        ""


EndTime=round(Time[-1],0)
StartTime=EndTime-300


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
T=FiveMinutesBefore
for a in range(0,6):
    TS=gmtime(T)
    TS=list(TS)
    for i in range(3,6):
        if TS[i] < 10:
            TS[i]="0"+str(TS[i])
        
        
    Tick=str(TS[3])+":"+str(TS[4])+":"+str(TS[5])
    Ticks.append(Tick)
    Locs.append(T)
    T+=60

L=AutoMinorLocator(4)
for i in range(0,10):
    plt.figure(figsize=(8,6))
    a=plt.plot(Time,Data[i],'ro',markersize=.25)
    plt.axes().yaxis.set_minor_locator(L)
    plt.grid(1)
    plt.xlabel('Time')
    plt.ylabel("Current (A)")
    plt.ylim([9,18])
    plt.xlim([(FiveMinutesBefore),(T-60)])
    plt.xticks(Locs,Ticks)
    string="Graph of Current vs Time for CH "+str(i+1)
    plt.title(string)
    name="WebServer/RPI1/FiveMinutePlots/CH"+str(i+1)+".png"
    plt.savefig(name)
    plt.cla()







