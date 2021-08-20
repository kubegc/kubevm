/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.henry;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeleteVM;


/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  2019/7/15
 *
 * This code is used to manage CustomResource's lifecycle,
 * such as VirtualMachine
 */
public class DeleteVMTest {
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = com.uit.cloud.kubernetes.AbstractTest.getClient();
		boolean successful = client.virtualMachines()
				.deleteVM("650646e8c17a49d0b83c1c797811e085", 
						new DeleteVM(), "eventid-delete");
		System.out.println(successful);
	}
	
}
