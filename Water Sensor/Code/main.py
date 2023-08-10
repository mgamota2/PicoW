from machine import ADC, Pin
import network
import time
import urequests
from secrets import *

import umail

# Internal libs


water = ADC(Pin(26))     # create ADC object on ADC pin
battery = ADC(Pin(27))

led_g=machine.Pin(3, machine.Pin.OUT)
led_y = machine.Pin(2, machine.Pin.OUT)

if battery.read_u16()<1300:
    led_g.value(0)
    led_y.value(1)
else:
    led_g.value(1)
    led_y.value(0)
    
BATTERY_CHECK=True

rtc = machine.RTC()
rtc.datetime((2023, 7, 23, 0, 11, 14, 36, 0))
day = (rtc.datetime()[2])

def connect_to_internet(ssid, password):
    # Pass in string arguments for ssid and password
    
    # Just making our internet connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connect or fail
    max_wait = 100
    while max_wait > 0:
      if wlan.status() < 0 or wlan.status() >= 3:
        break
      max_wait -= 1
      print('waiting for connection...')
      time.sleep(1)
    # Handle connection error
    if wlan.status() != 3:
       print(wlan.status())
       raise RuntimeError('network connection failed')
    else:
      print('connected')
      print(wlan.status())
      status = wlan.ifconfig()
    



def send_email(x):
    sender_email = 'scraperw50@gmail.com'
    sender_name = 'Water Heater'
    sender_app_password = ''
    recipient_email = 'mggamota@gmail.com'
    
    if x == 0:
        content='Battery is low, please replace'
    if x == 1:
        content= '******** ALERT: THERE IS A LEAK ********'
    connect_to_internet(wifi_ssid, wifi_pw)

    
    # Send the email
    # Connect to the Gmail's SSL port
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Login to the email account using the app password
    smtp.login(sender_email, sender_app_password)
    # Specify the recipient email address
    smtp.to(recipient_email)
    # Write the email header
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + content + "\n")
    smtp.write(" ")
    # Send the email
    smtp.send()
    # Quit the email session
    smtp.quit()
    print('Email Sent')
    
        
while True:
      
    
    water_res = water.read_u16()
    print(water_res)

    
    if water_res>8000:
        send_email(1)
        time.sleep(180)
        send_email(1)
        time.sleep(180)
        send_email(1)
        break
        
        
    if BATTERY_CHECK==True:
        battery_res =battery.read_u16()
        print(battery_res)
        if battery_res<1300:
            led_g.value(0)
            led_y.value(1)
            send_email(0)

    #Check the day
    print(rtc.datetime())
    if (rtc.datetime()[2]==day):
        BATTERY_CHECK=False;
    else:
        day = rtc.datetime()[2]
        BATTERY_CHEK=True
    
    time.sleep(5)
        

