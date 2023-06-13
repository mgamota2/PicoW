import machine
import socket
import network
import time
import ubinascii
from wifi_pw import secrets
from wifi_init import *
from train_func import *



led=machine.Pin('LED', machine.Pin.OUT)

#Create objects for track switches, rail control, and speed control
track1 = trackPins(2, 3, 4, 5)
track2 = trackPins(6, 7, 8, 9)
track3 = trackPins(10,11,12,13)
track4 = trackPins(21, 20, 19, 18)

track1.setState(0)
track2.setState(0)
track3.setState(0)
track4.setState(0)


railObj = railPins(14, 15)
railObj.setState(1)


speed = machine.PWM(machine.Pin(16))
duty_u16=(0)
speed.freq(5000)

# Track 1
# State 1: G1A = 1 | G1B = 0 | G1C = 1 | G1D = 0
# State 2: G1A = 0 | G1B = 1 | G1C = 1 | G1D = 1

#Track 2
# State 1: G2A = 1 | G2B = 0 | G2C = 1 | G2D = 0
# State 2: G2A = 0 | G2B = 1 | G2C = 1 | G2D = 1

x = init_wifi()
led.value(x)
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
        
        
        if (request.find('button2')!=-1):
            print('Stopping')
            stop(speed)
            

        else:
            index1 = request.find('slider=')  + len('slider=')
            
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
                
          
            if (request.find('button3')!=-1) and railObj.getState()==0:
                print('switching direction')
                stop(speed)
                print('Forwards')
                railObj.setState(1)
            
            if (request.find('button1')!=-1) and railObj.getState()==1:
                print('switching direction')
                stop(speed)
                print('Backwards')
                railObj.setState(0)
            
            index2 = request.find('checkbox1=')  + len('checkbox1=')
            if request[index2]=="t" and track1.getState()==False:
                print('Switching track 1')
                track1.setState(1)
            elif request[index2]=="f" and track1.getState()==True:
                print('Switching track 1')
                track1.setState(0)
                
            index3 = request.find('checkbox2=')  + len('checkbox2=')
            if request[index3]=="t" and track2.getState()==False:
                print('Switching track 2')
                track2.setState(1)
            elif request[index3]=="f" and track2.getState()==True:
                print('Switching track 2')
                track2.setState(0)
                
            index4 = request.find('checkbox3=')  + len('checkbox3=')
            if request[index4]=="t" and track3.getState()==False:
                print('Switching track 3')
                track3.setState(1)
            elif request[index4]=="f" and track3.getState()==True:
                print('Switching track 3')
                track3.setState(0)
                
            index5 = request.find('checkbox4=')  + len('checkbox4=')
            if request[index5]=="t" and track4.getState()==False:
                print('Switching track 1')
                track4.setState(1)
            elif request[index5]=="f" and track4.getState()==True:
                print('Switching track 1')
                track4.setState(0)
            
        
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




