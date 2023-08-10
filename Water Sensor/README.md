# Water Sensor Project

## Overview
This project is a solution for detecting water leaks. The system uses the umail repo for MicroPyton (https://github.com/shawwwn/uMail). When a leak is detected on the 
sensor board, a buzzer on the analog section of the board goes off along with an LED. The reading on the ADC pin of the Pico W will trigger an alert to be sent to the specified
email using SMTP. There is also a voltage divider connected to the ADC to read battery level if being powered with a battery, an alert is sent when battery is low.

## Files Overview
The Code folder contains the MicroPython firmware.

main.py : Reads ADC values to determine if there is a leak/low battery

umail.py : 3rd party library used to send email alert
