/*

 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.utils;

import java.util.regex.Pattern;

import com.github.kubesys.kubernetes.annotations.FieldDescriber;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/3
 *
 */
public class RegExpUtils {

	@FieldDescriber("名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点")
	public final static String NAME_PATTERN = "[a-z0-9-.]{4,100}";
	
	@FieldDescriber("名称是字符串类型，长度是3到12位，只允许数字、小写字母、中划线")
	public final static String BRIDGE_PATTERN = "[a-z0-9-]{3,12}";
	
	@FieldDescriber("名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点")
	public final static String NAME_PATTERN_WITH_COMMA = "[a-z0-9-.,]{4,100}";
	
	@FieldDescriber("名称是字符串类型，长度是3到12位，只允许数字、小写字母、中划线、以及圆点")
	public final static String NIC_PATTERN = "[a-z0-9-.]{3,12}";
	
	@FieldDescriber("UUID是字符串类型，长度是12到36位，只允许数字、小写字母、中划线、以及圆点")
	public final static String UUID_PATTERN = "uuid=[a-z0-9-.]{12,36}";
	
	@FieldDescriber("路径是字符串类型，长度是2到64位，只允许数字、小写字母、中划线、以及圆点")
	public final static String PATH_PATTERN = "(/var/lib/libvirt(/[a-z0-9-.]{2,64})*)|(/mnt/(localfs|usb)(/[a-z0-9-.]{2,64})*)";

	@FieldDescriber("路径是字符串类型，长度是2到64位，只允许数字、小写字母、中划线、以及圆点")
	public final static String LINUX_PATH_PATTERN = "\\/(\\w+\\/?)+";

	@FieldDescriber("名称是字符串类型，长度是6到128位，只允许数字、小写字母、中划线、以及圆点")
	public final static String TARGET_PATTERN = "(" + NAME_PATTERN + ")|(" + PATH_PATTERN + ")";
	
	@FieldDescriber("虚拟化支持的OS版本列表，详情执行osinfo-query os命令查看")
	public final static String OS_PATTERN = "alpinelinux3.5|alpinelinux3.6|alpinelinux3.7|alpinelinux3.8|alt.p8|alt.sisyphus|alt8.0|alt8.1|alt8.2|altlinux1.0|altlinux2.0|altlinux2.2|altlinux2.4|altlinux3.0|altlinux4.0|altlinux4.1|altlinux5.0|altlinux6.0|altlinux7.0|android-x86-8.1|asianux-unknown|asianux4.6|asianux4.7|asianux7.0|asianux7.1|asianux7.2|caasp-unknown|caasp1.0|caasp2.0|caasp3.0|centos6.0|centos6.1|centos6.10|centos6.2|centos6.3|centos6.4|centos6.5|centos6.6|centos6.7|centos6.8|centos6.9|centos7.0|cirros0.3.0|cirros0.3.1|cirros0.3.2|cirros0.3.3|cirros0.3.4|cirros0.3.5|cirros0.4.0|debian1.1|debian1.2|debian1.3|debian2.0|debian2.1|debian2.2|debian3|debian3.1|debian4|debian5|debian6|debian7|debian8|debian9|debiantesting|dragonflybsd1.0|dragonflybsd1.0A|dragonflybsd1.10.0|dragonflybsd1.10.1|dragonflybsd1.12.0|dragonflybsd1.12.1|dragonflybsd1.12.2|dragonflybsd1.2.0|dragonflybsd1.2.1|dragonflybsd1.2.2|dragonflybsd1.2.3|dragonflybsd1.2.4|dragonflybsd1.2.5|dragonflybsd1.2.6|dragonflybsd1.4.0|dragonflybsd1.4.4|dragonflybsd1.6.0|dragonflybsd1.8.0|dragonflybsd1.8.1|dragonflybsd2.0.0|dragonflybsd2.0.1|dragonflybsd2.10.1|dragonflybsd2.2.0|dragonflybsd2.2.1|dragonflybsd2.4.0|dragonflybsd2.4.1|dragonflybsd2.6.1|dragonflybsd2.6.2|dragonflybsd2.6.3|dragonflybsd2.8.2|dragonflybsd3.0.1|dragonflybsd3.2.1|dragonflybsd3.4.1|dragonflybsd3.4.2|dragonflybsd3.4.3|dragonflybsd3.6.0|dragonflybsd3.6.1|dragonflybsd3.6.2|dragonflybsd3.8.0|dragonflybsd3.8.1|dragonflybsd3.8.2|dragonflybsd4.0.0|dragonflybsd4.0.1|dragonflybsd4.2.0|dragonflybsd4.2.1|dragonflybsd4.2.3|dragonflybsd4.2.4|dragonflybsd4.4.1|dragonflybsd4.4.2|dragonflybsd4.4.3|dragonflybsd4.6.0|dragonflybsd4.6.1|dragonflybsd4.6.2|dragonflybsd4.8.0|dragonflybsd4.8.1|dragonflybsd5.0.0|dragonflybsd5.0.1|dragonflybsd5.0.2|dragonflybsd5.2.0|dragonflybsd5.2.1|dragonflybsd5.2.2|dragonflybsd5.4.0|eos3.3|fedora-unknown|fedora1|fedora10|fedora11|fedora12|fedora13|fedora14|fedora15|fedora16|fedora17|fedora18|fedora19|fedora2|fedora20|fedora21|fedora22|fedora23|fedora24|fedora25|fedora26|fedora27|fedora28|fedora29|fedora3|fedora4|fedora5|fedora6|fedora7|fedora8|fedora9|freebsd1.0|freebsd10.0|freebsd10.1|freebsd10.2|freebsd10.3|freebsd10.4|freebsd11.0|freebsd11.1|freebsd11.2|freebsd2.0|freebsd2.0.5|freebsd2.2.8|freebsd2.2.9|freebsd3.0|freebsd3.2|freebsd4.0|freebsd4.1|freebsd4.10|freebsd4.11|freebsd4.2|freebsd4.3|freebsd4.4|freebsd4.5|freebsd4.6|freebsd4.7|freebsd4.8|freebsd4.9|freebsd5.0|freebsd5.1|freebsd5.2|freebsd5.2.1|freebsd5.3|freebsd5.4|freebsd5.5|freebsd6.0|freebsd6.1|freebsd6.2|freebsd6.3|freebsd6.4|freebsd7.0|freebsd7.1|freebsd7.2|freebsd7.3|freebsd7.4|freebsd8.0|freebsd8.1|freebsd8.2|freebsd8.3|freebsd8.4|freebsd9.0|freebsd9.1|freebsd9.2|freebsd9.3|freedos1.2|gnome-continuous-3.10|gnome-continuous-3.12|gnome-continuous-3.14|gnome3.6|gnome3.8|haikunightly|haikur1alpha1|haikur1alpha2|haikur1alpha3|haikur1alpha4.1|macosx10.0|macosx10.1|macosx10.2|macosx10.3|macosx10.4|macosx10.5|macosx10.6|macosx10.7|mageia1|mageia2|mageia3|mageia4|mageia5|mageia6|mandrake10.0|mandrake10.1|mandrake10.2|mandrake5.1|mandrake5.2|mandrake5.3|mandrake6.0|mandrake6.1|mandrake7.0|mandrake7.1|mandrake7.2|mandrake8.0|mandrake8.1|mandrake8.2|mandrake9.0|mandrake9.1|mandrake9.2|mandriva2006.0|mandriva2007|mandriva2007.1|mandriva2008.0|mandriva2008.1|mandriva2009.0|mandriva2009.1|mandriva2010.0|mandriva2010.1|mandriva2010.2|mandriva2011|mbs1.0|mes5|mes5.1|msdos6.22|netbsd0.8|netbsd0.9|netbsd1.0|netbsd1.1|netbsd1.2|netbsd1.3|netbsd1.4|netbsd1.5|netbsd1.6|netbsd2.0|netbsd3.0|netbsd4.0|netbsd5.0|netbsd5.1|netbsd6.0|netbsd6.1|netbsd7.0|netbsd7.1|netbsd7.1.1|netbsd7.1.2|netbsd7.2|netbsd8.0|netware4|netware5|netware6|openbsd4.2|openbsd4.3|openbsd4.4|openbsd4.5|openbsd4.8|openbsd4.9|openbsd5.0|openbsd5.1|openbsd5.2|openbsd5.3|openbsd5.4|openbsd5.5|openbsd5.6|openbsd5.7|openbsd5.8|openbsd5.9|openbsd6.0|openbsd6.1|openbsd6.2|openbsd6.3|opensolaris2009.06|opensuse-factory|opensuse-unknown|opensuse10.2|opensuse10.3|opensuse11.0|opensuse11.1|opensuse11.2|opensuse11.3|opensuse11.4|opensuse12.1|opensuse12.2|opensuse12.3|opensuse13.1|opensuse13.2|opensuse15.0|opensuse42.1|opensuse42.2|opensuse42.3|opensusetumbleweed|popos17.10|popos18.04|popos18.10|rhel-atomic-7.0|rhel-atomic-7.1|rhel-atomic-7.2|rhel-atomic-7.3|rhel-atomic-7.4|rhel-unknown|rhel2.1|rhel2.1.1|rhel2.1.2|rhel2.1.3|rhel2.1.4|rhel2.1.5|rhel2.1.6|rhel2.1.7|rhel3|rhel3.1|rhel3.2|rhel3.3|rhel3.4|rhel3.5|rhel3.6|rhel3.7|rhel3.8|rhel3.9|rhel4.0|rhel4.1|rhel4.2|rhel4.3|rhel4.4|rhel4.5|rhel4.6|rhel4.7|rhel4.8|rhel4.9|rhel5.0|rhel5.1|rhel5.10|rhel5.11|rhel5.2|rhel5.3|rhel5.4|rhel5.5|rhel5.6|rhel5.7|rhel5.8|rhel5.9|rhel6-unknown|rhel6.0|rhel6.1|rhel6.10|rhel6.2|rhel6.3|rhel6.4|rhel6.5|rhel6.6|rhel6.7|rhel6.8|rhel6.9|rhel7-unknown|rhel7.0|rhel7.1|rhel7.2|rhel7.3|rhel7.4|rhel7.5|rhel7.6|rhel8-unknown|rhel8.0|rhl1.0|rhl1.1|rhl2.0|rhl2.1|rhl3.0.3|rhl4.0|rhl4.1|rhl4.2|rhl5.0|rhl5.1|rhl5.2|rhl6.0|rhl6.1|rhl6.2|rhl7|rhl7.1|rhl7.2|rhl7.3|rhl8.0|rhl9|silverblue28|silverblue29|sle-unknown|sle15|sle15-unknown|sled10|sled10sp1|sled10sp2|sled10sp3|sled10sp4|sled11|sled11sp1|sled11sp2|sled11sp3|sled11sp4|sled12|sled12-unknown|sled12sp1|sled12sp2|sled12sp3|sled9|sles10|sles10sp1|sles10sp2|sles10sp3|sles10sp4|sles11|sles11sp1|sles11sp2|sles11sp3|sles11sp4|sles12|sles12-unknown|sles12sp1|sles12sp2|sles12sp3|sles9|solaris10|solaris11|solaris9|ubuntu10.04|ubuntu10.10|ubuntu11.04|ubuntu11.10|ubuntu12.04|ubuntu12.10|ubuntu13.04|ubuntu13.10|ubuntu14.04|ubuntu14.10|ubuntu15.04|ubuntu15.10|ubuntu16.04|ubuntu16.10|ubuntu17.04|ubuntu17.10|ubuntu18.04|ubuntu18.10|ubuntu19.04|ubuntu4.10|ubuntu5.04|ubuntu5.10|ubuntu6.06|ubuntu6.10|ubuntu7.04|ubuntu7.10|ubuntu8.04|ubuntu8.10|ubuntu9.04|ubuntu9.10|win1.0|win10|win2.0|win2.1|win2k|win2k12|win2k12r2|win2k16|win2k3|win2k3r2|win2k8|win2k8r2|win3.1|win7|win8|win8.1|win95|win98|winme|winnt3.1|winnt3.5|winnt3.51|winnt4.0|winvista|winxp";
	
	@FieldDescriber("mac地址但不能以fe开头，只支持小写字母和数字")
	public final static String MAC_PATTERN  = "(([a-eg-z0-9][a-z0-9])|(f[a-df-z0-9]))(:[a-z0-9]{2}){5}";
	
	@FieldDescriber("vcpu个数，1到100之间")
	public final static String VCPU_PATTERN = "[1-9](\\d{1})?";
	
	@FieldDescriber("vlan ID号，0到4094之间")
	public final static String VLAN_PATTERN = "\\d{1,3}|[1-3][0-9][0-9][0-9]|40[0-8][0-9]|409[0-4]";
	
	@FieldDescriber("ram容量，单位MiB，100到99999之间")
	public final static String RAM_MiB_PATTERN = "\\d{3,5}(,maxmemory=\\d{3,5})?";
	
	@FieldDescriber("ram容量，单位KiB，100到99999之间")
	public final static String RAM_KiB_PATTERN = "\\d{6,8}";
	
	@FieldDescriber("MTU，100到10000之间")
	public final static String MTU_PATTERN = "\\d{2,4}";

	@FieldDescriber("存储池自动打开的参数，只能是yes和no之一")
	public final static String AUTOSTART_PATTERN = "yes|no";
	
	@FieldDescriber("磁盘类型，只能是raw，bochs，qcow，qcow2，vmdk，qed之一")
	public final static String DISK_SUBDRIVER_PATTERN = "raw|bochs|qcow|qcow2|vmdk|qed";
	
	@FieldDescriber("磁盘类型，只能是disk，lun，cdrom，floppy之一")
	public final static String DISK_TYPE_PATTERN = "disk|lun|cdrom|floppy";
	
	@FieldDescriber("磁盘类型，只能是ide，scsi，virtio，xen，usb，sata，sd之一")
	public final static String DISK_BUS_PATTERN = "ide|scsi|virtio|xen|usb|sata|sd";
	
	@FieldDescriber("磁盘SCSI设备IO模式，只能是unfiltered， filtered之一")
	public final static String DISK_SGIO_PATTERN = "unfiltered|filtered";
	
	@FieldDescriber("磁盘缓存类型，只能是none, writethrough, directsync, unsafe, writeback之一")
	public final static String DISK_CACHE_PATTERN = "none|writethrough|directsync|unsafe|writeback";

	@FieldDescriber("盘符名称，只能是vd[x]，hd[x]，sd[x]之一")
	public final static String FDISK_TYPE_PATTERN = "vd[a-z]|hd[a-z]|sd[a-z]";
	
	@FieldDescriber("磁盘读写类型，只能是readonly, shareable之一")
	public final static String DISK_MODE_PATTERN = "readonly|shareable";
	
	@FieldDescriber("磁盘源类型，只能是file, block之一")
	public final static String DISK_SOURCE_TYPE_PATTERN = "file|block";
	
	@FieldDescriber("磁盘驱动，只能是qemu, tap之一")
	public final static String DISK_DRIVER_PATTERN = "qemu|tap";
	
	@FieldDescriber("磁盘QoS，单位是字节，取值范围0-9999999999")
	public final static String DISK_QoS_PATTERN = "\\d{1,10}";
	
	@FieldDescriber("网络QoS，单位是KiB，取值范围0-99999999")
	public final static String NET_QoS_PATTERN = "\\d{1,8}";
	
	@FieldDescriber("磁盘IOPS，取值范围0-9999")
	public final static String DISK_IOPS_PATTERN = "\\d{1,5}";

	@FieldDescriber("名称是字符串类型，长度是4到100位，只允许数字、小写字母")
	public final static String POOL_PATH= "[a-z0-9]{4,100}";

	@FieldDescriber("名称是字符串类型，长度是4到100位，只允许数字、小写字母")
	public final static String POOL_UUID= "[a-z0-9]{4,100}";
	
	@FieldDescriber("磁盘大小，单位是Bytes，取值范围1000000000-999999999999")
	public final static String DISK_SIZE_PATTERN = "\\d{10,13}";

	@FieldDescriber("磁盘大小，单位是KiB，取值范围1000000-999999999999")
	public final static String DISK_SIZE_KIB_PATTERN = "\\d{7,13}";
	
	@FieldDescriber("USB透传的操作类型，只能是add, remove之一")
	public final static String DEVICE_PASSTHROUGH_ACTION = "add|remove";
	
	@FieldDescriber("USB透传的操作类型，只能是add, remove之一")
	public final static String DEVICE_PASSTHROUGH_DEV_TYPE = "usb|pci";
	
	@FieldDescriber("USB重定向的操作类型，只能是on, off之一")
	public final static String USB_REDIRECT_ACTION = "on|off";
	
	@FieldDescriber("模拟的USB个数，1到8之间")
	public final static String USB_REDIRECT_NUMBER = "[1-8]";
	
	@FieldDescriber("虚拟机网卡模式")
	public final static String NETWORK_MODEL_PATTERN = "(e1000|virtio|rtl8139)";
	
//	1 单独限制协议
//	tcp
//	2 限制协议和端口
//	tcp.src == 22
//	3 限制单个ip
//	ip4.src == 192.168.1.100
//	4 限制一组ip
//	ip4.src == { 192.168.1.100,192.168.1.102 }
//	5 限制cidr
//	ip4.src == 192.168.1.0/24
//	6 使用ovn中的address_set 的名字代表一组ip列表，比如dmz
//	ip4.src == $dmz
//	7 限制端口范围
//	1024 <= tcp.src <= 49151 等价于 1024 <= tcp.src && tcp.src <= 49151
//	8 组合不同的规则之间使用 && 表示 and ，|| 表示 or ，同时可以加（）
//	比如限制访问tcp 22-100 端口，源地址为address_set dmz 或者cidr 192.168.1.0/24
//	规则的写法为
//	 22 <= tcp.src <= 100 && （ ip4.src == $dmz || ip4.src == 192.168.1.0/24 ）
	@FieldDescriber("名称是字符串类型，长度是4到200位，只允许数字、小写字母、中划线、等于、与符号以及圆点")
	public final static String RULE_PATTERN = "'[a-z0-9-.,/{}()$&=<>| ]{2,200}'";
	
	@FieldDescriber("Address是字符串类型，长度是2到100位，只允许数字、小写字母、中划线、等于、与符号以及圆点")
	public final static String ADDRESS_PATTERN = "[a-z0-9-.,{}]{2,100}";
	
	@FieldDescriber("虚拟化类型，取值为kvm, xen之一")
	public final static String VIRT_TYPE_PATTERN = "kvm|xen";
	
	@FieldDescriber("虚拟交换机类型只能是bridge，或l2bridge，或l3bridge")
	public final static String SWITCH_TYPE_PATTERN = "bridge|l2bridge|l3bridge";
	
	@FieldDescriber("虚拟机agent支持的操作系统类型，只能是linux或windows")
	public final static String VM_AGENT_OS_TYPE_PATTERN = "linux|windows";
	
	@FieldDescriber("存储池类型，只能是localfs,uus,nfs,glusterfs,vdiskfs之一")
	public final static String POOL_TYPE_PATTERN = "localfs|uus|nfs|glusterfs|vdiskfs";

	@FieldDescriber("True或False")
	public final static String BOOL_TYPE_PATTERN = "True|False";
	
	@FieldDescriber("true或false")
	public final static String BOOL_STRING_TYPE_PATTERN = "true|false";
	
	@FieldDescriber("存储池类型，只能是vmd，vmdi，iso之一")
	public final static String POOL_CONTENT_PATTERN = "vmd|vmdi|iso";

	@FieldDescriber("存储池类型，只能是localfs,vdiskfs,nfs,glusterfs之一")
	public final static String POOL_TYPE_NOT_SUPPORT_UUS = "localfs|vdiskfs|nfs|glusterfs";
	
	@FieldDescriber("IP范围，如192.168.1.0")
	public final static String IP_PATTERN  = "(((25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]?\\d)\\.){3}(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]?\\d)|([a-zA-Z0-9]{1,4}(:[a-zA-Z0-9]{1,4}){7}))";

    @FieldDescriber("端口范围，如19999")
    public final static String PORT_PATTERN  = "([0-9]|[1-9]\\d|[1-9]\\d{2}|[1-9]\\d{3}|[1-5]\\d{4}|6[0-4]\\d{3}|65[0-4]\\d{2}|655[0-2]\\d|6553[0-5])";

    @FieldDescriber("存储池的IP范围，如192.168.1.0")
	public final static String POOL_IP_PATTERN  = "((25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]?\\d)\\.){3}(25[0-5]|2[0-4]\\d|1\\d{2}|[1-9]?\\d)";
    @FieldDescriber("创建存储池的url，如localfs:///dev/sdb1:/mnt/uit")
    public final static String POOL_URL_PATTERN = "(\\/mnt\\/localfs(\\/(\\w+\\/?)+)$)|" +
            "(\\w+(\\w+\\/?)+$)|" +
            "("+POOL_IP_PATTERN+":(\\/(\\w+\\/?)+)$)|" +
            "("+POOL_IP_PATTERN+":(\\w+)$)";

	@FieldDescriber("子网及其掩码，如192.168.1.0/24，掩码是8,16,24之一")
	public final static String SUBNET_PATTERN  = IP_PATTERN + "/([1-9]|1\\d|2\\d|30|31])";
	
	@FieldDescriber("配置虚拟交换机，source是必填，ip和switch是选填")
	public final static String IP_SWITCH_PATTERN      = "source=(virbr0|br-native|br-int|" + NAME_PATTERN + ")(,ip=" + IP_PATTERN + ")?(,switch=([a-z0-9-.]{4,32}))?";
	
	@FieldDescriber("VCPU高级配置，选填参数依次是：cpuset允许绑定具体物理CPU、maxvcpus最大vcpu个数、cores核数、sockets插槽数、threads线程数")
	public final static String VCPUSET_PATTERN      = VCPU_PATTERN + "(,cpuset=\\d{1,3}((,|-)\\d{1,3})*)?" + "(,maxvcpus=[1-9](\\d{1})?)" + "(,cores=[1-9](\\d{1})?)" + "(,sockets=[1-9](\\d{1})?)" + "(,threads=[1-9](\\d{1})?)";
	
	@FieldDescriber("配置基于vnc或者spice协议的虚拟机远程访问，密码是可选择的，为4-16位密码，是小写字母、数字和中划线组合")
	public final static String GRAPHICS_PATTERN     = "(vnc|spice),listen=0.0.0.0(,password=([a-z0-9-.]{4,16}))?";
	
	@FieldDescriber("配置vnc或者spice的4-16位密码，是小写字母、数字和中划线组合")
	public final static String PASSWORD_PATTERN     = "(([a-z0-9-.]{4,16}))?";
	
	@FieldDescriber("配置基于vnc或者spice协议的虚拟机远程访问")
	public final static String GRAPHICS_TYPE     = "(vnc|spice)";
	
	@FieldDescriber("单一磁盘，read_bytes_sec和write_bytes_sec是可选项")
	public final static String SINGLE_DISK_PATTERN  = PATH_PATTERN + "(,target=hda)?" + "(,read_bytes_sec=" + DISK_QoS_PATTERN + ")?" + "(,write_bytes_sec=" + DISK_QoS_PATTERN + ")?";
	
	@FieldDescriber("单一模板文件，read_bytes_sec和write_bytes_sec是可选项")
	public final static String SINGLE_IMAGE_PATTERN  = "ROOTDISK" + "(=" + PATH_PATTERN + ")?" + "(,target=hda)?" + "(,read_bytes_sec=" + DISK_QoS_PATTERN + ")?" + "(,write_bytes_sec=" + DISK_QoS_PATTERN + ")?";
	
	@FieldDescriber("单一光驱，必须设置成可读")
	public final static String SINGLE_CD_PATTERN  = PATH_PATTERN + ",device=cdrom,perms=ro";
	
	///var/lib/libvirt/images/test3.qcow2,read_bytes_sec=1024000000,write_bytes_sec=1024000000 --disk /opt/ISO/CentOS-7-x86_64-Minimal-1511.iso,device=cdrom,perms=ro
	@FieldDescriber("多个磁盘，必须以--disk进行连接")
	public final static String MUTI_DISKS_PATTERN   = SINGLE_DISK_PATTERN + "( --disk (" + SINGLE_DISK_PATTERN +"|" + SINGLE_CD_PATTERN + "|" + SINGLE_IMAGE_PATTERN + "))*";
	
	//type=l3bridge,source=br-int,inbound=102400,outbound=102400,ip=192.168.5.9,switch=switch,mac
	@FieldDescriber("高级网络设置，type, source,model和switch是必选项")
	public final static String NETWORK_TYPE_PATTERN = "type=("+ SWITCH_TYPE_PATTERN +")," + IP_SWITCH_PATTERN + "(,model=" + NETWORK_MODEL_PATTERN +")?" + "(,inbound=" + NET_QoS_PATTERN +")?" + "(,outbound=" + NET_QoS_PATTERN +")?" + "(,mac=" + MAC_PATTERN +")?";
	
	@FieldDescriber("设置虚拟机启动顺序，hd表示硬盘，cdrom表示光驱")
	public final static String BOOT_PATTERN = "hd|cdrom|hd,cdrom";
	
	@FieldDescriber("DNS类型，多个IP，以,号分开，如果多个，外面需要大括号")
	public final static String DNS_PATTERN = "("+ IP_PATTERN + ")|(\"\\{" + IP_PATTERN + "," + IP_PATTERN + "(," + IP_PATTERN +")*\\}\")";
	
	@FieldDescriber("无法获取IP的列表")
	public final static String EXCLUDEIPS_PATTERN = "(" + IP_PATTERN + "|" + IP_PATTERN + ".." + IP_PATTERN+")+" +  "(," + IP_PATTERN + "|," + IP_PATTERN + ".." + IP_PATTERN+")?";
	
	@FieldDescriber("网络协议，当前约束为TCP/IP")
	public final static String PROTOCAL_PATTERN = "(ip|ip4|ip6|tcp)(.(src|dst) == [a-z0-9-.]{1,100})?";
	
	@FieldDescriber("ACL规则，&&连接两个规则，注意src和dst后==前后必须有一个空格，ip4.src == $dmz && tcp.dst == 3306")
	public final static String ACL_RULE_PATTERN = PROTOCAL_PATTERN + "( && " + PROTOCAL_PATTERN + ")*";
	
	@FieldDescriber("ACL流向，只能是from或者to")
	public final static String ACL_TYPE_PATTERN = "from|to";
	
	@FieldDescriber("ACL操作，只能是allow或者frop")
	public final static String ACL_OPERATOR_PATTERN = "allow|drop";
	
	@FieldDescriber("ACL优先级，0-999")
	public final static String ACL_PRIORITY_PATTERN = "\\d{1,3}";
	
	@FieldDescriber("网络限制方向，只能是from或者to")
	public final static String QOS_TYPE_PATTERN = ACL_TYPE_PATTERN;
	
	@FieldDescriber("网络协议，支持主流协议")
	public final static String QOS_RULE_PATTERN = "ip|ip4|ip6|tcp|icmp";
	
	@FieldDescriber("QoS优先级，0-31999")
	public final static String QOS_PRIORITY_PATTERN = "\\d{1,4}|((1|2)\\d{1,4})|31\\d{1,3}";
	
	@FieldDescriber("带宽速度，单位是kbps, 0-1000Mbps")
	public final static String RATE_PATTERN = "\\d{1,6}";
	
	@FieldDescriber("带宽波动，单位是kbps, 0-100Mbps")
	public final static String BURST_PATTERN = "\\d{1,5}";

	@FieldDescriber("USB模式，逗号是连接符，usb,type=协议,server=IP:端口")
	public static final String USB_PATTERN = "1usb,type=tcp,server=" + IP_PATTERN + ":" + PORT_PATTERN;
	
	public static void main(String[] args) {
		String name = "192.168.1.10/24";
		Pattern pattern = Pattern.compile(RegExpUtils.SUBNET_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("");
		}
	}
}
