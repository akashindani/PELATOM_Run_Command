'''
Created on Jul 22, 2018

@author: akashi
'''

from classes import ConnectionHandler

from fabric2 import connection

machine={
            "username" : "akash",
            "host" : "vptestind01",
            "password" : "akash",
            "type" : "ssh"
        }

print (machine)

#session1=gateway_con.open()
#print(session1.is_connected)

#machine_details='akash@vptestind01:22'
command='''ls
           ls abc.csv
        '''
connect_handler = ConnectionHandler.ConnectionHandler(machine)
connect_handler.runCommand(command)

