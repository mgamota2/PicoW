# Ticker Tape

## Overview

## File Purposes
- bits.py : Custom LED matrix driver for WS2812B LEDs arranged in 7x21 (rows, column) in serpentine rastar order (left to right, "snake").
- main.py : Runs the web server. Parses the list of user entered stocks and creates a stock object instance list and maintains/updates this list. Calls functions to print the stock data in the correct color (red/green).
- printChars.py : Defines helper functions for printing characters, uses the bits.py bitmap driver.
- stock_data.py : Creates a class which stores the stock name, current price, and percent change from previous close. 
- wifi_init.py : Helper function to initialize wifi connection and server on Pico W.