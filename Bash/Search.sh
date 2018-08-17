#!/bin/bash
#This script is run by the search function defined in the .bashrc file
#  It will find a report coresponding to a specific date, or a a list of reports cponvering a period of time
# It has multiple usage options:
# -h stream usage info to screen
# -s specify start Date
#  -e specify end date
#  -a expand search to include files in archive
#  -f send results to file rather than a screen( do this for a list of files)

# THe function below is used to print the usage information
function Usage {
	printf "usage: search options\n"
	printf "This function finds the name of a report created at a certain time. It can also return a list of all reports\n"
       	printf "created between two dates.\n\n"

	printf "Options:\n"
	printf "1. -h   	Display usage information\n\n"
	printf "2. -s		Start Date: e.g. search -s 2018/07/29/00\n"
	printf "		Default is current date\n\n"
	printf "3. -e		End Date: e.g. search -s 2018/07/29/00 -e 2018/08/02/12\n"
       	printf "		Default is current Date\n\n"
	printf "4. -a 		Extend search to File Archives. Include flag if a date is more than two months in the past\n\n"

	printf "5. -f  		Stream input to file: e.g. search -s 2018/07/29/00 -e 2018/08/02/12  -f /home/pi/Output.txt\n"
	printf "		Give the absolute adress\n\n"
	printf "6. -v		Increase output verbosity\n\n"
}



# THis function does basic checking of the dates passed to the function
function check {
	error=true 
 	Date=$1 # Date is passed as input
	while [ $error == true ]; do
	

		if [[ ${Date:6:1} == "/" ]]
		then
			echo  ""
			echo "If the Date, Month or Hour is less than 10, make sure to include a leading 0(e.g, 05, not 5)"
			echo "Re-enter Date"
			echo ""
			read Date
			elif [[ ${Date:9:1} == "/" ]]
		then
			echo ""
			echo "If the Date, Month or Hour is less than 10, make sure to include a leading 0(e.g, 05, not 5)"
			echo "Re-enter Date"
			echo ""
			read Date
		elif [[ ${Date:(-2):1} == "/" ]]
		then
			echo ""
			echo "If the Date, Month or Hour is less than 10, make sure to include a leading 0(e.g, 05, not 5)"
			echo "Re-enter Date"
			echo ""
			read Date
		elif  [[ ${#Date} -ne 13 ]]
		then 
			echo ""
			echo "Please use the format specified by the usage information"
			echo "Re-enter Date"
			echo ""
			read Date
		else 
			error=false
		fi
	done
	retval=$Date
}


#Now, Parse options



while getopts "hs:e:af:v" OPTION
do
	case $OPTION in
		h)
			Usage
			exit 1
			;;
		s)
			Start=$OPTARG
			;;
		e)

	
			End=$OPTARG
			;;
		a)
			Archives=1
			;;
		
		f)   
			FileName=$OPTARG
			;;
		v)
			Verbosity="yes"
			;;

		[?])	Usage
			exit 1
			;;
	esac
done   	
# Now we must check the dates give for errors. If no dates were passed, then this step is skipped
if [[ $Verbosity ]]	
then
	echo "Checking Start Date: "
	if [[ $Start ]]
	then 
		check $Start
		Start=$retval
		Start=${Start:0:4}"-"${Start:5:2}"-"${Start:8:2}"--"${Start:11}
	fi
	echo  "Start Date Good"
	echo ""

	echo "Checking End Date: "
	if [[ $End ]]
	then
		if [[ $End != "Start" && $End != "start" ]]
		then

			check $End
			End=$retval
			End=${End:0:4}"-"${End:5:2}"-"${End:8:2}"--"${End:11}
		
		else
			End=$Start
		fi
	fi
	echo  "End Date Good"
	echo ""
else 
	if [[ $Start ]]
	then 
		check $Start
		Start=$retval
		Start=${Start:0:4}"-"${Start:5:2}"-"${Start:8:2}"--"${Start:11}
	fi
	
	if [[ $End ]]
	then
		if [[ $End != "Start" && $End != "start" ]]
		then

			check $End
			End=$retval
			End=${End:0:4}"-"${End:5:2}"-"${End:8:2}"--"${End:11}
		
		else
			End=$Start
		fi
	fi
fi



# Now we must account for the -a flag

# if the -a flag is passed, we want to search the archive directory as well as the Recent directory
# THe conditional block provides a directory adress that the find command will use


if [[ $Archives  ]]
then
	# if -a flag was passed, do not specify the directory incide of the reports diretory
	# the * operator tells find to search all directories in  Reports
	ext="/home/pi/MonitorPi/Reports/"*"/"
else	
       
	#if the flag was not passed, the extension specifies the Recent directory. 
	# This feature saves time if the times passed to search are from the last two months
	ext="/home/pi/MonitorPi/Reports/Recent/"
	
fi

#Next, find Boundary Reports
if [[ $Start ]] 
then

	F0=$(find $ext*$Start* 2>/dev/null -print | head -n1 2>/dev/null)
else
	read RN < /home/pi/MonitorPi/counter.txt
	RN=$((RN-1))
	F0=$(find $ext"Report"$RN"--"*  2>/dev/null)
fi

if [[ $End && $Start ]]
then
	FEnd=$(find $ext*$End* 2>/dev/null -print | tail -n1 2>/dev/null)
else
	read RN < /home/pi/MonitorPi/counter.txt
	RN=$((RN-1))
	FEnd=$(find $ext"Report"$RN"--"* 2>/dev/null)

fi


#Now, find the Report Numbers of these two reports
if [[ $F0 ]]
then
	N0=${F0:40}
	N0=${N0:0:(-22)}

else
	echo "No reports were created at the given start time"
	exit 1
fi


if [[ $FEnd ]]
then
	NEnd=${FEnd:40}
	NEnd=${NEnd:0:(-22)}

else
	echo "No reports were created at the given end time"
	exit 1 
fi

if [[ $NEnd -lt $N0 ]]
then 
	echo "InputError: Start time comes after end time"
	exit 1
fi

# Now, Find the actual Files!

if [[ $FileName ]]
then
	#THis conditional tests whether the -f flag was passed
	#If so, Filenames are written to the specified file
	while [[ $N0 -le $NEnd ]]; do
		find  $ext"Report"$N0"--"*  >> $FileName  2>/dev/null
		let N0=N0+1
	done
else 	
	if [[ $Verbosity ]]
	then

		echo "The Reports created in the specified time interval are shown below"
	fi
	while [[ $N0 -le $NEnd ]]; do
		find  $ext"Report"$N0"--"* 2>/dev/null
		let N0=N0+1
	done
fi


