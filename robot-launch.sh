#!/bin/bash

# Activate the EVA Text-To-Emotion (TTE) virtual environment
source /home/pi/EVA_ROBOT/eva-tte-module/venv/bin/activate

# Runs the TTE Module
python3 /home/pi/EVA_ROBOT/eva-tte-module/eva-tte.py &



# This command is necessary so that the robot's graphical interface (display) can be executed via the command line.
#export DISPLAY=:0.0

# Run the Web application that allows you to run and "kill" the EVA modules.
# The application can be accessed via the Raspberry IP, on port 5000.


#python3 /home/pi/EVA_ROBOT/robot-system-web-run.py

./robot-launch2.sh
