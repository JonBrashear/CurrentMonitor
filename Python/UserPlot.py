import argparse
#import matplotlib.pyplot as plot
from time import gmtime,time
from matplotlib.ticker import AutoMinorLocator
from calendar import timegm
from numpy import array,concatenate
from pandas import read_csv
from pandas.errors import EmptyDataError
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

#Now, we use glob to find FileNames to plot
Start=Start[0:4]+(0,0)
End=End[0:4]+(0,0)
StartSeconds=timegm(Start)
EndSeconds=timegm(End)
ToLoad=[]
for i in range(1,4):
    if Start[i] < 10:
        Start[i]="0"+str(Start[i])
Date=str(Start[0])+"-"+str(Start[1])+"-"+str(Start[2])+"-"+str(Start[3])
ReportName="/home/pi/MonitorPi/

ToFind=StartSeconds+3600


    





