from numpy import loadtxt, concatenate, array
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from time import gmtime,time
from calendar import timegm
from glob import glob
from pandas import read_csv
from pandas.errors import EmptyDataError


TimeStruct=gmtime()
DayBefore=timegm(TimeStruct)-86400
TimeStruct=gmtime(DayBefore)
TimeCounter=DayBefore
Reports=[]
for n in range(0,2):
    TimeList=list(gmtime(TimeCounter))
    for i in range(0,4):
        if TimeList[i] <10:
            TimeList[i]="0"+str(TimeList[i])
    Date=str(TimeList[0])+"-"+str(TimeList[1])+"-"+str(TimeList[2])+"--"
    Name="/home/pi/MonitorPi/Reports/Recent/*"+Date+"*"
    Reports=Reports+glob(Name)
    TimeCounter+=86400

Time=array([])
Data=[]
for i in range(10):
    Data.append(array([]))

t1=time()
for e in Reports:
    try:
        df=read_csv(e,header=None,delimiter=',',names=["t",'CH1','CH2',"CH3",'CH4','CH5','CH6','CH7','CH8','CH9','CH10'],skiprows=3)
        D=[df.CH1.values,df.CH2.values,df.CH3.values,df.CH4.values,df.CH5.values,df.CH6.values,df.CH7.values,df.CH8.values,df.CH9.values,df.CH10.values]
        Time=concatenate((Time,df.t.values))
        for i in range(0,10):
            Data[i]=concatenate((Data[i],D[i]))
    except EmptyDataError:
        ""
t2=time()
Ticks=[]
Locs=[]
T=DayBefore

for a in range(0,25):
    TS=gmtime(T)
    TS=list(TS)
    for i in range(1,5):
        if TS[i] < 10:
            TS[i]="0"+str(TS[i])
    
        
    Tick=str(TS[1])+"/"+str(TS[2])+" "+str(TS[3])+":"+str(TS[4])
    Ticks.append(Tick)
    Locs.append(T)
    T+=3600


# Now Generate plots


L=AutoMinorLocator(4)
for i in range(0,10):
    plt.figure(figsize=(15,8))
    a=plt.plot(Time,Data[i],'ro',markersize=.01,markevery=2)
    plt.axes().yaxis.set_minor_locator(L)
    plt.grid(1)
    plt.xlabel('Time')
    plt.ylabel("Current (A)")
    plt.xticks(Locs,Ticks,rotation=30,size='small')
    plt.ylim([9,18])
    plt.xlim([DayBefore,(T-3600)])
    string="Graph of Current vs Time for CH "+str(i+1)
    plt.title(string)
    name="WebServer/RPI1/DayLongPlots/CH"+str(i+1)+".png"
    
    plt.savefig(name)
    plt.cla()


print(t2-t1)

