#!/bin/bash

Y=$(date -u +"%y")
M=$(date -u +"%-m")
if [[ $M -lt 4 ]]
then
	Conversion=$((3-M))
	M=$((12-Conversion))
	Y=$((Y-1))
else
	M=$((M-2))
	echo $M > M.txt
fi
if [[ $M -lt 10 ]]
then
	M="0"$M
fi
YM=$Y"-"$M
DirectoryName=$Y"--"$M
mkdir /home/pi/MonitorPi/Reports/$DirectoryName 2>/home/pi/error.txt
mv /home/pi/MonitorPi/Reports/Recent/Report*$YM* /home/pi/MonitorPi/Reports/$DirectoryName  2>/home/pi/error.txt
