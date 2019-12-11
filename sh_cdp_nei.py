#!/usr/bin/env
from netmiko import Netmiko
from netmiko import ConnectHandler
from multiprocessing import Process
from testlab_device_list import device_list as devices
import time


def sh_cdp_nei(a_device):
    net_connect = ConnectHandler(**a_device)
    output3a = net_connect.send_command('show version', use_textfsm=True)
    local_host = str(output3a[0].get('hostname'))
    output3=net_connect.send_command('show cdp neig detail', use_textfsm=True)
    print('{:^125}'.format('DEVICES ATTACHED TO ' + local_host +' ARE:'))
    print('{:^125}'.format('-' * 50))
    print('{:<25}{:^25}{:<25}{:<25}{:<25}'.format('destination_host', 'management_ip', 'platform', 'remote_port', 'local_port'))
    d=('*' * 20)
    print('{:<25}{:^25}{:<25}{:<25}{:<25}'.format(d, d, d, d, d))
    for c in output3[0:]:
        print('{:<25}{:^25}{:<25}{:<25}{:<25}'.format(str(c.get('destination_host')), str(c.get('management_ip')), str(c.get('platform')),
                                                          str(c.get('remote_port')), str(c.get('local_port'))))
    print('\n') 
    print('\n') 

def main():
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=sh_cdp_nei, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)
        time.sleep(1)
        
    for a_proc in procs:
#        print(a_proc)
        a_proc.join()
    
    
    
if __name__ == '__main__':
    main()                                        