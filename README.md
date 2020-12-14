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




