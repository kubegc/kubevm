/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinediskimage.Lifecycle.CreateDiskImageFromDisk;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateDiskImageFromDiskTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDiskImages()
				.createDiskImageFromDisk("centos7", "vm.node22", get(), "abcd");
		System.out.println(successful);
	}

	protected static CreateDiskImageFromDisk get() {
		CreateDiskImageFromDisk createDiskImageFromDisk = new CreateDiskImageFromDisk();
		createDiskImageFromDisk.setTargetPool("pooldir1");
		createDiskImageFromDisk.setSourcePool("pooldir");
		createDiskImageFromDisk.setSourceVolume("pooldirdisktest");
		return createDiskImageFromDisk;
	}
}
