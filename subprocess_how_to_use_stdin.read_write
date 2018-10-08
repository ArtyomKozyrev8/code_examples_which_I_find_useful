#main file:

import subprocess
import time
a = subprocess.Popen(args=['python','child1.py'],stdout=subprocess.PIPE,
                     stderr=subprocess.PIPE,stdin=subprocess.PIPE)
a.stdin.write('4 '.encode('utf-8'))
a.stdin.write('5 '.encode('utf-8'))
a.stdin.write('7 '.encode('utf-8'))
a.stdin.write('9'.encode('utf-8'))
j=a.communicate() # returns tuple which contains stdout and stderror
print(f"Output is {j[0].decode('utf-8')}") # output of the process
print(j[1].decode('utf-8')) # stderror if any error happened in the process
time.sleep(2)


#child file - subprocess I would like to start

import sys
import time


def main(a,b,c,d):
    x = int(a)+int(b)+int(c)+int(d)
    sys.stdout.write(f'{x}')
    time.sleep(3)
     

if __name__ == '__main__':
    h = sys.stdin.read().split( ) # all income parameters are read as one line, I use ' ' to separate values
    a = h[0]
    b = h[1]
    c = h[2]
    d = h[3]
    main(a,b,c,d)
