- About project:
      Copying files from remote hosts via ssh to multiple streams, using rsync

Files:
 - config / config.py - Config file
   - path - path to the executable program
   - log_path - path to the directory with log files
   - log - the main log file of the program
   - tmp - path to zabbix monitoring file
   - host - name of the host with the program
   - ssh_user - ssh user for working with nodes
   - ssh_port - port for working via ssh with nodes
   - node_host - an array of nodes from which we will copy data
   - node_port - array of node ports
   - node_master_ip - ip of the master, which we do not touch when copying
   - resource - an array of resources to copy
   - pool - zfs pool name
   - rem_day - the number of zfs snapshots to keep
   - process_rsync - number of simultaneous rsync processes
      on the node where the program is running

 - zfs / zfs.py - module for working with zfs
   - zfs_snapshot_create - create a snapshot
   - zfs_find_snapshot_old - search for snapshots older than rem_day
     only on days no more than 30 days
   - zfs_snapshot_destroy - delete snapshots

 - ssh / ssh.py - module for working via ssh

 - rsync / rsync.py - a module for working with rsync
   - rsync_process - creates and monitors new rsync processes to copy data
     without balancing the load on the nodes
   - rsync_wait - controls the number of running rcync processes, parameter - process_rsync
   - rsync_exec - spawns new rsync processes

 - log / logger.py - logging module

 - interface / interface.py - executable file of the program
   - find_node_active - find live nodes
   - GetFolder - getting a list of resource folders
   - SetNewResource - setting a new resource from the GetFolder list
   - UploadNewResource - resource allocation by nodes

 - exclude.txt - exclude rsync

Work logic:
 - Create zfs snapshot
 - Remove zfs snapshots older than rem_day
 - Find active nodes
 - Distribute resources across nodes
 - Run rcync on nodes 

