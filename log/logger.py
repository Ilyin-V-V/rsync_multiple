#!/usr/bin/env python
from datetime import datetime
import sys
sys.path.append('../config/')
import config

class Logger():
 def __init__(self):
  self.name='Logger'
  self.process='(SyncNode)'
  self.date=datetime.strftime(datetime.now(),"%d:%m:%Y-%H:%M:%S")

 def writeLog(self,data):
  file_path=config.Config().log
  file=open(file_path, 'a')
  messages=self.date+" | "+self.process+" | "+data
  file.write(messages +"\n")
  file.close()

 def tmp_file(self,data):
  file = open(config.Config().tmp, 'w')
  file.write(str(data) +"\n")
  file.close()
