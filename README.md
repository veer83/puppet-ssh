#!/bin/sh
#
# filebeat        Startup script for filebeat
#
# chkconfig: - 85 15
# processname: filebeat
# config: /etc/filebeat/filebeat.yml
# pidfile: /var/run/filebeat.pid
# description: Filebeat is the next-generation Logstash Forwarder designed to quickly and reliably ship log file data to Logstash or Elasticsearch while only consuming a fraction of the resources.
#
### BEGIN INIT INFO
# Provides: filebeat
# Required-Start: $local_fs $remote_fs $network
# Required-Stop: $local_fs $remote_fs $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: start and stop filebeat
### END INIT INFO

NAME=filebeat
FILEBEAT_USER=filebeat
FILEBEAT_HOME="/usr"
FILEBEAT_CONFIG="/etc/filebeat/filebeat.yml"

filebeat_pid() {
    echo `ps aux | grep filebeat | grep -v grep | awk '{ print $2 }'`
}

start() {
  # Start filebeat
  echo "Starting Filebeat"
  /bin/su - -c "cd $FILEBEAT_HOME/bin && $FILEBEAT_HOME/bin/filebeat -c $FILEBEAT_CONFIG > /dev/null 2>&1 &" $FILEBEAT_USER
  return 0
}

stop() {
  pid=$(filebeat_pid)
  echo "Shutting down Filebeat"
  kill -9 $pid
  return 0
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
       pid=$(filebeat_pid)
        if [ -n "$pid" ]
        then
           echo "Filebeat is running with pid: $pid"
        else
           echo "Filebeat is not running"
        fi
        ;;
    *)
        echo $"Usage: $NAME {start|stop|restart|status}"
esac

exit 0


----------------------------------------------


#!/bin/sh
#
# filebeat        Startup script for filebeat
#
# chkconfig: - 85 15
# processname: filebeat
# config: /etc/filebeat/filebeat.yml
# pidfile: /var/run/filebeat.pid
# description: Filebeat is the next-generation Logstash Forwarder designed to quickly and reliably ship log file data to Logstash or Elasticsearch while only consuming a fraction of the resources.
#
### BEGIN INIT INFO
# Provides: filebeat
# Required-Start: $local_fs $remote_fs $network
# Required-Stop: $local_fs $remote_fs $network
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: start and stop filebeat
### END INIT INFO

NAME=filebeat
FILEBEAT_USER=filebeat
FILEBEAT_HOME="/usr"
FILEBEAT_CONFIG="/etc/filebeat/filebeat.yml"

filebeat_pid() {
    echo `ps aux | grep filebeat | grep -v grep | awk '{ print $2 }'`
}

start() {
  # Start filebeat
  echo "Starting Filebeat"
  /bin/su - -c "cd $FILEBEAT_HOME/bin && $FILEBEAT_HOME/bin/filebeat -c $FILEBEAT_CONFIG > /dev/null 2>&1 &" $FILEBEAT_USER
  return 0
}

stop() {
  pid=$(filebeat_pid)
  echo "Shutting down Filebeat"
  kill -9 $pid
  return 0
}

case $1 in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    status)
       pid=$(filebeat_pid)
        if [ -n "$pid" ]
        then
           echo "Filebeat is running with pid: $pid"
        else
           echo "Filebeat is not running"
        fi
        ;;
    *)
        echo $"Usage: $NAME {start|stop|restart|status}"
esac

exit 0

==========================
#!/bin/bash
#
# filebeat:          Startup script for Filebeat Log Shipper.
#
# chkconfig: 3 80 05
# description:      Startup script for Filebeat Log Shipper standalone

FILEBEAT_HOME=/root;
export FILEBEAT_HOME

start() {
       echo -n "Starting Filebeat: "
       echo "Starting Filebeat at `date`" >> $FILEBEAT_HOME/startup.log
       /usr/share/filebeat/bin/filebeat \
      -path.home /usr/share/filebeat \
      -path.config /etc/filebeat \
      -path.data /var/lib/filebeat \
      -path.logs /var/log/filebeat -e &
       sleep 2
       echo "done"
}

stop() {
       echo -n "Stopping Filebeat: "
       echo "Stopping Filebeat at `date`" >> $FILEBEAT_HOME/startup.log
       su $FILEBEAT_OWNER -c "pkill filebeat"
       echo "done"
}

# See how we were called.
case "$1" in
       start)
               start
               ;;
       stop)
               stop
               ;;
       restart)
               stop
               start
               ;;
       status)
               if pgrep -fl "/usr/share/filebeat/bin/filebeat" > /dev/null;then echo running;else echo not running;fi
               ;;
       *)
               echo $"Usage: filebeat {start|stop|restart}"
               exit
esac




