'''
Created on Jul 24, 2018

@author: akashi
'''
import os
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures._base import TimeoutError
from invoke import UnexpectedExit
default_timeout = 60


# DEFINE A DUMMY EXCEPTION
class FabricException(Exception):
    print (str(Exception))
    pass


def exceptionHandler(f):
    '''
        General description:This method handles the exception.
        Args:
        param1:f
        Returns:none

    '''
    def newFunction(*args, **kw):
        try:
            result = f(*args, **kw)  # VALUES SHOULD BE NEVER RETURND AS STRING
            if result:
                return result
        except (Exception, ValueError) as e:  # catch *all* exceptions
            print ('CustomExceptionHandler handled exception %s' % e)
            traceback.print_exc()
            status_message = str(e)
            status_message = status_message.replace("'", "")
            status_message = status_message.replace('"', "")
            raise Exception(status_message)
        except FabricException as e:
            raise Exception(
                "Fabric exception was received while perform given task")
        except SystemExit as e:
            raise Exception("SystemExit was received while perform given task")
    return newFunction

def handleResult(result):
    result.stdout = result.stdout.encode('ascii', 'ignore').decode('ascii')
    result.stderr = result.stderr.encode('ascii', 'ignore').decode('ascii')
    return result


def handlemessage(message):
    return message.encode('ascii', 'ignore').decode('ascii')


@exceptionHandler
def runCommand(command, warn=False, timeout=default_timeout, **kwargs):
    connect = kwargs['connect']
    command = command.strip()
    shell = kwargs.get("shell_type", "/bin/bash")
    connect.connect_timeout = timeout
    try:
        print ("fabric2:runCommand: '" + str(shell) + " " + str(command) + "' is being executed on: "\
                                 + str(connect.user) + "@" + str(connect.host) + ":" + str(connect.port))
        
        with ThreadPoolExecutor(1) as p:
            f = p.submit(connect.run,str(command), warn=warn, shell=shell)
            return handleResult(f.result(timeout=timeout))
    except TimeoutError as e:
        print ('Error :' + "Command timed out maximum wait time :"+str(timeout)+" sec")
        raise ValueError("Command timed out maximum wait time :"+str(timeout)+" sec")
    except UnexpectedExit as e:
        if hasattr(e.result, 'stderr') and e.result.stderr:
            print ('Error :' + str(handlemessage(e.result.stderr)))
            raise ValueError(str(handlemessage(e.result.stderr)))
        if hasattr(e.result, 'stdout') and e.result.stdout:
            print ('Error :' + str(handlemessage(e.result.stdout)))
            raise ValueError(str(handlemessage(e.result.stdout)))
        print ('Error :' + str(e.result))
        raise ValueError(str(e.result))
    except Exception as e:
        if hasattr(e, 'message') and e.message:
            e.message = handlemessage(e.message)
            raise ValueError(str(e.message))
        elif hasattr(e, 'strerror') and e.strerror:
            e.strerror = handlemessage(e.strerror)
            raise ValueError(str(e.strerror))
        else:
            raise ValueError(str(e))
    finally:
        try:
            connect.close()
        except Exception:
            pass
        

@exceptionHandler
def createFolder(folder, **kwargs):
    try:
        print ('Trying to create dir : ' + str(folder))
        result = runCommand('mkdir -p -m 777 ' + folder,
                            warn=True, timeout=default_timeout, **kwargs)
        print ('Dir : ' + str(folder) + ' was created')
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def move(fromDir, toDir, filename="", **kwargs):
    try:
        print ('Trying to move to dir : ' + str(toDir) + " from: " + str(fromDir))
        result = runCommand("cd {}; mkdir -p ".format(fromDir) + toDir + " ; mv -f " +
                            filename + " " + toDir + "/ 2>/dev/null", warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def copy_dir_to_remote(RequestId, From, To, current_path, **kwargs):
    connect = kwargs['connect']
    connect.connect_timeout = default_timeout
    # handle folder copy for fabric2
    assert os.path.isdir(
        From) == True, "the path you provided is not a directory"
    for root, dirs, files in os.walk(From, topdown=True):
        for name in dirs:
            print ("create dir")
            print (os.path.join(root, name).replace(current_path, To).replace('\\', '/'))
            runCommand('mkdir -p ' + os.path.join(root, name).replace(current_path,
                                                                      To).replace('\\', '/'), warn=True, timeout=default_timeout, **kwargs)
        for name in files:
            connect.put(os.path.join(root, name), os.path.join(root, name).replace(
                current_path, To).replace('\\', '/'), preserve_mode=False)
        runCommand('chmod -R +x {}'.format(To + '/' +
                                                   RequestId), warn=True, timeout=default_timeout, **kwargs)


@exceptionHandler
def getSize(RequestId, To, **kwargs):
    try:
        result = runCommand("du -sk {} | cut -f1".format(To +
                                                               '/' + RequestId), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def copyDirectorywithNewName(From, To, **kwargs):
    try:
        print ('copyDirectorywithNewName : ' + str(To))
        result = runCommand('cp -R ' + str(From) + "/ " +
                            str(To) + "/", warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def PingMachine(machineDetails, **kwargs):
    try:
        result = runCommand("hostname", True, 10, **kwargs)
        if result.return_code != 0:
            raise Exception(
                "Unable to connect machine with host:" + machineDetails["host"])
    except Exception as e:  # catch *all* exceptions
        raise Exception("Unable to connect machine with host:" +
                        machineDetails["host"] + " Error:" + str(e))

@exceptionHandler
def copyToRemote(source, remote, **kwargs):
    connect = kwargs['connect']
    try:
        if os.path.isdir(source):
            for root, dirs, files in os.walk(source, topdown=True):
                for name in dirs:
                    print ("create dir")
                    print (os.path.join(root, name).replace(source, remote).replace('\\', '/'))
                    connect.run('mkdir -p ' + os.path.join(root,
                                                           name).replace(source, remote).replace('\\', '/'))
                for name in files:
                    print ("*** bulk copy file from :" + str(os.path.join(root, name)) + " to " + str(os.path.join(root, name).replace(source, remote).replace('\\', '/')))
                    try:
                        connect.put(os.path.join(root, name), os.path.join(root, name).replace(source, remote).replace('\\', '/'),
                                    preserve_mode=False)
                    except Exception as e:  # catch *all* exceptions
                        print ("Failed to copy with error: " + str(e))
        else:
            splited_source = source.replace('\\', '/').rsplit('/', 1)
            file_name = splited_source[1]
            splited_remote = remote.replace('\\', '/').rsplit('/', 1)
            remote_path_without_file_name = splited_remote[0]
            if '.' in remote:
                connect.run('mkdir -p ' + remote_path_without_file_name)
                return connect.put(source, remote)
            else:
                connect.run('mkdir -p ' + remote)
                return connect.put(source, remote + '/' + file_name)
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def copyFromRemote(remote, target, **kwargs):
    try:
        connect = kwargs['connect']
        result = connect.get(remote, target)
        return result        
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def unzip(file_name, **kwargs):
    try:
        result = runCommand('unzip -u ' + file_name,
                            warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def zip(zip_name, files_list, **kwargs):
    try:
        result = runCommand(' zip -9 ' + zip_name +
                            ' '.join(files_list), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def deleteFile(file_name, **kwargs):
    try:
        result = runCommand('rm -f ' + file_name, warn=True,
                            timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def deleteFolder(folder, **kwargs):
    try:
        result = runCommand('rm -r -f ' + folder, warn=True,
                            timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def replaceTextInFile(fileName, oldText, newText, **kwargs):
    try:
        print ("FileName: " + str(fileName))
        print ("oldText: " + str(oldText).replace('/', '\/'))
        print ("newText: " + str(newText).replace('/', '\/'))
        result = runCommand("sed -i 's/" + str(oldText).replace('/', '\/') + "/" + str(
            newText).replace('/', '\/') + "/g' {}".format(fileName), warn=True, timeout=default_timeout, **kwargs)
        if result.return_code != 0:
            raise ValueError(result.stdout)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))


@exceptionHandler
def grantFolderPermissions(perm, folder, **kwargs):
    try:
        result = runCommand('chmod -R ' + str(perm) + ' ' +
                            folder, warn=True, timeout=default_timeout, **kwargs)
        return result
    except Exception as e:  # catch *all* exceptions
        print ('Error :' + str(e))
        raise ValueError(str(e))