import machine
import time

class trackPins:
    def __init__(self, pin1, pin2, pin3, pin4, flipped=False):
            self.flipped = flipped
            self.pin1=machine.Pin(pin1, machine.Pin.OUT)
            self.pin2=machine.Pin(pin2, machine.Pin.OUT)
            self.pin3=machine.Pin(pin3, machine.Pin.OUT)
            self.pin4=machine.Pin(pin4, machine.Pin.OUT)
            self.pin1.value(0)
            self.pin2.value(0)
            self.pin3.value(0)
            self.pin4.value(0)
    def setState(self, i):
        if (i==1): #Flipped
            
            self.pin1.value(1)
            self.pin2.value(0)
            self.pin3.value(1)
            self.pin4.value(0)
            self.flipped=True
        else: #Defalut
            
            self.pin1.value(0)
            self.pin2.value(1)
            self.pin3.value(1)
            self.pin4.value(1)
            self.flipped=False
        
        time.sleep(0.3)
        self.pin1.value(0)
        self.pin2.value(0)
        self.pin3.value(0)
        self.pin4.value(0)
    def getState(self):
        return (self.flipped)


class railPins:
    def __init__(self, pin1, pin2):
            self.pin1=machine.Pin(pin1, machine.Pin.OUT)
            self.pin2=machine.Pin(pin2, machine.Pin.OUT)
            self.pin1.value(0)
            self.pin2.value(0)
    def setState(self, i):
        if (i==1): #Forwards
            self.pin1.value(1)
            self.pin2.value(0)
        elif (i==2):
            self.pin1.value(1)
            self.pin2.value(1)
        else: #Backwards
            self.pin1.value(0)
            self.pin2.value(1)
    def getState(self):
        return self.pin1.value()
    
def stop(pin, railPins):
    while pin.duty_u16()>32000:
        pin.duty_u16(int(pin.duty_u16()/2))
        time.sleep(0.3)
    pin.duty_u16(26200)
    railPins.setState(2)

def myround(x, base=5):
    return base * round(x/base)