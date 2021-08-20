# kubeOVN
SDN for Kubernetes network

## authors:

- wuheng@otcaix.iscas.ac.cn
- wuyuewen@otcaix.iscas.ac.cn

# 1. Features

- **IPv4**/IPv6
- **vlan**, **geneve**, vxlan, 
- **fixed IP/floating IP**
- **static IP/dynamic IP**
- **ACL**
- **QoS**
- CNI

# 2. Roadmap

- Support geneve/IPv4 [1.x]
  - ~~support vlan [1.1.0]~~
  - ~~support floating ip [1.2.0]~~
  - ~~upport ACL [1.3.0]~~
  - ~~support QoS [1.4.0]~~
  - production ready [1.5.0]
- Support vxlan [2.x]
- Support CNI [3.x]
- Support IPv6 [4.x]

# 3. Info

```
Notes to self: Clustering seems to be doable in OVS > 2.9 (>2.10 preferred). A working example can be seen here:

northd01 (master) == 172.21.239.73
northd02 == 172.21.238.6
northd03 == 172.21.238.240

## Primary
/usr/share/openvswitch/scripts/ovn-ctl --db-nb-addr=172.21.239.73 \
--db-nb-create-insecure-remote=yes \
--db-sb-addr=172.21.239.73 \
--db-sb-create-insecure-remote=yes \
--db-nb-cluster-local-addr=172.21.239.73 \
--db-sb-cluster-local-addr=172.21.239.73 \
--ovn-northd-nb-db=tcp:172.21.239.73:6641,tcp:172.21.238.6:6641,tcp:172.21.238.240:6641 \
--ovn-northd-sb-db=tcp:172.21.239.73:6642,tcp:172.21.238.6:6642,tcp:172.21.238.240:6642 \
start_northd

Starting OVN ovsdb-servers and ovn-northd on the node with IP y.y.y.y and joining the cluster started at x.x.x.x

#infra2
/usr/share/openvswitch/scripts/ovn-ctl --db-nb-addr=172.21.238.6 \
--db-nb-create-insecure-remote=yes \
--db-sb-addr=172.21.238.6 \
--db-sb-create-insecure-remote=yes \
--db-nb-cluster-local-addr=172.21.238.6 \
--db-sb-cluster-local-addr=172.21.238.6 \
--db-nb-cluster-remote-addr=172.21.239.73 \
--db-sb-cluster-remote-addr=172.21.239.73 \
--ovn-northd-nb-db=tcp:172.21.239.73:6641,tcp:172.21.238.6:6641,tcp:172.21.238.240:6641 \
--ovn-northd-sb-db=tcp:172.21.239.73:6642,tcp:172.21.238.6:6642,tcp:172.21.238.240:6642 \
start_northd

Starting OVN ovsdb-servers and ovn-northd on the node with IP z.z.z.z and joining the cluster started at x.x.x.x

/usr/share/openvswitch/scripts/ovn-ctl --db-nb-addr=172.21.238.240 \
--db-nb-create-insecure-remote=yes \
--db-nb-cluster-local-addr=172.21.238.240 \
--db-sb-addr=172.21.238.240 \
--db-sb-create-insecure-remote=yes \
--db-sb-cluster-local-addr=172.21.238.240 \
--db-nb-cluster-remote-addr=172.21.239.73 \
--db-sb-cluster-remote-addr=172.21.239.73 \
--ovn-northd-nb-db=tcp:172.21.239.73:6641,tcp:172.21.238.6:6641,tcp:172.21.238.240:6641 \
--ovn-northd-sb-db=tcp:172.21.239.73:6642,tcp:172.21.238.6:6642,tcp:172.21.238.240:6642 \
start_northd

The trick is verifying when this needs to be implemented and how it behaves with subsequent playbook runs.

See full activity log
```

# Books

- https://feisky.gitbooks.io/sdn/ovs/ovn-internal.html

# 4. References

- Basic:
  - http://blog.spinhirne.com/2016/10/ovn-and-acls.html
  - https://zhaozhanxu.com/2017/02/22/SDN/OVN/2017-02-22-ovn-nbdb/
  - https://developers.redhat.com/blog/2018/09/03/ovn-dynamic-ip-address-management/
  - https://blog.scottlowe.org/2016/12/09/using-ovn-with-kvm-libvirt/
  - http://dani.foroselectronica.es/simple-ovn-setup-in-5-minutes-491/
  - https://www.li-rui.top/2018/12/16/network/ovn%E5%AD%90%E7%BD%91%E4%BB%A5%E5%8F%8A%E4%B8%89%E5%B1%82%E7%BD%91%E5%85%B3/
  - https://hechao.li/2018/05/15/VXLAN-Hands-on-Lab/
  - https://github.com/cao19881125/ovn_lab
  - https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/

- Floating IP:
  - https://segmentfault.com/a/1190000020311817
  - https://www.sdnlab.com/19802.html
  - https://www.cnblogs.com/silvermagic/p/7666124.html

- QoS：
  - https://macauleycheng.gitbooks.io/ovn/qos-dscp-configuration.html

- ACLS:
  - http://blog.spinhirne.com/2016/10/ovn-and-acls.html
  - https://blog.csdn.net/zhengmx100/article/details/75431393

- VxLan
  - https://macauleycheng.gitbooks.io/ovn/examplewith-vtep.html
  - http://docs.openvswitch.org/en/latest/howto/vtep/
  - https://hechao.li/2018/05/15/VXLAN-Hands-on-Lab/
  - https://docs.pica8.com/display/picos2102cg/OVSDB+VTEP+with+vtep-ctl+Configuration+Examples
  
- Debug
  - https://www.twblogs.net/a/5b8118292b71772165aaf9a5
  
 - Bug
   - https://bugzilla.redhat.com/show_bug.cgi?id=1580542
   - https://access.redhat.com/errata/RHBA-2019:3718
