/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.henry;

import java.util.Map;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;

import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  2019/8/1
 *
 * This code is used to manage CustomResource's lifecycle,
 * such as VirtualMachine
 */
public class GetVMTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = com.uit.cloud.kubernetes.AbstractTest.getClient();
		System.out.println(client.virtualMachines().get("650646e8c17a49d0b83c1c797811e081"));
	}
	
	
}
