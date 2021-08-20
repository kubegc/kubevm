/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.henry;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  2019/8/1
 *
 * This code is used to manage CustomResource's lifecycle,
 * such as VirtualMachine
 */
public class ListenEventTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = com.uit.cloud.kubernetes.AbstractTest.getClient();
		client.events().watch(new Watcher<Event>() {

			@Override
			public void eventReceived(Action action, Event resource) {
				if (!resource.getInvolvedObject().getKind().equals("VirtualMachine")
					|| action != Action.MODIFIED)  {
					return;
				}
				System.out.println(action + ":" + resource);
			}

			@Override
			public void onClose(KubernetesClientException cause) {
				// TODO Auto-generated method stub
				
			}});
	}
	
	
}
