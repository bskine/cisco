#!/usr/bin/env
from netmiko import Netmiko
from netmiko import ConnectHandler
from multiprocessing import Process
from testlab_device_list import device_list as devices

def sh_span(a_device):
    
    net_connect = ConnectHandler(**a_device)
    output = net_connect.send_command_timing('show version', use_textfsm=True)
    output1 = net_connect.send_command_timing('sh spann', use_textfsm=True)
    print('-' * 50)
    print('{:^50}'.format('HOSTNAME'))
    print('{:^50}'.format(str(output[0].get('hostname'))))
    print('-' * 50)
    
    for k in output1[0:]:
        if k.get('role') == 'Root':
            z = ('{:^25}{:^25}'.format(str(k.get('role')), str(k.get('interface'))))
            print('{:^25}{:^25}'.format(('*' * 12), ('*' * 12)))
            print(z)
            print('{:^25}{:^25}'.format(('*' * 12), ('*' * 12)))
            print('\n')
            break
    else:
        print('{:^50}'.format('*' * 25))
        print('{:^50}'.format('This switch is the root!!'))
        print('{:^50}'.format('*' * 25))
        print('\n')


def main():
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=sh_span, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)
        
    for a_proc in procs:
#        print(a_proc)
        a_proc.join()


if __name__ == '__main__':
    main()                                            
