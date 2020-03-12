#!/bin/sh

#chkconfig: 123456 90 10

# openerp server for user authentication


daemon_start() {
    echo "Server started."
    /usr/bin/kubesds-rpc-service start
}

daemon_stop() {

    pid=`ps -ef | grep '/usr/bin/kubesds-rpc-service start' | awk '{ print $2 }'`

    echo $pid

    kill $pid

    sleep 1

    echo "Server killed."

}

case "$1" in

start)

    daemon_start

    ;;

stop)

    daemon_stop

    ;;

restart)

    daemon_stop

    daemon_start

    ;;

*)

    echo "Usage:  /usr/bin/kubesds-ctl.sh {start|stop|restart}"

    exit 1

esac

exit 0
