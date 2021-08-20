/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResizeVM;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class ResizeVMTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachines()
				.resizeVM("vmtest111", get());
		System.out.println(successful);
	}

	protected static ResizeVM get() {
		ResizeVM resizevm = new ResizeVM();
		resizevm.setPath("/var/lib/libvirt/cstor/1709accf174fccaced76b0dbfccdev/1709accf174fccaced76b0dbfccdev/vmdisk1/vmdisk1");
		Long size = 40L*1024*1024*1024;
		resizevm.setSize(String.valueOf(size));
		return resizevm;
	}
}
	
