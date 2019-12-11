#!/usr/bin/env
from netmiko import Netmiko
from netmiko import ConnectHandler
from multiprocessing import Process
from testlab_device_list import device_list as devices
import time


def sh_int_status(a_device):
    net_connect = ConnectHandler(**a_device)
    output2= net_connect.send_command('show int status', use_textfsm=True)
    output3a = net_connect.send_command_timing('show version', use_textfsm=True)
    local_host = str(output3a[0].get('hostname'))
    print('{:^75}'.format('INTERFACE STATUS OF ' + local_host +' IS:'))
    print('*' * 75)
    print('{:<12}{:<12}{:^11}{:<12}{:<12}{:<12}'.format('PORT', 'STATUS', 'VLAN', 'DUPLEX', 'SPEED', 'TYPE'))
    print('*' * 75)
    for k in output2[0:28]:
        print('{:<12}{:<12}{:^11}{:<12}{:<12}{:>12}'.format(str(k.get('port')), str(k.get('status')), str(k.get('vlan')),
                                                             str(k.get('duplex')), str(k.get('speed')), str(k.get('type'))))
    print('\n')
    print('\n')
    

def main():
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=sh_int_status, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)
        time.sleep(1)
        
    for a_proc in procs:
#        print(a_proc)
        a_proc.join()
    
    
    
if __name__ == '__main__':
    main()                                                              