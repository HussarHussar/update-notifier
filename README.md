# Debian Update Notifier
Update Notifier is a simple and easy-to-use application that uses chronjobs for scheduling package updates. It takes a password and runs ``sudo apt update`` in a subprocess. It stores no passwords in any files.

// [Insert picture of notification popup]

## Usage
`` ./setup.py 15``

Sets the chronjob to run the update.py script at the current location every 15 days. Setup expects an integer representing the update interval.
