/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;

import com.github.kube.controller.KubevirtConstants;
import com.github.kube.controller.KubevirtWatcher;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSpec;

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
 * convert VirtualMachine to Pod. 
 **/
public class VirtualMachineWatcher extends KubevirtWatcher implements Watcher<VirtualMachine> {

	/**
	 * @param client            client
	 */
	public VirtualMachineWatcher(ExtendedKubernetesClient client) {
		super(client);
	}

	public void eventReceived(Action action, VirtualMachine vm) {
		eventReceived(action, vm.getKind(), vm.getMetadata(), vm.getSpec());
	}

	@Override
	public ResourceRequirements getResourceDemands(Object spec) {
		ResourceRequirements resources = new ResourceRequirements();
		Map<String, Quantity> requests = new HashMap<String, Quantity>();
		VirtualMachineSpec vms = (VirtualMachineSpec) spec;
		if (vms.getLifecycle().getCreateAndStartVMFromISO() != null) {
			requests.put(KubevirtConstants.CPU_RESOURCE, new Quantity(getCPU(vms.getLifecycle().getCreateAndStartVMFromISO().getVcpus())));
			requests.put(KubevirtConstants.RAM_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromISO().getMemory()));
		} else if (vms.getLifecycle().getCreateAndStartVMFromImage() != null) {
			requests.put(KubevirtConstants.CPU_RESOURCE, new Quantity(getCPU(vms.getLifecycle().getCreateAndStartVMFromImage().getVcpus())));
			requests.put(KubevirtConstants.RAM_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromImage().getMemory()));
		} 
		resources.setRequests(requests);
		return resources;
	}

	/**
	 * @param str     the CPU description 
	 * @return        CPU number
	 */
	public String getCPU(String str) {
		String[] values = str.split(",");
		return values[0];
	}

	@Override
	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.SEVERE, cause.toString());
		client.watchVirtualMachines(this);
	}
}
