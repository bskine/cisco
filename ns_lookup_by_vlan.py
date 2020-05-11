import subprocess
import socket
from datetime import datetime
import pprint

start_time = datetime.now()
switches_responding = []
x = []
dns_issues = []
foo = []
date = start_time.strftime('%m_%d_%y')
vlan = str(input('What Vlan would you like to check?\n\n'))


# Gathers all ip's in subnet into list 'x'
for last_octet in range(2, 255):
    address = "10.27." + vlan + "." + str(last_octet)
    x.append(address)

# Pings each ip in list 'x', if there is a reply.... puts into list 'switches_responding'
for i in x:
    ping_command = ("ping -n 2 -w 10 " + str(i))
    result = subprocess.Popen(ping_command, stdout=subprocess.PIPE, shell=True, encoding="utf-8").communicate()[0]
    if "Reply from" in result:
        switches_responding.append(i)

for s in switches_responding:
    try:
        name = socket.gethostbyaddr(s)
        name2 = ' '.join(name[2])
        output = name2 + ' : ' + name[0]
        print(output)
        foo.append(output)
    except Exception:
        print(s, ' : ', 'DNS misconfigured on device')
        dns_issues.append(s)
        continue

with open('Vlan_' + vlan + '   ' + str(date) + '.txt', 'a+') as f:
    f.write('The number of switches responding on Vlan' + vlan + ' is ' + str(len(switches_responding)) + ('\n'*2))
    f.write('\n'.join(foo) + ('\n'*3))
    f.write('The number of witches with dns misconfigurations is ' + str(len(dns_issues)) + ('\n'*2))
    f.write('\n'.join(dns_issues))

elapsed_time = datetime.now() - start_time

print(elapsed_time)

                                  
