/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.DeleteCloudInitUserDataImage;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class DeleteCloudInitUserDataImageTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.deleteCloudInitUserDataImage("cloudinit1", get());
		System.out.println(successful);
	}
	
	public static DeleteCloudInitUserDataImage get() {
		DeleteCloudInitUserDataImage deleteDisk = new DeleteCloudInitUserDataImage();
		deleteDisk.setPool("migratepoolnodepool22");
		return deleteDisk;
	}
}
