#!/usr/bin/env
from netmiko import Netmiko
from netmiko import ConnectHandler
from multiprocessing import Process
from datetime import datetime
from testlab_device_list import device_list as devices
start_time = datetime.now()


    
    
def show_cdp_nei(a_device):
    
    net_connect = ConnectHandler(**a_device)
    output1 = net_connect.send_command('show version', use_textfsm=True)
    output2= net_connect.send_command_timing('show int status', use_textfsm=True)
    output3a = net_connect.send_command_timing('show version', use_textfsm=True)
    local_host = str(output3a[0].get('hostname')) 
    output3=net_connect.send_command_timing('show cdp neig detail', use_textfsm=True)
    e=('*' * 14)
    d=('*' * 20)
    file = open('netmiko_test1', 'a')
    output = ('{:^41}{:^42}{:^42}'.format('IOS VERSION', 'HOSTNAME', 'MODEL#'))#could add uptime
    file.write(output + '\n')
    output = ('{:^41}{:^42}{:^42}'.format(e, e, e))
    file.write(output + '\n')
    output = ('{:^41}{:^42}{:^42}'.format(str(output1[0].get('version')), str(output1[0].get('hostname')), str(output1[0].get('hardware'))))
    file.write(output + '\n')
    output = ('{:^41}{:^42}{:^42}'.format(e, e, e))
    file.write(output + '\n')
    output = ('\n')
    file.write(output + '\n')
    output = ('{:^125}'.format('DEVICES ATTACHED TO ' + local_host +' ARE:'))
    file.write(output + '\n')
    output = ('{:^125}'.format('---------------------'))
    file.write(output + '\n')
    output = ('{:<25}{:^25}{:<25}{:<25}{:<25}'.format('destination_host', 'management_ip', 'platform', 'remote_port', 'local_port'))
    file.write(output + '\n')
    output = ('{:<25}{:^25}{:<25}{:<25}{:<25}'.format(d, d, d, d, d))
    file.write(output + '\n')
    for c in output3[0:]:
        output = ('{:<25}{:^25}{:<25}{:<25}{:<25}'.format(str(c.get('destination_host')), str(c.get('management_ip')), str(c.get('platform')),
                                                          str(c.get('remote_port')), str(c.get('local_port'))))
        file.write(output + '\n')
    output = ('')
    file.write(output + '\n')    
    output = ('{:<11}{:<11}{:^11}{:<11}{:<11}{:<11}'.format('PORT', 'STATUS', 'VLAN', 'DUPLEX', 'SPEED', 'TYPE'))
    file.write(output + '\n')
    output = ('*' * 75)
    file.write(output + '\n')
    for k in output2[0:28]:
        output = ('{:<12}{:<12}{:^11}{:<12}{:<12}{:>12}'.format(str(k.get('port')), str(k.get('status')), str(k.get('vlan')),
                                                             str(k.get('duplex')), str(k.get('speed')), str(k.get('type'))))
        file.write(output + '\n')
    output = ('-' * 125)
    file.write(output + '\n')
    output = ('\n\n')
    file.write(output + '\n')
    file.close()
    
def main():
    
    procs = []
    for a_device in devices:
        my_proc = Process(target=show_cdp_nei, args=(a_device,))
        my_proc.start()
        procs.append(my_proc)
        
    for a_proc in procs:
        print(a_proc)
        a_proc.join()


    print(datetime.now() - start_time)

if __name__ == '__main__':
    main()                                                              