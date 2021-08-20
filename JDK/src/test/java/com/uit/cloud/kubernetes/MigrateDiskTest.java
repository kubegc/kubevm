/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CloneDisk;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class MigrateDiskTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.migrateDisk("vmtest111disk2", getMigrateDisk());
		System.out.println(successful);
	}

	public static Lifecycle.MigrateDisk getMigrateDisk() {
		Lifecycle.MigrateDisk createDisk = new Lifecycle.MigrateDisk();
		createDisk.setPool("c6ce75b556b445929a3c24e865a07df0");
		return createDisk;
	}
}
