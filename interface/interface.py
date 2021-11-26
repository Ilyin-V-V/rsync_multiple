#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/SyncDataNode/config')
sys.path.append('/root/SyncDataNode/interface')
sys.path.append('/root/SyncDataNode/log')
sys.path.append('/root/SyncDataNode/ssh')
sys.path.append('/root/SyncDataNode/zfs')
sys.path.append('/root/SyncDataNode/rsync')
import config
import logger
import ssh
import zfs
import rsync

class Interface(object):
 def __init__(self):
  self.name='Interface'
  self.nodeActive=[]
  self.folderList=[]
  self.newResource=[]
  self.newDictResource={}

 def find_node_active(self):
  for key,value in config.Config().node_host.items():
   node = ssh.Ssh(config.Config().ssh_user,value,
    config.Config().node_port[key]).ssh_exec('ip addr')
   if node:
    if node.find(config.Config().node_master_ip) == -1:
     self.nodeActive.append(key)
  return self.nodeActive

 def GetFolder(self,nodeActive):
  for key,value in config.Config().node_host.items():
   for node in nodeActive:
    if node == key:
     for data in config.Config().resource:
      list = ssh.Ssh(config.Config().ssh_user,value,
       config.Config().node_port[key]).ssh_exec('ls -1 -d '+data+'/*/')
      if list:
       self.folderList.append(list.split('\n'))
   if len(self.folderList):
    return self.folderList
  return self.folderList

 def SetNewResource(self,folderList,nodeActive):
  for element in folderList:
   for folder in element:
    if folder != '':
     self.newResource.append(folder)
  portion = int(len(self.newResource)) // int(len(nodeActive))
  position = -1; step = portion; col_node = int(len(nodeActive))
  for key,node in enumerate(nodeActive):
   if col_node == 1:
    portion = int(len(self.newResource)) - 1;
    newDictResource,position = Interface().UploadNewResource(
     self.newResource,self.newDictResource,key,node,portion,position)
   else:
     newDictResource,position = Interface().UploadNewResource(
      self.newResource,self.newDictResource,key,node,portion,position)
     portion = position + step; col_node = col_node - 1;
  return newDictResource

 def UploadNewResource(
  self,newResource,newDictResource,key_node,node,portion,position):
  arrTmp=[];
  for key,folder in enumerate(newResource):
   if portion >= key:
    if key > position:
     arrTmp.append(folder)
     if key == portion:
      newDictResource[node] = arrTmp; break;
  return newDictResource,key

 def main(self):
  # Zfs create snapshot
  create,snapshot = zfs.Zfs().zfs_snapshot_create()
  if create == 0:
   logger.Logger().writeLog('Create snapshot '+str(snapshot))
  else: logger.Logger().writeLog('Create snapshot problem '+
   str(snapshot)); logger.Logger().tmp_file('0'); return

  # Zfs destroy snapshot
  remove = zfs.Zfs().zfs_snapshot_destroy()
  if remove == 0:
   logger.Logger().writeLog('Remove snapshot !')
  else: logger.Logger().writeLog('Not found snapshot !')

  # Node active find
  nodeActive = Interface().find_node_active()
  if len(nodeActive):
   logger.Logger().writeLog('Node online '+str(nodeActive))
  else: logger.Logger().writeLog('Node online not found ');
  logger.Logger().tmp_file('0'); return

  # Get folder
  folderList = Interface().GetFolder(nodeActive)
  if len(folderList):
   logger.Logger().writeLog('Get folder count resource '+str(len(folderList)))
  else: logger.Logger().writeLog('Problem get folder ');
  logger.Logger().tmp_file('0'); return

  # Set new resource of node
  newResource = Interface().SetNewResource(folderList,nodeActive)
  if len(newResource):
   logger.Logger().writeLog('New resource set col node '+str(len(newResource)))
  else: logger.Logger().writeLog('Problem set new resource ');
  logger.Logger().tmp_file('0'); return

  # Sync rsync folder
  sync = rsync.Rsync().rsync_process(newResource)
  if sync:
   logger.Logger().writeLog('Sync rsync finish '+str(sync))
   logger.Logger().tmp_file('1'); return
  else:
   logger.Logger().writeLog('Problem sync rsync finish '+str(sync))
   logger.Logger().tmp_file('0'); return

if __name__ == "__main__":
 count_par = len(sys.argv)
 if count_par == 2:
  if sys.argv[1] == 'sync':
   Interface().main()
  else:
   print 'Not parameter for running interface ...'
   print 'Reading Readme !'
 else:
  print 'Not parameter for running interface ...'
  print 'Reading Readme !'
