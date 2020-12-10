import serial
import time
import sys
import credentials
from datetime import datetime

start_time = datetime.now()

READ_TIMEOUT = 8

current_password = credentials.login['current_password']
current_secret = credentials.login['current_secret']
configured_password = credentials.login['last_password']
configured_secret = credentials.login['last_secret']
access_ports = b'int range g10/1-22'
trunk_ports = b'int range g0/13-16'
src_int = b'vlan 10'
access_vlan = b'switchport access vlan 16'
voice_vlan = b'switchport voice vlan 243'

# print('What is your IP address?')
# ip_add=input()
ip_add = (input('Enter Management Address\n'))
ip_split = ip_add.split('.')

host_name = (input('Enter Hostname\n'))
mng_ip = (ip_add + ' ' + '255.255.255.0')
default_gateway = str(ip_split[0] + '.' + ip_split[1] + '.' + ip_split[2] + '.' + '1')
COM_PORT = (input('Which COM port are you using?\n'))

def read_serial(console):
    data_bytes = console.inWaiting()
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ''

def login(console):
    print("Logging into router")
    while True:
        console.write(b'\r\n')
        time.sleep(1)
        input_data = console.read(console.inWaiting())
        print(input_data)
        if b'[yes/no]:' in input_data:
            console.write(b'no')
        elif b'User Access' in input_data:
            print(send_command(console, cmd=last_password))
            time.sleep(1)
        elif b'>' in input_data:
            console.write(b'en')
        elif b'Password' in input_data:
            print(send_command(console, cmd=last_secret))
            time.sleep(.5)
        elif b'config' in input_data:
            console.write(b'exit')
        elif b'#' in input_data:
            print("We are logged in")
            break

def send_command(console, cmd=''):
    console.write(cmd + '\r'.encode())
    time.sleep(1)
    return read_serial(console)

def wipe_switch(console):
    print(send_command(console, cmd=b'wr erase'))
    time.sleep(1)
    print(send_command(console, cmd=b'\r\n\r\n'))
    print(send_command(console, cmd=b'delete flash:vlan.dat'))
    time.sleep(1)
    print(send_command(console, cmd=b'\r\n\r\n'))
    print(send_command(console, cmd=b'reload\n'))
    time.sleep(.5)
    print(send_command(console, cmd=b'no'))
    print(send_command(console, cmd=b'\r\n\r\n'))
    time.sleep(320)
    print(send_command(console, cmd=b'\r\n\r\n'))
    print(send_command(console, cmd=b'\r\n\r\n'))

def global_commands(console):
    print(send_command(console, cmd=b'conf t'))
    print(send_command(console, cmd=b'no logg con'))
    console.write(str('hostname ' + host_name + '\n').encode())
    time.sleep(.5)
    console.write(str('ip default-gateway ' + default_gateway + '\n').encode())
    time.sleep(.5)
    print(send_command(console, cmd=b'service password-e'))
    print(send_command(console, cmd=b'ena s ' + current_secret))
    time.sleep(.5)
    print(send_command(console, cmd=b'usern tombstone pr 15 s ' + current_secret))
    time.sleep(.5)
    print(send_command(console, cmd=b'mls qos'))
    print(send_command(console, cmd=b'lldp run'))
    print(send_command(console, cmd=b'no ip source-route'))
    print(send_command(console, cmd=b'logg file flash:logfile.txt 1000000 info'))
    print(send_command(console, cmd=b'logg buff 65536'))
    print(send_command(console, cmd=b'clo t AKST -9 0'))
    print(send_command(console, cmd=b'clo s AKDT r last Sun Mar 01:00 last Sun Oct 01:00'))
    print(send_command(console, cmd=b'no ip http server'))
    print(send_command(console, cmd=b'no ip http secure-server'))
    print(send_command(console, cmd=b'ip sla responder'))

def ntp_commands(console):
    print(send_command(console, cmd=b'ntp se 10.25.1.6'))
    print(send_command(console, cmd=b'ntp se 10.25.1.7'))
    print(send_command(console, cmd=b'ntp authenticate'))
    print(send_command(console, cmd=b'ntp authentication-key 10 md5 01070F095E590100 7'))
    print(send_command(console, cmd=b'ntp trusted-key 12'))

def dns_dhcp_commands(console):
    print(send_command(console, cmd=b'ip do n cop.net'))
    print(send_command(console, cmd=b'ip nam 10.26.15.40 10.25.52.31'))
    print(send_command(console, cmd=b'ip do li conocophillips.net'))
    print(send_command(console, cmd=b'ip do li conoco.net'))
    print(send_command(console, cmd=b'ip dhcp snoop vlan 1-4094'))
    print(send_command(console, cmd=b'no ip dhcp snoop info option'))
    print(send_command(console, cmd=b'ip dhcp snoop'))
    print(send_command(console, cmd=b'ip device tracking probe delay 10'))

def mng_vlan(console):
    print(send_command(console, cmd=b'int ' + src_int))
    time.sleep(1)
    console.write(str('ip add ' + mng_ip + '\n').encode())
    time.sleep(1)
    print(send_command(console, cmd=b'no ip route-cache'))
    print(send_command(console, cmd=b'no ip mroute-cache'))
    print(send_command(console, cmd=b'no shut'))
    print(send_command(console, cmd=b'exit'))

def access_int(console):
    print(send_command(console, cmd=access_ports))
    time.sleep(.5)
    console.write(access_vlan + b'\n')
    time.sleep(.5)
    print(send_command(console, cmd=b'sw m a'))
    print(send_command(console, cmd=voice_vlan))
    time.sleep(.5)
    print(send_command(console, cmd=b'sw po max 50'))
    print(send_command(console, cmd=b'sw po v r'))
    print(send_command(console, cmd=b'sw po a ti 2'))
    print(send_command(console, cmd=b'sw po a ty i'))
    print(send_command(console, cmd=b'sw po'))
    print(send_command(console, cmd=b'no sn t l'))
    print(send_command(console, cmd=b'mls qos trust dscp'))
    print(send_command(console, cmd=b'no md a'))
    print(send_command(console, cmd=b'spa portf'))
    print(send_command(console, cmd=b'spa bpdug e'))
    print(send_command(console, cmd=b'spa g r'))
    print(send_command(console, cmd=b'ip dh sn l r 15'))
    print(send_command(console, cmd=b'exit'))

def trunk_int(console):
    print(send_command(console, cmd=trunk_ports))
    time.sleep(.5)
    print(send_command(console, cmd=b'sw m t'))
    print(send_command(console, cmd=b'mls qos trust dscp'))
    print(send_command(console, cmd=b'ip dh sn t'))
    print(send_command(console, cmd=b'exit'))

def aaa_commands(console):
    print(send_command(console, cmd=b'aaa new-model'))
    print(send_command(console, cmd=b'aaa authe l d g t local l'))
    print(send_command(console, cmd=b'aaa authe login NO-TACACS line'))
    print(send_command(console, cmd=b'aaa autho exec d g tacacs+ if-authenticated'))
    print(send_command(console, cmd=b'aaa autho com 0 d g t l none'))
    print(send_command(console, cmd=b'aaa autho com 1 d g t l none'))
    print(send_command(console, cmd=b'aaa autho com 15 d g t l none'))
    print(send_command(console, cmd=b'aaa accounting update periodic 15'))
    print(send_command(console, cmd=b'aaa ac e d sta g t'))
    print(send_command(console, cmd=b'aaa ac com 1 d sta g t'))
    print(send_command(console, cmd=b'aaa ac com 5 d sta g t'))
    print(send_command(console, cmd=b'aaa ac com 15 d sta g t'))
    print(send_command(console, cmd=b'aaa ac system d sta g t'))

def vtp_commands(console):
    print(send_command(console, cmd=b'vtp ver 2'))
    time.sleep(1)
    #     print(send_command(console, cmd= b'vtp domain null'))
    #     time.sleep(1)
    print(send_command(console, cmd=b'vtp domain Alpine'))
    time.sleep(1)
    print(send_command(console, cmd=b'vtp mode client'))
    time.sleep(1)

def vty_commands(console):
    print(send_command(console, cmd=b'line vty 0 4'))
    print(send_command(console, cmd=b'transport input ssh'))
    print(send_command(console, cmd=b'exec-timeout 30 0'))
    print(send_command(console, cmd=b'session-timeout 30'))
    print(send_command(console, cmd=b'password ' + current_password))
    print(send_command(console, cmd=b'logg syn'))
    print(send_command(console, cmd=b'line vty 5 15'))
    print(send_command(console, cmd=b'transport input ssh'))
    print(send_command(console, cmd=b'password ' + current_password))
    print(send_command(console, cmd=b'logg syn'))
    print(send_command(console, cmd=b'exec-timeout 30 0'))
    print(send_command(console, cmd=b'session-timeout 30'))

def console_commands(console):
    print(send_command(console, cmd=b'line con 0'))
    print(send_command(console, cmd=b'logg syn'))
    print(send_command(console, cmd=b'exec-t 30 0'))
    print(send_command(console, cmd=b'session-timeout 30'))
    print(send_command(console, cmd=b'login authe NO-TACACS'))
    print(send_command(console, cmd=b'password ' + current_password))

def source_int(console):
    print(send_command(console, cmd=b'ip tf s ' + src_int))
    print(send_command(console, cmd=b'ip do lo s ' + src_int))
    print(send_command(console, cmd=b'ip tacacs sour ' + src_int))
    print(send_command(console, cmd=b'ntp so ' + src_int))
    print(send_command(console, cmd=b'logg so ' + src_int))
    print(send_command(console, cmd=b'snmp- trap-s ' + src_int))

def tacacs_commands(console):
    print(send_command(console, cmd=b'tacacs- h 10.26.60.20'))
    time.sleep(.5)
    print(send_command(console, cmd=b'tacacs- h 158.139.170.16'))
    time.sleep(.5)
    print(send_command(console, cmd=b'tacacs- h 155.191.182.137'))
    time.sleep(.5)
    print(send_command(console, cmd=b'tacacs- k 7 047D02422724554B5B'))
    print(send_command(console, cmd=b'tacacs- di'))

def acl_commands(console):
    print(send_command(console, cmd=b'access-list 66 permit 136.226.69.43'))
    print(send_command(console, cmd=b'access-list 66 permit 10.26.15.10'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.198.247'))
    print(send_command(console, cmd=b'access-list 66 permit 10.25.52.9'))
    print(send_command(console, cmd=b'access-list 66 permit 10.25.32.7'))
    print(send_command(console, cmd=b'access-list 66 permit 136.226.90.8'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.195.0 0.0.0.255'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.170.0 0.0.0.63'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.162.0 0.0.0.127'))
    print(send_command(console, cmd=b'access-list 66 permit 155.191.182.156 0.0.0.3'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.104.8 0.0.0.7'))
    print(send_command(console, cmd=b'access-list 66 permit 158.139.49.48 0.0.0.15'))
    print(send_command(console, cmd=b'access-list 66 permit 153.15.98.64 0.0.0.31'))
    print(send_command(console, cmd=b'access-list 67 permit 158.139.170.24 0.0.0.3'))
    print(send_command(console, cmd=b'access-list 88 permit 10.25.52.62'))

def snmp_commands(console):
    print(send_command(console, cmd=b'snmp- h 158.139.170.25 S1mPl3@miNds'))
    print(send_command(console, cmd=b'snmp- h 158.139.170.26 S1mPl3@miNds'))
    print(send_command(console, cmd=b'snmp- h 158.139.195.19 S1mPl3@miNds'))
    print(send_command(console, cmd=b'snmp- h 158.139.195.20 S1mPl3@miNds'))
    print(send_command(console, cmd=b'snmp- com S1mPl3@miNds RO 66'))
    print(send_command(console, cmd=b'snmp- com Br@iNd3Ad! RW 67'))
    print(send_command(console, cmd=b'snmp- com D0ct3R_StrANG3 RO 88'))
    print(send_command(console, cmd=b'snmp- l Alaska local'))

def logging_commands(console):
    print(send_command(console, cmd=b'logging trap notifications'))
    print(send_command(console, cmd=b'logging host 158.139.170.25'))
    print(send_command(console, cmd=b'logging host 158.139.170.26'))
    print(send_command(console, cmd=b'logging host 10.26.15.10'))

def ssh_commands(console):
    print(send_command(console, cmd=b'crypto key gen rsa mod 1024'))
    time.sleep(2)
    print(send_command(console, cmd=b'ip ssh version 2'))
    print(send_command(console, cmd=b'ip ssh dscp 16'))

def login_banner(console):
    print(send_command(console, cmd=b'banner login %'))
    time.sleep(.5)
    print(send_command(console, cmd=b'                        W A R N I N G !!!!!!!'))
    print(send_command(console, cmd=b'       '))
    print(send_command(console, cmd=b'This is a private computer system to be accessed and used for'))
    print(send_command(console, cmd=b'company business purposes.  All access to it must be specifically'))
    print(send_command(console, cmd=b'authorized. Unauthorized access or use of this system is prohibited'))
    print(send_command(console, cmd=b'and may expose you to liability under criminal and/or civil law.'))
    print(send_command(console, cmd=b'       '))
    print(send_command(console, cmd=b'Unless provided for by a separate written agreement signed by the'))
    print(send_command(console, cmd=b'company, all information placed on this computer system is the'))
    print(send_command(console, cmd=b'property of the company. The company reserves the right to monitor,'))
    print(send_command(console, cmd=b'access, intercept, record, read, copy, capture and disclose all'))
    print(send_command(console, cmd=b'information received, sent through or stored in this computer'))
    print(send_command(console, cmd=b'system, without notice, for any purpose and at anytime.'))
    print(send_command(console, cmd=b'       '))
    print(send_command(console, cmd=b'By accessing, using and continuing to use this system, you agree to'))
    print(send_command(console, cmd=b'these terms of use, as the company may modify from time to time; you'))
    print(send_command(console, cmd=b'agree to waive any right or expectation of privacy regarding this'))
    print(send_command(console, cmd=b'system or your use of it; and you further warrant that you have'))
    print(send_command(console, cmd=b'proper authorization to use this system.'))
    print(send_command(console, cmd=b'       '))
    print(send_command(console, cmd=b'                 IF YOU DO NOT AGREE, LOG OFF NOW.'))
    print(send_command(console, cmd=b'%'))
    print(send_command(console, cmd=b'exit'))

# must follow login_banner to follow config sequence and be last function to call to exit properly
def exec_banner(console):
    console.write(str('sh ver | inc System serial\r\n').encode())
    time.sleep(.5)
    input_data = console.read(console.inWaiting()).decode()
    input_data = input_data.split(':')
    b = input_data[1]
    input_data2 = b.split('\r')
    a = input_data2[0]
    console.write(str('sh ver | inc Model number\r\n').encode())
    time.sleep(.5)
    input_data3 = console.read(console.inWaiting()).decode()
    input_data3 = input_data3.split(':')
    d = input_data3[1]
    input_data4 = d.split('\r')
    c = input_data4[0]
    print(send_command(console, cmd=b'conf t'))
    print(send_command(console, cmd=b'banner exec %'))
    time.sleep(.5)
    print(send_command(console, cmd=b'**********************************'))
    print(send_command(console, cmd=b'Location:          Alpine'))
    print(send_command(console, cmd=b'Department:        Operations'))
    console.write(str('Switch Name:       ' + host_name + '\n').encode())
    time.sleep(.5)
    print(send_command(console, cmd=b'Type:              Switch'))
    print(send_command(console, cmd=b'Manufacturer:      Cisco'))
    console.write(str('Model:            ' + c + '\n').encode())
    time.sleep(.5)
    console.write(str('Serial No:        ' + a + '\n').encode())
    time.sleep(.5)
    print(send_command(console, cmd=b'**********************************'))
    print(send_command(console, cmd=b'%'))
    print(send_command(console, cmd=b'exit'))


def main():
    console = serial.Serial(
        port = COM_PORT,
        baudrate = 9600,
        parity = 'N',
        stopbits = 1,
        bytesize = 8,
        timeout = READ_TIMEOUT)

    if not console.isOpen():
        sys.exit()

#    login(console)

#    wipe_switch(console)

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

    print(send_command(console, cmd=b'wr'))
    print(send_command(console, cmd=b'exit'))
    print(datetime.now() - start_time)


if __name__ == '__main__':
    main()




