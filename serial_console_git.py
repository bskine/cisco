import serial
import time
import sys
import credentials
from datetime import datetime
start_time = datetime.now()

READ_TIMEOUT=8

new_password = credentials.login['new_password']
new_secret = credentials.login['new_secret']
old_password = credentials.login['old_password']
old_secret = credentials.login['old_secret']
old_old_password = credentials.login['old_old_password']
old_old_secret = credentials.login['old_old_secret']
access_ports = b'int range g0/1-12'
trunk_ports = b'int range g0/13-16'
src_int = b'vlan 1'

print('What is your IP address?')
ip_add=input()
ip_split = ip_add.split('.')
    
host_name = ('sw1')
mng_ip = (ip_add + ' ' + '255.255.255.0')
default_gateway = str(ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.' + '1')


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
        time.sleep(1)
        input_data = console.read(console.inWaiting())
        print(input_data)
        if b'[yes/no]:' in input_data:            
            console.write(b'no')   
        elif b'User Access' in input_data:
            print(send_command(console, cmd= old_password))      
            time.sleep(1)
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


def wipe_switch(console):
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


def global_commands(console):
    print(send_command(console, cmd= b'conf t'))
    print(send_command(console, cmd= b'no logg con'))    
    console.write(str('hostname ' + host_name + '\n').encode())    
    time.sleep(1)
    console.write(str('ip default-gateway ' + default_gateway + '\n').encode())     
    time.sleep(1)
    print(send_command(console, cmd= b'service password-e'))
    print(send_command(console, cmd= b'ena s ' + new_secret))                
    time.sleep(.5)
    print(send_command(console, cmd= b'mls qos')) 
    print(send_command(console, cmd= b'lldp run'))
    print(send_command(console, cmd= b'no ip source-route'))
    print(send_command(console, cmd= b'logg file flash:logfile.txt 1000000 info')) 
    print(send_command(console, cmd= b'logg buff 65536'))
    print(send_command(console, cmd= b'no ip http server'))
    print(send_command(console, cmd= b'no ip http secure-server')
    print(send_command(console, cmd= b'exit'))
    

def ntp_commands(console):
    
def dns_dhcp_commands(console):
   
def mng_vlan(console):
    print(send_command(console, cmd= b'int ' + src_int))
    time.sleep(1)
    console.write(str('ip add ' + mng_ip + '\n').encode())
    time.sleep(1)
    print(send_command(console, cmd= b'no ip route-cache'))
    print(send_command(console, cmd= b'no ip mroute-cache'))
    print(send_command(console, cmd= b'no shut'))
    print(send_command(console, cmd= b'exit'))


def access_int(console):
    print(send_command(console, cmd= access_ports))      
    time.sleep(.5)
    print(send_command(console, cmd= b'sw ac v 1'))
    time.sleep(.5)
    print(send_command(console, cmd= b'sw m a'))
    print(send_command(console, cmd= b'sw v v 2'))
    time.sleep(.5)
    print(send_command(console, cmd= b'sw po max 50'))
    print(send_command(console, cmd= b'sw po v r'))
    print(send_command(console, cmd= b'sw po a ti 2'))
    print(send_command(console, cmd= b'sw po a ty i'))
    print(send_command(console, cmd= b'sw po'))
    print(send_command(console, cmd= b'no sn t l'))
    print(send_command(console, cmd= b'mls qos trust dscp'))
    print(send_command(console, cmd= b'no md a'))
    print(send_command(console, cmd= b'spa portf'))
    print(send_command(console, cmd= b'spa bpdug e'))
    print(send_command(console, cmd= b'spa g r'))
    print(send_command(console, cmd= b'ip dh sn l r 15'))
    print(send_command(console, cmd= b'exit'))
    
    
def trunk_int(console):
    print(send_command(console, cmd= trunk_ports))   
    time.sleep(.5)    
    print(send_command(console, cmd= b'sw m t'))
    print(send_command(console, cmd= b'mls qos trust dscp'))
    print(send_command(console, cmd= b'ip dh sn t'))   
    print(send_command(console, cmd= b'exit'))


def aaa_commands(console):
    print(send_command(console, cmd= b'aaa new-model'))
    print(send_command(console, cmd= b'aaa authe l d g t local l'))
    print(send_command(console, cmd= b'aaa authe login NO-TACACS line'))
    print(send_command(console, cmd= b'aaa autho exec d g tacacs+ if-authenticated'))
    print(send_command(console, cmd= b'aaa autho com 0 d g t l none'))
    print(send_command(console, cmd= b'aaa autho com 1 d g t l none'))
    print(send_command(console, cmd= b'aaa autho com 15 d g t l none'))
    print(send_command(console, cmd= b'aaa accounting update periodic 15'))
    print(send_command(console, cmd= b'aaa ac e d sta g t'))
    print(send_command(console, cmd= b'aaa ac com 1 d sta g t'))
    print(send_command(console, cmd= b'aaa ac com 5 d sta g t'))
    print(send_command(console, cmd= b'aaa ac com 15 d sta g t'))
    print(send_command(console, cmd= b'aaa ac system d sta g t'))


def vtp_commands(console):
    print(send_command(console, cmd= b'vtp ver 2'))
    time.sleep(1)
    print(send_command(console, cmd= b'vtp domain vtp'))
    time.sleep(1)
    print(send_command(console, cmd= b'vtp mode client'))
    time.sleep(1)


def vty_commands(console):
    print(send_command(console, cmd= b'line vty 0 4'))
    print(send_command(console, cmd= b'transport input ssh'))
    print(send_command(console, cmd= b'exec-timeout 30 0'))
    print(send_command(console, cmd= b'session-timeout 30'))
    print(send_command(console, cmd= b'password ' + new_password))                
    print(send_command(console, cmd= b'logg syn'))    
    print(send_command(console, cmd= b'line vty 5 15'))
    print(send_command(console, cmd= b'transport input ssh'))
    print(send_command(console, cmd= b'password ' + new_password))                
    print(send_command(console, cmd= b'logg syn'))    
    print(send_command(console, cmd= b'exec-timeout 30 0'))
    print(send_command(console, cmd= b'session-timeout 30'))


def console_commands(console):
    print(send_command(console, cmd= b'line con 0'))
    print(send_command(console, cmd= b'logg syn'))
    print(send_command(console, cmd= b'exec-t 30 0'))        
    print(send_command(console, cmd= b'session-timeout 30'))
    print(send_command(console, cmd= b'login authe NO-TACACS'))        
    print(send_command(console, cmd= b'password ' + new_password))


def source_int(console):
    print(send_command(console, cmd= b'ip tf s ' + src_int))
    print(send_command(console, cmd= b'ip do lo s ' + src_int))
    print(send_command(console, cmd= b'ip tacacs sour ' + src_int))
    print(send_command(console, cmd= b'ntp so ' + src_int))    
    print(send_command(console, cmd= b'logg so ' + src_int))    
    print(send_command(console, cmd= b'snmp- trap-s ' + src_int))


def tacacs_commands(console):
    print(send_command(console, cmd= b'tacacs- di'))


def acl_commands(console):
    

def snmp_commands(console):
    
    
def logging_commands(console):    
    print(send_command(console, cmd= b'logging trap notifications'))


def ssh_commands(console):
    print(send_command(console, cmd= b'crypto key gen rsa mod 1024'))
    time.sleep(2)
    print(send_command(console, cmd= b'ip ssh version 2'))
    print(send_command(console, cmd= b'ip ssh dscp 16'))


def login_banner(console):
    
#must follow login_banner to follow config sequence and be last function to call to exit properly   
def exec_banner(console):
    print(send_command(console, cmd= b'exit'))
    console.write(str('sh ver | inc System serial\r\n').encode())
    time.sleep(.5)
    input_data = console.read(console.inWaiting()).decode()
    input_data = input_data.split(':')
    b=input_data[1]
    input_data2 = b.split('\r')
    a=input_data2[0]
    console.write(str('sh ver | inc Model number\r\n').encode())
    time.sleep(.5)    
    input_data3 = console.read(console.inWaiting()).decode()
    input_data3 = input_data3.split(':')
    d=input_data3[1]
    input_data4 = d.split('\r')
    c=input_data4[0]
    print(send_command(console, cmd= b'conf t'))
    print(send_command(console, cmd= b'banner exec %'))
    time.sleep(.5)
    print(send_command(console, cmd= b'**********************************'))
    print(send_command(console, cmd= b'Location:          1'))
    print(send_command(console, cmd= b'Department:        1'))
    console.write(str('Switch Name:       ' + host_name + '\n').encode())   
    time.sleep(.5)
    print(send_command(console, cmd= b'Type:              Switch'))
    print(send_command(console, cmd= b'Manufacturer:      Cisco'))
    console.write(str('Model:            ' + c + '\n').encode())    
    time.sleep(.5)
    console.write(str('Serial No:        ' + a + '\n').encode())   
    time.sleep(.5)
    print(send_command(console, cmd= b'**********************************'))
    print(send_command(console, cmd= b'%'))
    print(send_command(console, cmd= b'exit'))
    
    
def main():
    console= serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity='N',
    stopbits=1,
    bytesize=8,
    timeout=READ_TIMEOUT)

    if not console.isOpen():
        sys.exit()
    
    login(console)
    
    wipe_switch(console)
    
    login(console)

    global_commands(console)
    
    ntp_commands(console)
    
    dns_dhcp_commands(console)
    
    mng_vlan(console)
    
    access_int(console)
    
    trunk_int(console)
    
    aaa_commands(console)
    
    vtp_commands(console)
   
    vty_commands(console)
    
    console_commands(console)
    
    source_int(console)
    
    tacacs_commands(console)
    
    acl_commands(console)
    
    snmp_commands(console)
    
    logging_commands(console)
    
    ssh_commands(console)
    
    login_banner(console)
   
    exec_banner(console)
 
    print(send_command(console, cmd= b'wr'))
    print(send_command(console, cmd= b'exit'))
    print(datetime.now() - start_time)

if __name__ == '__main__':
    main()




