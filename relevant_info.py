import serial
import time
import sys
import credentials
import re
import regex
from datetime import datetime

new_password = credentials.login['new_password']
new_secret = credentials.login['new_secret']
old_password = credentials.login['old_password']
old_secret = credentials.login['old_secret']
old_old_password = credentials.login['old_old_password']
old_old_secret = credentials.login['old_old_secret']


def read_serial(console):
    data_bytes = console.inWaiting()
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ''


def send_command(console, cmd=''):
    console.write(cmd + '\r'.encode())
    time.sleep(1)
    return read_serial(console)




def ios_scrape(console):
    console.write(str('sh ver | inc IOS.*Version\r\n').encode())
    time.sleep(.5)
    ios_data = console.read(console.inWaiting()).decode()
    ios_data = ios_data.split(',')
    print(ios_data[2])
    print('----------------------------------') 


def uptime(console):
    console.write(str('sh ver | inc uptime\r\n').encode())   # some ios versions want to use the section regex
    time.sleep(.5)
    switch_uptime = console.read(console.inWaiting()).decode()
#    print(switch_uptime)
    switch_uptime = switch_uptime.split()
#    print(switch_uptime)
    switch_uptime =(switch_uptime[6], switch_uptime[7], switch_uptime[8], switch_uptime[9], switch_uptime[10], switch_uptime[11])
    switch_uptime = ' '.join(switch_uptime)
    print(switch_uptime)
    print('----------------------------------')
    print(' ')
    

def cdp_nei(console):
    console.write(b'sh cdp nei det | inc (SEP|Phone|Interface)\r\n')
    time.sleep(1)
    output = console.read(console.inWaiting()).decode()      
    output = output.splitlines()
#    print(output)
#    output = list(dict.fromkeys(output))   #Removes any duplicate entries
    output = [x for x in output if ('Device' in x or 'Platform' in x or 'Port 1' in x)]   #filters list to strings that contain x
    dash = '-----------------------------------------------------------'
    n = 3   # adding 'dash after every 3rd element
    i = n
    while i < len(output):
        output.insert(i, dash)
        i +=(n+1)
    n = 4   # adding new line after every fourth element
    x = n
#    while x < len(output):
#        output.insert(x, ' ')
#        x +=(n+1)    
    print('IP Phones on switch are:')
    print('*****************')
#    print(' ')
    print(*output, sep = '\n')
    print(' ')


def lldp_nei(console):
    console.write(b'sh lldp nei d | inc (System Name|^Local Intf|   IP|^Port)\r\n')
    time.sleep(1)
    output = console.read(console.inWaiting()).decode()
    output = output.splitlines()
    output = [x for x in output if not 'SW PORT' in x]
    output = [x for x in output if not ':P1' in x]
    output = [x for x in output if not 'nei' in x]   #removes index containing 'nei'
    foo = [output.index(i) for i in output if 'SEP' in i] # getting index of strings that contain 'SEP'       
    m=[]                             #creating a blank list
    for index in foo:                #looking for index after index containing 'SEP'      
        index -= 1
        m.append(index)                         #now I have the index numbers I want to remove from output!
    t=[output[i] for i in m]         #using output from m to identify index in output
    dmx = [x for x in output if x not in t]   #removing stranded phone interfaces from main output list
    dmx = [x for x in dmx if not 'SEP' in x]
    dmx = [x for x in dmx if not 'Port Desc' in x]
    dmx = [sub.replace ('Port id', 'Remote Interface') for sub in dmx]
    dmx = [sub.replace ('System Name', 'Remote Device') for sub in dmx]
    dmx = [sub.replace ('Intf', 'Interface') for sub in dmx]
    dmx = [sub.replace ('    IP', 'Remote Device IP:') for sub in dmx]
    dash = '-----------------------------------------------------------'
    n = 4   # adding 'dash after every fourth element
    i = n
    while i < len(dmx):
        dmx.insert(i, dash)
        i +=(n+1)
    n = 5   # adding new line after every fifth element
    x = n
    while x < len(dmx):
        dmx.insert(x, ' ')
        x +=(n+1)
    print('Devices attached Are: ')
    print('*****************')
    print(*dmx, sep = '\n')
    print(' ')

def int_status(console):
    console.write(b'sh int status | inc notconnect\r\n')
    time.sleep(3)
    output = console.read(console.inWaiting()).decode()
    output = output.split('\n')
    interface = ('Fa', 'Gi')
    print('Available ports are ')
    print('*****************')
    for x in output:
        if x.startswith(interface):
            x = x.split()
            x=(x[0] + '   vlan ' + x[2])
            print(x)
#    ^[A-Z][A-Za-z]+\s?([0-1]+/){0,}[0-9]+$  
#    print(*output, sep = '\n')
def model_number(console):
    console.write(str('sh ver | inc Model number\r').encode())
    time.sleep(.5)    
    input_data = console.read(console.inWaiting()).decode()
    input_data = input_data.split(':')
    d=input_data[1]
    input_data4 = d.split('\r')
    c=input_data4[0]
    print(c)


def login(console):
#    print ("Logging into router")
    while True:
        console.write(b'\r\n')
        time.sleep(2.5)
        input_data = console.read(console.inWaiting())
        print(input_data)
        if b'[yes/no]:' in input_data:            
            console.write(b'no')   
        elif b'User Access' in input_data:
            print(send_command(console, cmd= new_password))      
            time.sleep(2.5)
        elif b'>' in input_data:
            console.write(b'en')   
        elif b'Password' in input_data:
            print(send_command(console, cmd= new_secret))      
            time.sleep(.5)
        elif b'config' in input_data:
            console.write(b'exit')
        elif b'#' in input_data:
#            print ("We are logged in") 
            break
       

def main():
    console= serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=8)
    
    login(console)
    print(send_command(console, cmd= b'terminal length 0'))
    print('----------------------------------')
    print(' Relevant Information.............')
    print('----------------------------------')
    model_number(console)
    
    ios_scrape(console)
    
    uptime(console)
    
    cdp_nei(console)
    
    lldp_nei(console)
    
    int_status(console)
    print(send_command(console, cmd= b'terminal length 24'))
#    print(send_command(console, cmd= b'exit'))
#    print(send_command(console, cmd= b'exit'))
    
if __name__ == '__main__':
    main()
    