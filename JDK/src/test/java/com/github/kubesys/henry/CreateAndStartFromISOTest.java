/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.henry;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromISO;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  2019/8/1
 *
 * This code is used to manage CustomResource's lifecycle,
 * such as VirtualMachine
 */
public class CreateAndStartFromISOTest {
	
	
	public static void main(String[] args) throws Exception {
		ExtendedKubernetesClient client = com.uit.cloud.kubernetes.AbstractTest.getClient();
		CreateAndStartVMFromISO createAndStartVMFromISO = get();
		// name
		boolean successful = client.virtualMachines()
				.createAndStartVMFromISO("650646e8c17a49d0b83c1c797811e085", 
						createAndStartVMFromISO, "eventid-create");
		System.out.println(successful);
	}
	
	
	public static CreateAndStartVMFromISO get() throws Exception {
		
		CreateAndStartVMFromISO createAndStartVMFromISO = new CreateAndStartVMFromISO();
		// default value
		createAndStartVMFromISO.setMetadata("uuid=650646e8-c17a-49d0-b83c-1c797811e081");
		createAndStartVMFromISO.setVirt_type("kvm"); 
		createAndStartVMFromISO.setOs_variant("RHEL");
		createAndStartVMFromISO.setNoautoconsole(true); 
		
		// calculationSpecification
		calculationSpecification(createAndStartVMFromISO);  
		
		// cdrom
		createAndStartVMFromISO.setCdrom("/opt/ISO/CentOS-7-x86_64-Minimal-1511.iso"); 
		// Disk and QoS for 1 disk and many disks
		createAndStartVMFromISO.setDisk("size=10");
		
		//network and QoS
		createAndStartVMFromISO.setNetwork("bridge=br-int,virtualport_type=openvswitch");  
		
		// consoleMode amd passowrd
		createAndStartVMFromISO.setGraphics("vnc,listen=0.0.0.0");
//		createAndStartVMFromISO.setGraphics("spice,listen=0.0.0.0" + getconsolePassword("567890")); 
		
		createAndStartVMFromISO.setOs_variant("rhel7");
		return createAndStartVMFromISO;
	}


	protected static void calculationSpecification(CreateAndStartVMFromISO createAndStartVMFromISO) {
		createAndStartVMFromISO.setMemory("1024");    
		createAndStartVMFromISO.setVcpus("1");
//		createAndStartVMFromISO.setBlkiotune("iotune");
	}
	
}
