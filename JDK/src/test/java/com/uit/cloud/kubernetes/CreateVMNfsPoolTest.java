/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateVMNfsPoolTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachinePools()
				.createPool("poolnfs", "vm.node32", getPool(), "123");
		System.out.println(successful);
	}

	protected static Lifecycle.CreatePool getPool() {
		Lifecycle.CreatePool createPool = new Lifecycle.CreatePool();

		// nfs
		createPool.setType("nfs");
		createPool.setUrl("133.133.135.30:/home/nfs");
		createPool.setContent("vmd");
		createPool.setUuid("170dd9accdd174caced76b0db3232");
		return createPool;
	}
}
