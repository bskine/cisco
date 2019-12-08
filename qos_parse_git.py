#! usr/bin/env
import re
line =[]
with open('alp-cr5-confg', 'r') as z:
    for var in z:
        line.append(var)
y = [x for x in line if re.search('(ip access-list e|^\spermit ip )', x)]
for var in y:
    print(var, end='')
print('\n')
h = [x for x in line if re.search('(class-map|^\smatch)', x)]
for foo in h:
    print(foo, end='')
print('\n')
a = [x for x in line if re.search('(^policy-map|class\s[a-z]|^\s+shape average)', x)]
for bar in a:
    print(bar, end='')

           
        
