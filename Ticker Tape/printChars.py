import neopixel
import machine
import time
from bits import *


# 32 LED strip connected to X8.
p = machine.Pin(5)
n = neopixel.NeoPixel(p, 147)
bitmap1=bitmap

def write_char(color, character):
    n[i] = (i * 8, 0, 0)
    n.write

def getLEDpos(x, y):
    if (x %2==0):
        pos=x*21+y
    else:
        pos = (x * 21) + (20 - y)
      
    return pos

def print_char(char, color ,drift=0, bitmap=bitmap):
    size=len(bitmap[char])
    for i in range(0,size):
        x=getLEDpos(bitmap[char][i][0], bitmap[char][i][1]+drift)
        if color=='blue':
            n[x] = (0, 0, 8)
        elif color == 'red':
            n[x] = (8, 0, 0)
        elif color == 'green':
            n[x] = (0, 8, 0)
    n.write()
    
def clear():
    for x in range(0,147):
        n[x]=(0,0,0)
    n.write()
    
def print_string(string, color='blue', bitmap=bitmap, bitmap_widths=bitmap_widths):
    clear()
    i = 0
    for c in string:
        try:
            print_char(c, color, i)
            i += (bitmap_widths[c] + 1)
        except:
            print('Invalid')

def print_num(string, color='blue', bitmap=bitmap, bitmap_widths=bitmap_widths):
    clear()
    i=0
    whole = string.split('.')
    for c in whole[0]:
        try:
            print_char(c, color, i)
            i += (bitmap_widths[c]+1)
        except:
            print('Invalid')
    
    print_char('.', color, i)
    i+=2
    for c in whole[1]:
        try:
            print_char(c, color, i)
            i += (bitmap_widths[c]+1)
        except:
            print('Invalid')

def print_p(string, color='blue', bitmap=bitmap, bitmap_widths=bitmap_widths):
    clear()
    i=0
    whole = string.split('.')
    for c in whole[0]:
        try:
            print_char(c, color, i)
            i += (bitmap_widths[c]+1)
        except:
            print('Invalid')
    
    try:
        print_char('.', color, i)
    except:
        print('Invalid')
        
    i+=2
    for c in whole[1]:
        try:
            print_char(c, color, i)
            i += (bitmap_widths[c]+1)
        except:
            print('Invalid')
    try:
        print_char('%', color, i)
    except:
        print('Invalid')



        


