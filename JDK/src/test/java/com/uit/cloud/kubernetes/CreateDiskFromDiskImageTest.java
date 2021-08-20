/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateDiskFromDiskImage;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateDiskFromDiskImageTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.createDiskFromDiskImage("vmbackupdisktest1", "vm.node25", get(), "abc");
		System.out.println(successful);
	}

	protected static CreateDiskFromDiskImage get() {
		CreateDiskFromDiskImage createDisk = new CreateDiskFromDiskImage();
		createDisk.setType("nfs");
		// create a volume in this pool
		createDisk.setTargetPool("3915282a12dd4c34a0ae565d3ba2da41");
		// vm disk image name
		createDisk.setSource("/var/lib/libvirt/cstor/076fe6aa813842d3ba141f172e3f8eb6/076fe6aa813842d3ba141f172e3f8eb6/a228713d3be2440e9cd1ececfe6f5783/a228713d3be2440e9cd1ececfe6f5783");
//		createDisk.setFull_copy(true);
		return createDisk;
	}
}
