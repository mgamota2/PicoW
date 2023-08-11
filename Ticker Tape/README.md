# Ticker Tape

## Overview
This repo includes MicroPython code to create your own customizable stock ticker tape with a DIY LED matrix made from a WS2812B LED strip

## File Purposes
- bits.py : Custom LED matrix driver for WS2812B LEDs arranged in 7x21 (rows, column) in serpentine rastar order (left to right, "snake").
- main.py : Runs the web server. Parses the list of user entered stocks and creates a stock object instance list and maintains/updates this list. Calls functions to print the stock data in the correct color (red/green).
- printChars.py : Defines helper functions for printing characters, uses the bits.py bitmap driver.
- stock_data.py : Creates a class which stores the stock name, current price, and percent change from previous close. This data is gathered by calling the Finnhub.io API (https://finnhub.io/docs/api/introduction) You will need an API key, but the free version will work for this application. Put yours in line 15
- wifi_init.py : Helper function to initialize wifi connection and server on Pico W.

![image](https://github.com/mgamota2/PicoW/assets/97132068/879522c4-6bea-480d-b405-501fe0fa0f47)
