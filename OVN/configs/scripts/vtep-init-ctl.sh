#######################################################
##
##      Copyright(2019, ) Institute of Software
##             Chinese Academy of Sciences
##               Author@wuheng@otcaix.iscas.ac.cn
##
########################################################

function start-vtep()
{
  pid=$(ps aux | grep vtep.db | grep ovsdb-server | grep -v grep | awk '{print$2}')
  if [[ -n $pid ]]
  then
    exit 0
  fi
  
  vtepdb=$(ls /etc/openvswitch/ | grep vtep.db)
  if [[ -z $vtepdb ]]
  then
    ovsdb-tool create /etc/openvswitch/vtep.db /usr/share/openvswitch/vtep.ovsschema
  fi

  ovsdb-server --remote punix:/run/openvswitch/db.sock --remote=db:hardware_vtep,Global,managers /etc/openvswitch/vtep.db
}

function stop-vtep()
{
  pid=$(ps aux | grep vtep.db | grep ovsdb-server | grep -v grep | awk '{print$2}')
  if [[ -n $pid ]]
  then
    kill -9 $pid
  fi  
}

function help()
{
  echo -e "  start-vtep  :Start vtep"
  echo -e "  stop-vtep   :Stop vtep"
}

case $1 in
  "start-vtep")
    start-vtep
    ;;
  "stop-vtep")
    stop-vtep
    ;;
  "--help")
    help
    ;;
  *)
  help
  ;;
esac
