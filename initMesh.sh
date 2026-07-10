#!/bin/bash


# Start processes and store PIDs
python ServerClass.py &
PID1=$!
python InceptronClass.py &
PID2=$!

echo "Scripts running. Press [CTRL+C] to stop all."

# Trap the SIGINT (Ctrl+C) signal to kill both scripts on exit
trap "kill $PID1 $PID2 ; exit" SIGINT

# Keep the Bash script alive so the trap stays active
while true; do sleep 1; done
