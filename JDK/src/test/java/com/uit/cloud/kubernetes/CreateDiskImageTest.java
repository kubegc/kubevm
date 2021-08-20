/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinediskimage.Lifecycle.CreateDiskImage;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateDiskImageTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDiskImages()
				.createDiskImage("a228713d3be2440e9cd1ececfe6f5783", "vm.node25", get(), "abc");
		System.out.println(successful);
	}

	protected static CreateDiskImage get() {
		CreateDiskImage createDiskImage = new CreateDiskImage();
		// Only support file in "/var/lib/libvirt/" or its sub-dirs
//		createDiskImage.setSource("/var/lib/libvirt/cstor/076fe6aa813842d3ba141f172e3f8eb6/076fe6aa813842d3ba141f172e3f8eb6/a228752f3be2440e9cd1ececfe6f5783/a228752f3be2440e9cd1ececfe6f5783");
		createDiskImage.setTargetPool("a9f69fcf05c946d492369d5d8531d34b");
		return createDiskImage;
	}
}
