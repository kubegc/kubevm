/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import java.util.ArrayList;
import java.util.List;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.BatchDeprecatedACL;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeprecatedACL;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class DeleteBatchDeprcatedACLsTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachines()
				.batchDeprecatedACL("cloudinit1", get());
		System.out.println(successful);
	}
	
	public static BatchDeprecatedACL get() {
		BatchDeprecatedACL bda = new BatchDeprecatedACL();
		List<DeprecatedACL> deprecatedACLs = new ArrayList<DeprecatedACL>();
		DeprecatedACL a1 = new DeprecatedACL();
		a1.setSwName("aaa1");
		a1.setVmmac("52:54:00:fd:67:3b");
		deprecatedACLs.add(a1);
		DeprecatedACL a2 = new DeprecatedACL();
		a2.setSwName("aaa2");
		a2.setVmmac("52:54:00:fd:67:3b");
		deprecatedACLs.add(a2);
		bda.setDeprecatedACLs(deprecatedACLs );
		return bda;
	}
}
