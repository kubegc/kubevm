/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.ResizeDisk;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class ResizeDiskTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.resizeDisk("disk44444", get());
		System.out.println(successful);
	}

	protected static ResizeDisk get() {
		ResizeDisk resizeDisk = new ResizeDisk();
		resizeDisk.setType("nfs");
		resizeDisk.setCapacity("21737418240");
		resizeDisk.setPool("123poolnfs");
		return resizeDisk;
	}
}
	
