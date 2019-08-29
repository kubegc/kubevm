/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSnapshot;

import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed July 08 17:26:22 CST 2019
 * 
 *        https://www.json2yaml.com/ http://www.bejson.com/xml2json/
 * 
 *        debug at runWatch method of
 *        io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class VirtualMachineSnapshotWatcher extends AbstractWatcher implements Watcher<VirtualMachineSnapshot> {

	protected final static Logger m_logger = Logger.getLogger(VirtualMachineSnapshotWatcher.class.getName());

	public VirtualMachineSnapshotWatcher(ExtendedKubernetesClient client) {
		super(client);
	}


	public void eventReceived(Action action, VirtualMachineSnapshot snapshot) {

		String namespace = snapshot.getMetadata().getNamespace();
		String podName = getPrefix() + "-" + snapshot.getMetadata().getName() + "-" + namespace;
		
		if (action.toString().equals(ACTION_ADDED)) {
			Pod pod = null;;
			try {
				pod = createPod(snapshot.getMetadata(), snapshot.getSpec(), snapshot.getSpec().getNodeSelector(),
						snapshot.getSpec().getNodeName(), podName);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			if (client.pods().inNamespace(namespace).withName(podName).get() == null) {

				client.pods().inNamespace(namespace).create(pod);
				m_logger.log(Level.INFO, "Create snapshot '" + snapshot.getMetadata().getName() + "' in namespace '"
						+ snapshot.getMetadata().getNamespace() + "'");
				m_logger.log(Level.INFO, "Create Pod '" + podName + "' in namespace '" + namespace + "'");
			}
		} else if (action.toString().equals(ACTION_DELETED)) {
			if (client.pods().inNamespace(namespace).withName(podName).get() != null) {
				client.pods().inNamespace(namespace).withName(podName).delete();
				m_logger.log(Level.INFO, "Delete Pod '" + podName + "' in namespace '" + namespace + "'");
				m_logger.log(Level.INFO, "Delete snapshot '" + snapshot.getMetadata().getName() + "' in namespace '"
						+ snapshot.getMetadata().getNamespace() + "'");
			}
		}
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineSnapshotWatcher");
	}

	@Override
	public String getPrefix() {
		return "snapshot2pod";
	}


	@Override
	public String getPlural() {
		return "virtualmachinesnapshots";
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
