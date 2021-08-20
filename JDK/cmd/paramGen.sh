############################################
##
## Copyright (2019, ) Institute of Software
##        Chinese Academy of Sciences
##         Author: wuheng@otcaix.iscas.ac.cn
##           Date: 2019-06-17
##
############################################

cmds=$(virsh help | egrep -v "cd|echo|exit|help|pwd|quit|connect" | egrep -v "list|event|allocpages|capabilities|cpu-baseline|cpu-compare|cpu-models|domcapabilities|freecell|freepages|hostname|hypervisor-cpu-baseline|hypervisor-cpu-compare|maxvcpus|node-memory-tune|nodecpumap|nodecpustats|nodeinfo|nodememstats|nodesuspend|sysinfo|uri|iface-begin|iface-commit|iface-rollback|version|domstats" | grep -v "Grouped" |grep -Ev "^$|[#;]" | awk '{print$1}')

rm -rf paramResults

for cmd in $cmds
do
  echo "[virsh "$cmd"]" >> paramResults
  virsh $cmd --help | grep -A 50 "OPTIONS" | grep -v "OPTIONS" | awk '{gsub(/^\s+|\s+$/, "");print}' >> paramResults
done

  echo "[virt-install]" >> paramResults
  virt-install --help | grep "\-\-"  | awk '{gsub(/^\s+|\s+$/, "");print}' >> paramResults
  echo "[virt-clone]" >> paramResults
  virt-clone --help | grep "\-\-" | egrep -v "usage" | awk '{gsub(/^\s+|\s+$/, "");print}' >> paramResults
