# DC Train Control
This project offers an LAN solution for DC model train control

## Overview
This project includes both hardware design and firmware for the Raspberry Pi Pico written in Micropython. The hardware is designed as a hub which can control the speed and
direction of the train as well as switch electrically switching tracks. The hub is controlled from a Raspberry Pi Pico hosted web server which has a dashboard for user 
inputs, allowing remote control of the train


## File Descriptions
**Files in the Full Control folder support track switching, speed, and direction while files in the Speed Control folder only support speed control.

index.html : This file contains the HTML, CSS, and JavaScript code to create, style, and add functionality to the slider and buttons.
main.py : This file initilizes a train object and parses requests from the server to evaluate user input and change speedm direction, or switching tracks accordingly
train_func.py : This file defines the trackPins and railPins classes which correspond to the switching tracks and train direction and speed, respectively
wifi_init.py : This file defines a helper function to connect the Pico W to a WiFi network and establish the server

### PCB
Since this project includes hardware design, the KiCAD project files are provided
