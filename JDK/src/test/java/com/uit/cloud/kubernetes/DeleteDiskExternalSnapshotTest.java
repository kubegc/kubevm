/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisksnapshot.Lifecycle.DeleteDiskExternalSnapshot;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class DeleteDiskExternalSnapshotTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDiskSnapshots()
				.deleteDiskExternalSnapshot("vmbackuptestdisk1.1", get());
		System.out.println(successful);
	}
	
	public static DeleteDiskExternalSnapshot get() {
		DeleteDiskExternalSnapshot deleteDiskExternalSnapshot = new DeleteDiskExternalSnapshot();
		deleteDiskExternalSnapshot.setPool("61024b305b5c463b80bceee066077079");
		deleteDiskExternalSnapshot.setType("nfs");
		deleteDiskExternalSnapshot.setVol("vmbackuptestdisk1");
		deleteDiskExternalSnapshot.setDomain("vmbackuptest");
		return deleteDiskExternalSnapshot;
	}
}
