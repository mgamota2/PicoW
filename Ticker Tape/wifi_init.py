import network
import ubinascii
import machine
import urequests as requests
import time
from wifi_pw import secrets

def init_wifi():

    ssid = secrets['ssid']
    password = secrets['pw']
     
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid,password)


    # Wait for connect or fail
    wait = 10
    while wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        wait -= 1
        print('waiting for connection...')
        time.sleep(1)
     
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('wifi connection failed')
        return (0)
    else:
        print('connected')
        ip=wlan.ifconfig()[0]
        print('IP: ', ip)
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        print('mac = ' + mac)
        return (1)
     
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
            
    return html
