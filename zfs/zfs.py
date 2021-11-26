#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
import commands
import sys
import os
import re
sys.path.append('../logger/')
sys.path.append('../config/')
import logger
import config

class Zfs():
 def __init__(self):
  self.name="ZfsExec"
  self.date=datetime.strftime(datetime.now(),"%Y-%m-%d-%H-%M")
  self.zfs="/sbin/zfs"

 def zfs_snapshot_create(self):
  snapshot = os.system(self.zfs+' snapshot '+
   config.Config().pool+'@'+self.date)
  return snapshot,config.Config().pool+'@'+self.date

 def zfs_find_snapshot_old(self):
  list_snap = commands.getoutput(self.zfs+' list -t snapshot')
  list_snap = re.findall('data@\d*-\d*-\d*-\d*-\d\d',list_snap)
  d_point,day,old_day,metka,col = 0,0,0,0,0
  if len(list_snap):
   for snap in enumerate(reversed(list_snap)):
    if snap[0] == 0:
     point = snap[1].split('-')
     d_point = point[2]
    if snap[0] > 0:
     name = snap[1].split('-')
     day = name[2]
     if d_point != day:
      if old_day != day:
       col = col + 1;
       if col == config.Config().rem_day:
        metka = snap[1]
     old_day = day
   return metka,list_snap
  return False

 def zfs_snapshot_destroy(self):
  metka,list_snap = Zfs().zfs_find_snapshot_old();
  removeArr=[]; rem = False; rem_snap = 0;
  if metka:
   if len(list_snap):
    for snap in enumerate(reversed(list_snap)):
     if snap[1] == metka:
      rem = True
     if rem:
      removeArr.append(snap[1])
    for snap in enumerate(reversed(removeArr)):
     rem_snap = os.system(self.zfs+' destroy '+str(snap[1]))
     logger.Logger().writeLog('Remove snapshot '+str(snap[1]))
    return rem_snap
  return False
