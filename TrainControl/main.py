import machine
import socket
import network
import time
import ubinascii
from wifi_pw import secrets

class trackPins:
    def __init__(self, pin1, pin2, pin3, pin4):
            self.pin1=machine.Pin(pin1, machine.Pin.OUT)
            self.pin2=machine.Pin(pin2, machine.Pin.OUT)
            self.pin3=machine.Pin(pin3, machine.Pin.OUT)
            self.pin4=machine.Pin(pin4, machine.Pin.OUT)
    def setState(self, i):
        if (i==1):
            self.pin1.value(1)
            self.pin2.value(0)
            self.pin3.value(1)
            self.pin4.value(0)
        else:
            self.pin1.value(0)
            self.pin2.value(1)
            self.pin3.value(1)
            self.pin4.value(1)
        
        time.sleep(0.1)
        self.pin1.value(0)
        self.pin3.value(0)
        self.pin4.value(0)


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
        else: #Backwards
            self.pin1.value(0)
            self.pin2.value(1)
    def getState(self):
        return self.pin1.value()
    
def stop(pin):
    while pin.duty_u16()>32000:
        pin.duty_u16(int(pin.duty_u16()/2))
        time.sleep(0.3)
    pin.duty_u16(26200)

def myround(x, base=5):
    return base * round(x/base)

led=machine.Pin('LED', machine.Pin.OUT)

speed = machine.PWM(machine.Pin(16))
duty_u16=(0)
speed.freq(5000)


#Create objects for track switches, rail control, and speed control
track1 = trackPins(2, 3, 4, 5)
track2 = trackPins(6, 7, 8, 9)
track3 = trackPins(10,11,12,13)
track4 = trackPins(21, 20, 19, 18)


railObj = railPins(14, 15)

railObj.setState(1)

# Track 1
# State 1: G1A = 1 | G1B = 0 | G1C = 1 | G1D = 0
# State 2: G1A = 0 | G1B = 1 | G1C = 1 | G1D = 1

#Track 2
# State 1: G2A = 1 | G2B = 0 | G2C = 1 | G2D = 0
# State 2: G2A = 0 | G2B = 1 | G2C = 1 | G2D = 1

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
else:
    print('connected')
    led.value(1)
    ip=wlan.ifconfig()[0]
    print('IP: ', ip)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('mac = ' + mac)
 
# Function to load in html page    
def get_html(html_name):
    with open(html_name, 'r') as file:
        html = file.read()
        
    return html

# HTTP server with socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# Listen for connections
while True:
    try:
        
        conn, addr = s.accept()
        
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        if "signed-exchange" in str(request):
            pass
        print('Content = %s' % str(request))
        request = str(request)
        
        
        if (request.find('E?')!=-1):
            print('Stopping')
            stop(speed)
            

        else:
            index1 = request.find('Speed=')  + len('Speed=')
            
            #Parse int
            try:
                if request[index1].isdigit():
                    offset = 1
                    if request[index1+1].isdigit():
                        offset = 2
                        if request[index1+2].isdigit():
                            offset = 3
                    duty = (int(request[index1:index1+offset])*230)+26200
                    print(duty, '\n')
                    speed.duty_u16(duty)
            except:
                pass
                
          
            if (request.find('F')!=-1) and (railObj.getState()==0):
                print('switching direction')
                stop(speed)
                print('Forwards')
                railObj.setState(1)
            
            if (request.find('B')!=-1) and (railObj.getState()==1):
                print('switching direction')
                stop(speed)
                print('Backwards')
                railObj.setState(0)
            
        
        response = get_html('index.html')
        response = response.replace('slider_value1', str(myround(int((speed.duty_u16()-26200)/230))))
            

        
        conn.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        conn.send(response)
        conn.close()
        led.value(1)
    except OSError as e:
        conn.close()
        s.close()
        led.value(0)
        print('Connection closed')
        break
    except (KeyboardInterrupt):
        conn.close()
        s.close()
        led.value(0)
        print('Connection closed')
        break




