/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromISO;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateAndStartSingleDiskTest {
	
	
	public static void main(String[] args) throws Exception {
		ExtendedKubernetesClient client = AbstractTest.getClient();
		CreateAndStartVMFromISO createAndStartVMFromISO = get();
		// name
		boolean successful = client.virtualMachines()
				.createAndStartVMFromISO("test1", "vm.node22", createAndStartVMFromISO, "01");
		System.out.println(successful);
	}
	
	
	public static CreateAndStartVMFromISO get() throws Exception {
		
		CreateAndStartVMFromISO createAndStartVMFromISO = new CreateAndStartVMFromISO();
		// default value
//		createAndStartVMFromISO.setMetadata("uuid=950646e8-c17a-49d0-b83c-1c797811vm001");
		createAndStartVMFromISO.setVirt_type("kvm"); 
		// @see https://github.com/uit-plus/api/blob/master/src/main/java/com/github/uitplus/utils/OSDistroUtils.java
		createAndStartVMFromISO.setOs_variant("centos7.0");
		createAndStartVMFromISO.setNoautoconsole(true); 
		
		// calculationSpecification
		calculationSpecification(createAndStartVMFromISO);  
		
		// Disk and QoS for 1 disk and many disks
		// path /var/lib/libvirt/images/test11 can be get by CreateDiskTest
		// cdrom
//		createAndStartVMFromISO.setCdrom("/var/lib/libvirt/iso/centos7-minimal-1511.iso"); 
		// Disk and QoS for 1 disk and many disks
//		createAndStartVMFromISO.setBoot("hd");
		createAndStartVMFromISO.setDisk("/var/lib/libvirt/images/650646e8c17a49d0b83c1c797811e068-10.qcow2,cache=none,read_bytes_sec=1024000000,write_bytes_sec=1024000000");
				

		/*
		 * libivrt default bridge
		 * Parameters:
		 * 	type
		 * 		type of network support values: "bridge", "l2bridge" and "l3bridge"
		 * 	source
		 * 		network source name
		 * 	inbound (optional)
		 * 		inbound bandwidth in KB
		 * 	outbound (optional)
		 * 		outbound bandwidth in KB
		 * 	mac (optional)
		 * 		if no mac, create a random mac
		 * 		Note! Mac address is unique and does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3)
		 */
//		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,ip=192.168.10.14,switch=vxlan");
		createAndStartVMFromISO.setNetwork("type=bridge,source=virbr0,model=virtio");
//      if you want to use l3bridge, please first execute the command on your master node, 'kubeovn-adm create-switch --name switch8888 --subnet 192.168.5.0/24' 		
//		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,switch=l2l3,inbound=102400,outbound=102400");  
		
		/*
		 * l2 network example
		 * Parameters:
		 * 	type
		 * 		type of network support values: "bridge", "l2bridge" and "l3bridge"
		 * 	source
		 * 		network source name
		 * 	inbound (optional)
		 * 		inbound bandwidth in KB
		 * 	outbound (optional)
		 * 		outbound bandwidth in KB
		 * 	mac (optional)
		 * 		if no mac, create a random mac
		 * 		Note! Mac address is unique and does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3)
		 */
//		createAndStartVMFromISO.setNetwork("type=l2bridge,source=br-native,inbound=102400,outbound=102400");
		
		/*
		 * l3 network example
		 * Parameters:
		 * 	type
		 * 		type of network support values: "bridge", "l2bridge" and "l3bridge"
		 * 	source
		 * 		network source name
		 * 	inbound (optional)
		 * 		inbound bandwidth limitation in KB, default is no limitation
		 * 	outbound (optional)
		 * 		outbound bandwidth limitation in KB, default is no limitation
		 * 	mac (optional)
		 * 		if no mac, create a random mac
		 * 		Note! Mac address is unique and does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3)
		 * 	ip (optional)
		 * 		ip address for l3 network, default is "dynamic" from DHCP
		 * 	switch
		 * 		switch name
		 */
		
//		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,inbound=102400,outbound=102400,ip=192.168.5.9,switch=switch");  
		
		// consoleMode amd passowrd
		createAndStartVMFromISO.setGraphics("vnc,listen=0.0.0.0");
//		createAndStartVMFromISO.setGraphics("spice,listen=0.0.0.0" + getconsolePassword("567890")); 
		
		return createAndStartVMFromISO;
	}


	protected static void calculationSpecification(CreateAndStartVMFromISO createAndStartVMFromISO) {
		createAndStartVMFromISO.setMemory("1024,maxmemory=1024");    
		createAndStartVMFromISO.setVcpus("1" + getCPUSet("1-4,6,8"));
	}
	
	protected static String getCPUSet(String cpuset) {
		return (cpuset == null || cpuset.length() == 0) 
				? "" :",cpuset=" + cpuset;
	}
	
	protected static String getconsolePassword(String pwd) {
		return (pwd == null || pwd.length() == 0) ? "" : ",password=111111";
	}
	
	protected static String nameToUUID(String name) {
		StringBuffer sb = new StringBuffer();
		sb.append(name.substring(0, 8)).append("-")
				.append(name.substring(8, 12)).append("-")
				.append(name.substring(12, 16)).append("-")
				.append(name.substring(16, 20)).append("-")
				.append(name.substring(20, 32));
		return sb.toString();
	}
	
}
