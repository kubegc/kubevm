/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.HashMap;
import java.util.Map;

import com.github.kube.controller.KubevirtConstants;
import com.github.kube.controller.KubevirtWatcher;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachineDiskImage;

import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * convert VirtualMachineImage to Pod. 
 **/
public class VirtualMachineDiskImageWatcher extends KubevirtWatcher implements Watcher<VirtualMachineDiskImage> {


	/**
	 * @param client         client
	 */
	public VirtualMachineDiskImageWatcher(ExtendedKubernetesClient client) {
		super(client);
	}

	public void eventReceived(Action action, VirtualMachineDiskImage image) {
		eventReceived(action, image.getKind(), image.getMetadata(), image.getSpec());
	}

	@Override
	public ResourceRequirements getResourceDemands(Object spec) {
		ResourceRequirements resources = new ResourceRequirements();
		Map<String, Quantity> requests = new HashMap<String, Quantity>();
		requests.put(KubevirtConstants.CPU_RESOURCE, new Quantity("100m"));
		requests.put(KubevirtConstants.RAM_RESOURCE, new Quantity("64Mi"));
		resources.setRequests(requests);
		return resources;
	}

}
