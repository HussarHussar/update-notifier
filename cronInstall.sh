#!/bin/bash

distResult=$(grep "PRETTY_NAME=" < /etc/*-release)
echo "$distResult"
updateInterval="$1"
updatePath="$(pwd)/update.py"

if [ -z "$updateInterval" ]; then
	updateInterval=30
	echo $updateInterval
fi
#Check that the running distro is debian and update.py exists
if [[ "$distResult" != *"Debian"* ]]; then
	echo 'Identified distribution is not debian. Quiting...'
	exit 1
fi

if [ ! -f "$updatePath" ]; then
	echo 'update.py not found. Quitting...'
	exit 1
fi

#Check if there is too many arguments
if [ "$#" -gt "1" ]; then
	echo "Too many arguments. There are $#."
	exit 1
fi

retes='^[0-9]+$'
if ! [[ $updateInterval =~ $retes ]]; then 
	echo 'interval has non int value. Quiting.'
	exit 1
fi

echo 'Starting'

#inTime = '17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly'
insert="$updateInterval 	5 	pkg.updates 	$updatePath"
currentLine=$(cat /etc/anacrontab | grep 'pkg.updates')

if [ "$currentLine" = "" ]; then
	echo "$insert" >> /etc/anacrontab
else
	sed -i "/pkg.updates/ c\\$insert" /etc/anacrontab
fi
