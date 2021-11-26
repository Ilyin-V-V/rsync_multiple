#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import commands
import time
sys.path.append('../logger/')
sys.path.append('../config/')
import logger
import config

class Rsync():
 def __init__(self):
  self.name="RsyncExec"
  self.touch="/usr/bin/touch"
  self.rsync="/usr/bin/rsync"
  self.ps="/usr/bin/ps"
  self.grep="/usr/bin/grep"
  self.wc="/usr/bin/wc"
  self.rsync_key="-aAXhP -e"
  self.rsync_param="--numeric-ids "+\
   "--progress --force --delete "+\
   "--delete-excluded --ignore-errors "+\
   "--exclude-from=\'"+config.Config().path+"exclude.txt\' --log-file="

 def rsync_process(self,newResource):
  MaxIteracion = True; i = 0; MaxProcess = True; Sync = False
  while MaxIteracion:
   Rsync().rsync_wait()
   for key,resource in enumerate(newResource):
    try:
     logger.Logger().writeLog('Start rsync process host '+\
      str(config.Config().node_host[resource])+' resource '+\
      newResource[resource][i])
     name = newResource[resource][i].split('/')
     login = len(name); user = name[login-2]
     Rsync().rsync_exec(
      str(config.Config().node_host[resource]),
      newResource[resource][i],user)
    except BaseException:
     MaxIteracion = False
     Sync = True
   i = i + 1
  return Sync

 def rsync_wait(self):
  while True:
   col_process = commands.getoutput(self.ps+' -ax | '+\
     self.grep+' '+self.rsync+' | '+\
     self.grep+' -v '+self.grep+' | '+self.wc+' -l')
   if int(col_process) >= int(config.Config().process_rsync):
    logger.Logger().writeLog('Wait col process '+str(col_process))
    time.sleep(2)
   else:
    return

 def rsync_exec(self,node,folder,user):
  command = self.rsync+' '+self.rsync_key+\
   ' "ssh -p '+config.Config().ssh_port+'\" '+\
   self.rsync_param+config.Config().log_path+user+\
   ' '+config.Config().ssh_user+'@'+node+':'+\
   folder+' '+folder
  subprocess.Popen(command,shell=True)
