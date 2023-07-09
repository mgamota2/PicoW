import machine
import socket
import network
import time
import ubinascii
import urequests

#Create a "Stock" class which has a API request result, name, price, and percent change
class Stock():
    def __init__(self, name):
        self.name=name.upper()
        self.price=0
        self.percent_change=0
        self.result=[]
        self.url = 'https://finnhub.io/api/v1/quote?symbol=' + self.name + '&token=cikt6q1r01qk492qui8gcikt6q1r01qk492qui90'
    
    #Get the data from the finnhub API, store it in the object
    def get_data(self):
        r = urequests.get(self.url)
        self.result = str(r.content)
        #print(self.result)
        self.get_price()
        self.get_percent()

    #Helper function to parse the API response for the price
    def get_price(self):
        price_start_index=int(self.result.find('c"')+3)
        i=price_start_index
        while self.result[i]!=",":
            i+=1
        price_end_index=i
        self.price = self.result[price_start_index: (price_end_index)]
        #print(self.price)
    
    #Helper function to parse the API response for the percent change
    def get_percent(self):
        
        percent_start_index=int(self.result.find('dp"')+4)
        i=percent_start_index
        while self.result[i]!=".":
            i+=1
        percent_end_index=i+3
        self.percent_change = self.result[percent_start_index: (percent_end_index)]
        #print(self.percent_change)
                
