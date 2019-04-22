'''
Created on Jul 24, 2018

@author: akashi
'''
import paramiko
from filelock import FileLock
import os, sys

with FileLock("sshclient_number.txt"):
    print ("Lock acquired")
    fd = os.open("sshclient_number.txt",os.O_RDWR)
    ret = str(os.read(fd,12).decode('utf-8').strip())
    print(ret)
    ret=ret+1
    print (ret)
    os.close(fd)
    #number=f.readlines()
    #print(f)

#ssh[ret] = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#ssh.connect('vptestind01', username='akash', password='akash')
#cmd=('ls')
#stdin, stdout, stderr = ssh.exec_command(cmd)

#print(stdout.read())

