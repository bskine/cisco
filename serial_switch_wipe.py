import serial
import time
import sys
import credentials

READ_TIMEOUT=8
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
    

 
def login(console):
    print ("Logging into router")
    while True:
        console.write(b'\r\n')
        time.sleep(2.5)
        input_data = console.read(console.inWaiting())
        print(input_data)
        if b'[yes/no]:' in input_data:            
            console.write(b'no')   
        elif b'User Access' in input_data:
            print(send_command(console, cmd= old_password))      
            time.sleep(2.5)
        elif b'>' in input_data:
            console.write(b'en')   
        elif b'Password' in input_data:
            print(send_command(console, cmd= old_secret))      
            time.sleep(.5)
        elif b'config' in input_data:
            console.write(b'exit')
        elif b'#' in input_data:
            print ("We are logged in")
            break
            
def send_command(console, cmd=''):
    console.write(cmd + '\r'.encode())
    time.sleep(1)
    return read_serial(console)


def switch_wipe(console):
    print(send_command(console, cmd= b'wr erase'))
    time.sleep(1)
    print(send_command(console, cmd= b'\r\n\r\n'))
    print(send_command(console, cmd= b'delete flash:vlan.dat'))
    time.sleep(1)
    print(send_command(console, cmd= b'\r\n\r\n'))
    print(send_command(console, cmd= b'reload\n'))
    time.sleep(.5)
    print(send_command(console, cmd= b'no'))
    print(send_command(console, cmd= b'\r\n\r\n'))
    time.sleep(320)
    print(send_command(console, cmd= b'\r\n\r\n'))
    print(send_command(console, cmd= b'\r\n\r\n'))



def main():
    console= serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=READ_TIMEOUT
)

        
    login(console)
    
    switch_wipe(console)

if __name__ == '__main__':
    main()    
    