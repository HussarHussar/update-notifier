# Debian Update Notifier
Update Notifier is a simple and easy-to-use application that uses chronjobs for scheduling package updates. It pipes a password stored in memory to sudo subprocesses and stores no passwords in any plain text files.

![screenshot](/assets/gui-screenshot.png)

## Requirements
PySide2, trio, sudo, and cron

``$ pip3 install PySide2 trio``

``$ apt install sudo cron``

## Debian Cron Addition
`` $ sudo ./CronInstall.sh [n]``

This is not a package installation it appends a cronjob to the anacrontab file using the update.py file in the current directory. It Sets the chronjob to run the update.py script at the current location every n days. The default is 30 if nothing is specified. Anacrontab also can be modified to run the update.py file if using a different distro. The update script can also be run manually.

## TODO
* Handle subprocess termination after cancel button is pressed
* Handle ctrl-c terminal press
* Handle Cancel and other errors
* Add chronjob install script
* Add icon
