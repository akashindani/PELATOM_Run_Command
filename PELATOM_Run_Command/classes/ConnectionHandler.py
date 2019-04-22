'''
Created on Jul 24, 2018

@author: akashi
'''
import os

from classes import RemoteAuthenticationService
from classes.fabfile import runCommand,copyFromRemote

class ConnectionHandler():
    def __init__(self,machine_details):
        self.machine_details = machine_details
        self.remote_authentication_service = RemoteAuthenticationService.RemoteAuthenticationService()
        #self.remote_authentication_service.authenticate(self.machine_details, self.pingMachine)
        
    def pingMachine(self, **keyargs):
        print ("### CHECKING IF ABLE TO CONNECT SERVER")
        result = runCommand("hostname", False, **keyargs)
        print (result)
    
    def runCommand(self,command):
        return self.remote_authentication_service.authenticate(self.machine_details, self.run_on_remote,command)
        
    
    def run_on_remote(self,command, **keyargs):
        result = runCommand(command, False, **keyargs)
        return str(result.stdout).strip()

    def downloadFile(self,file_with_path):
        return self.remote_authentication_service.authenticate(self.machine_details, self.download_from_remote,file_with_path)
        
    
    def download_from_remote(self,file_with_path, **keyargs):
        if not os.path.exists("temp"):
            os.mkdir("temp")
        result = copyFromRemote(file_with_path, "temp"+"/"+os.path.basename(file_with_path), **keyargs)
        return "temp"+"/"+os.path.basename(file_with_path)