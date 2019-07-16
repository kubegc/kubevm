/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSpec;

import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed May 01 17:26:22 CST 2019
 * 
 *        https://www.json2yaml.com/ http://www.bejson.com/xml2json/
 * 
 *        debug at runWatch method of
 *        io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class VirtualMachineWatcher extends AbstractWatcher implements Watcher<VirtualMachine> {

	protected final static Logger m_logger = Logger.getLogger(VirtualMachineWatcher.class.getName());

	public VirtualMachineWatcher(ExtendedKubernetesClient client) {
		super(client);
	}

	public void eventReceived(Action action, VirtualMachine vm) {

		String namespace = vm.getMetadata().getNamespace();
		String podName = getPrefix() + "-" + vm.getMetadata().getName() + "-" + namespace;
		
		if (action.toString().equals(ACTION_CREATE)) {
			Pod pod = null;;
			try {
				pod = createPod(vm.getMetadata(), vm.getSpec(), podName);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			if (client.pods().inNamespace(namespace).withName(podName).get() == null) {

				client.pods().inNamespace(namespace).create(pod);
				m_logger.log(Level.INFO, "Create VM '" + vm.getMetadata().getName() + "' in namespace '"
						+ vm.getMetadata().getNamespace() + "'");
				m_logger.log(Level.INFO, "Create Pod '" + podName + "' in namespace '" + namespace + "'");
			}
		} else if (action.toString().equals(ACTION_REMOVE)) {
			if (client.pods().inNamespace(namespace).withName(podName).get() != null) {
				client.pods().inNamespace(namespace).withName(podName).delete();
				m_logger.log(Level.INFO, "Delete Pod '" + podName + "' in namespace '" + namespace + "'");
				m_logger.log(Level.INFO, "Delete VM '" + vm.getMetadata().getName() + "' in namespace '"
						+ vm.getMetadata().getNamespace() + "'");
			}
		}
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineWatcher");
	}

	@Override
	public String getPrefix() {
		return "vm2pod";
	}

	@Override
	public String getPlural() {
		return "virtualmachines";
	}

	@Override
	public ResourceRequirements getResourceDemands(Object spec) {
		ResourceRequirements resources = new ResourceRequirements();
		Map<String, Quantity> requests = new HashMap<String, Quantity>();
		VirtualMachineSpec vms = (VirtualMachineSpec) spec;
		if (vms.getLifecycle().getCreateAndStartVMFromISO() != null) {
			requests.put(CPU_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromISO().getVcpus()));
			requests.put(RAM_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromISO().getMemory()));
		} else if (vms.getLifecycle().getCreateAndStartVMFromImage() != null) {
			requests.put(CPU_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromImage().getVcpus()));
			requests.put(RAM_RESOURCE, new Quantity(vms.getLifecycle().getCreateAndStartVMFromImage().getMemory()));
		} 
		resources.setRequests(requests);
		return resources;
	}

}
