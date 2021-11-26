#!/usr/bin/env python
# yum install python-devel
# yum install libffi-devel
# yum install openssl-devel
# yum install python2-bcrypt
# yum install python2-cryptography
# yum install python-paramiko
import sys
sys.path.append('../logger/')
import logger
import paramiko

class Ssh():
 def __init__(self,user,host,port):
  self.name="SshExec"
  self.user=user
  self.host=host
  self.port=port

 def ssh_exec(self,command):
  client=paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  try:
   client.connect(hostname=self.host, username=self.user,
    port=int(self.port), timeout=4, banner_timeout=3)
   stdin,stdout,stderr=client.exec_command(command)
   execData=stdout.read()+stderr.read()
   return execData
  except (paramiko.AuthenticationException,
          paramiko.ssh_exception.NoValidConnectionsError) as e:
          logger.Logger().writeLog('Timeout connect host '+self.host)
  except  paramiko.SSHException as e:
          logger.Logger().writeLog('Logical error ssh connect host '+self.host)
  except (paramiko.ssh_exception.BadHostKeyException,
          paramiko.ssh_exception.BadAuthenticationType) as e:
          logger.Logger().writeLog('Bad key error ssh connect host '+self.host)
  finally:
          client.close()
