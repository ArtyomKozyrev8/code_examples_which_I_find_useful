# mian file:

import subprocess
import time
a = subprocess.Popen(args=['python','child2.py', '2','3','4'],stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                     
# a=2, b=3, c=4 - are transfered to child program                    
                    
j=a.communicate() # start subprocess
print(f"Output is {j[0].decode('utf-8')}")
print(j[1].decode('utf-8'))
time.sleep(2)

#child file:

import sys
import time

def main(a,b,c):
    x = int(a)+int(b)+int(c)
    sys.stdout.write(f'The result is {x}')
    time.sleep(3)
     
if __name__ == '__main__':
    a=sys.argv[1]
    b=sys.argv[2]
    c=sys.argv[3]
    main(a,b,c)
