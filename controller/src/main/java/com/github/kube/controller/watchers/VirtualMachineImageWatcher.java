/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.HashMap;
import java.util.Map;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachineImage;

import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since Wed Aug 29 17:26:22 CST 2019
 * 
 * convert VirtualMachineImage to Pod. 
 **/
public class VirtualMachineImageWatcher extends AbstractWatcher implements Watcher<VirtualMachineImage> {


	/**
	 * @param client         client
	 */
	public VirtualMachineImageWatcher(ExtendedKubernetesClient client) {
		super(client);
	}

	public void eventReceived(Action action, VirtualMachineImage image) {
		doConvert(action.toString(), image.getMetadata(), image.getSpec());
	}

	public void onClose(KubernetesClientException cause) {
		logStopInfo(cause);
	}

	@Override
	public ResourceRequirements getResourceDemands(Object spec) {
		ResourceRequirements resources = new ResourceRequirements();
		Map<String, Quantity> requests = new HashMap<String, Quantity>();
		requests.put(CPU_RESOURCE, new Quantity("100m"));
		requests.put(RAM_RESOURCE, new Quantity("64Mi"));
		resources.setRequests(requests);
		return resources;
	}

}
