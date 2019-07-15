## Backgroud

In order to describe the XML schemas of libvirt, we design an algorithm based on [libvirt-go-xml](https://github.com/libvirt/libvirt-go-xml) to generate it. 
Please see [libvirt-xml.md](../docs/libvirt-xml.md) and [libvirt-json.md](../docs/libvirt-json.md).

In addition, we find that libvirt-go-xml is still not 'production ready'. So we plan to implement a kubernetes-based VM maangement platform
with [libvirt-python](https://github.com/libvirt/libvirt-python), which is used by [OpenStack](https://www.openstack.org)


## Limitations

- please use https://github.com/syswu/libvirt-go-xml (not official sdk)
- only support basic and List type

## Run


```
/**
 * Copyright (2018, ) Institute of Software, Chinese Academy of Sciences
 */
package main

import (
	"fmt"
	"github.com/kubesys/kubevirt/analyser"
	libvirtxml "github.com/libvirt/libvirt-go-xml"
	"reflect"
)

/**
 * @author wuheng(@otcaix.iscas.ac.cn)
 * @since 2019/4/26
 *
 */

func main() {
	xmlDesc(reflect.TypeOf(libvirtxml.Domain{}), "domain")
	xmlDesc(reflect.TypeOf(libvirtxml.Network{}), "network")
	xmlDesc(reflect.TypeOf(libvirtxml.StoragePool{}), "pool")
	xmlDesc(reflect.TypeOf(libvirtxml.DomainSnapshot{}), "domainsnapshot")
}

func xmlDesc(objType reflect.Type, tag string)  {
	fmt.Println(analyser.Analyse(objType, tag))
}
```
