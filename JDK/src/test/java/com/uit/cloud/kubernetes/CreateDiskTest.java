/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateDisk;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateDiskTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.createDisk("backuptest1", "vm.node22", get(), "abc");
		System.out.println(successful);
	}

	protected static CreateDisk get() {
		CreateDisk createDisk = new CreateDisk();
		createDisk.setPool("migratenodepool22");
		// bytes 10G
		Long size = 30L*1024*1024*1024;
		createDisk.setCapacity(String.valueOf(size));
		createDisk.setFormat("qcow2");
		createDisk.setType("nfs");
		return createDisk;
	}
}
