import machine
import socket
import network
import time
import ubinascii
import urequests
from wifi_pw import secrets
from wifi_init import *
from stock_data import *
import neopixel
from printChars import *
from bits import *

np = neopixel.NeoPixel(machine.Pin(16), n=3,bpp=3,timing=1)

ticker_list=[]
my_stocks=[]
stocks_list=[]

clear()
led=machine.Pin('LED', machine.Pin.OUT)

x = init_wifi()
led.value(x)
# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)

def get_entries(website_data):
    tickers=[]
    first_ticker_start_index=int(website_data.find('s=')+2) #Look for "entries="
    
    safari = int(website_data.find("favicon.ico")) #This only comes up when on PC
    
    if (safari==-1):
        string_end = int(website_data.find("HTTP/1.1")-1)
    else:   
        string_end = int(website_data.find("Accept-Encoding")-4)

    #If it can't find any entries
    if (first_ticker_start_index==1):
        return tickers
    i=first_ticker_start_index

    print(website_data)

    #Split into list of tickers
    ticker_string=website_data[first_ticker_start_index:string_end]
    tickers=ticker_string.split("%2C")
    
    return tickers

#Update info from a list of Stock objects
def update_stocks(list_stocks, index=-1):
    try:
        list_stocks[index].get_data()
    except:
        print('No index')
    return list_stocks

#Turn a list of stock symbols into a list of Stock objects
def stock_obj_list(string_list):
    stock_list=[]
    for tick in string_list:
        stock_list.append(Stock(tick))
    return stock_list

first_pass = True
# Listen for connections
while True:
    #Web server access
    try:
        led.value(1)
        
        conn, addr = s.accept()
        
        led.value(0)
        
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)

        #print('Content = %s' % str(request))
        request = str(request)
        
        #Try to get ticker symbols from URL
        new_ticker_list = get_entries(request)
        
        #If it is not an empty list, this means the user has entered stocks so we update the ticker list
        #We also make the ticker names into objects
        #We also change the timeout for the socket so we can update our stock data
        
        if len(new_ticker_list) != 0:
            ticker_list=new_ticker_list
            my_stocks=stock_obj_list(ticker_list)
            s.settimeout(1.0)

        response = get_html('index.html')           

        
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
        
        
    except OSError as e:
        led.value(0)
        print('Connection closed from timeout')
    except (KeyboardInterrupt):
        clear()
        s.close()
        led.value(0)
        print('Connection closed')
        break
    
    print(ticker_list)
    
    if first_pass==True:
        for i in range (len(my_stocks)):
            update_stocks(my_stocks, i)
        first_pass=False
        
    
    #Iterate over the stocks, update them, then display their name, price, and percent change
    for i in range (len(my_stocks)):
        if str(my_stocks[i].percent_change)=='0':
            color='blue'
        elif '-' in str(my_stocks[i].percent_change):
            color='red'
        else:
            color='green'
            
        print_string(str(my_stocks[i].name), color)
        update_stocks(my_stocks, index=i)
        print_num(str(my_stocks[i].price), color)
        time.sleep(3)
        print_p(str(my_stocks[i].percent_change), color)
        time.sleep(3)
        
    
    
    



