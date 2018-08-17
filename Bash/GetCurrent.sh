#!/bin/bash
#This Script will read the last measurements and stream them to the screen

#First, we must find the most recent Report
#Read in counter
read n < /home/pi/MonitorPi/counter.txt
let n=n-1
#Use it to find FileName
Name=$(find "/home/pi/MonitorPi/Reports/Recent/Report"$n-""*)
LastLine=$(tail -n1 $Name)
IFS=','
read -ra Array <<< $LastLine
if [[ $1 ]]

then
	if [[ $1 -lt 1 || $1 -gt 10 ]]
	then 
		echo "Invalid Channel Number"
	else

		string="CH"$1" = "${Array[$1]}" A"
		echo $string 
	fi
else

	i=1
	string='| '
	while [[ $i -le 10 ]]; do
		string=$string"CH"$i" = "${Array[i]}" A | "
		let i=i+1
	done
	echo $string
fi	


