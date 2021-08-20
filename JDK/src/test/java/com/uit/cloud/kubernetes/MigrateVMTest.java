/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class MigrateVMTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachines()
				.migrateVM("centos", get());
		System.out.println(successful);
	}

	public static Lifecycle.MigrateVM get() throws Exception {
		Lifecycle.MigrateVM migrateVM = new Lifecycle.MigrateVM();
		migrateVM.setIp("133.133.135.22");
//		migrateVM.setOffline(true);
		return migrateVM;
	}
}
