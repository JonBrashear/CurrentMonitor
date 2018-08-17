#!/bin/bash

tr </home/pi/MonitorPi/counter.txt -d '\000' > /home/pi/MonitorPi/mcounter.txt
mv /home/pi/MonitorPi/mcounter.txt /home/pi/MonitorPi/counter.txt

read n < /home/pi/MonitorPi/counter.txt
n=$((n-1))
cd /home/pi/MonitorPi/Reports/Recent
LastReport=$(find "Report"$n"--"*)
echo $LastReport

tr </home/pi/MonitorPi/Reports/Recent/$LastReport -d '\000' > /home/pi/MonitorPi/Reports/Recent/"m"$LastReport
mv /home/pi/MonitorPi/Reports/Recent/"m"$LastReport /home/pi/MonitorPi/Reports/Recent/$LastReport


