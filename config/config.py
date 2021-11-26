#!/usr/bin/env python
####################################
# Description: Copy resource rsync #
# Mantainer: Ilyin.V.V	           #
# Date: 09.11.2020                 #
####################################

class Config:
 def __init__(self):

# Patch dir, log name
  self.path='/root/SyncDataNode/'
  self.log_path='/var/log/SyncNode/'
  self.log='/var/log/SyncNode/SyncNode.log'
  self.tmp='/etc/zabbix/scripts/sync.tmp'

# Variable connect
  self.host='rsync'
  self.ssh_user='root'
  self.ssh_port='22'

# Node list
  self.node_host={'node1':'host-01.domain.ru',
                  'node2':'host-02.domain.ru',
                  'node3':'host-03.domain.ru'}
  self.node_port={'node1':'22',
                  'node2':'22',
                  'node3':'22'}
# Master node ip
  self.node_master_ip='172.30.0.225'

# Resource list
  self.resource=['/homes']

# Zfs name pool
  self.pool='data'

# Zfs snapshot remove day
# Not more 30 day
  self.rem_day=7

# Count process rsync parallely
  self.process_rsync=8
