'''
Created on Jul 25, 2018

@author: akashi
'''

from classes import ConnectionHandler

class run_commands:
    
    def __init__(self):
        self.machine={
            "username" : "akash",
            "host" : "vptestind01",
            "password" : "akash",
            "type" : "ssh"
        }
    
    def make_connection(self):
        connect_handler = ConnectionHandler.ConnectionHandler(self.machine)
        return connect_handler
    
    def run_unix_commands(self,commands):
        #commands=str(commands).strip()
        #print(commands)
        connect_handler=self.make_connection()
        for line in commands:
            try:
                command=line.strip()
                print ("Input : \n"+ command)
                print ("Output : \n")
                temp=connect_handler.runCommand(command)
                #print ("Input : \n"+ command)
                #print("Output : "+temp)
                #print(command)
            except Exception as e:
                print("Caused by : check if entered unix command is correct")
                #print(str(e))
                break