/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.ha;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.api.model.Node;
import io.fabric8.kubernetes.api.model.ObjectReference;
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
public class NodeStatusWatcher implements Watcher<Node> {

	protected final static Logger m_logger = Logger.getLogger(NodeStatusWatcher.class.getName());

	protected final ExtendedKubernetesClient client;

	public NodeStatusWatcher(ExtendedKubernetesClient client) {
		this.client = client;
	}

	protected boolean isShutDown(Map<String, Object> status) {
		return status.get("reason").equals("ShutDown");
	}

	public void onClose(KubernetesClientException cause) {
		System.out.println(cause);
		m_logger.log(Level.INFO, "Stop NodeStatusWatcher:" + cause);
		client.nodes().watch(new NodeStatusWatcher(client));
	}

	@Override
	public void eventReceived(Action action, Node node) {

		String nodeName = node.getMetadata().getName();

		if (nodeName.startsWith("vm.") && NodeSelectorImpl.notReady(node)) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);

			for (VirtualMachine vm : client.virtualMachines().list(labels).getItems()) {
				try {
					
					m_logger.log(Level.INFO, "Check VM " + vm.getMetadata().getName() + "'s power status.");
					String power = vm.getSpec().getPowerstate();
					if (power == null || "".equals(power) || "Shutdown".equals(power)) {
						m_logger.log(Level.INFO, "VM " + vm.getMetadata().getName() + " is already shutdown.");
						continue;
					}
					
					vm.getSpec().setPowerstate("Shutdown");
					client.virtualMachines().update(vm);
					m_logger.log(Level.INFO, "Update VM " + vm.getMetadata().getName() + " status to Shutdown.");
				} catch (Exception e) {
					System.out.println("Error to modify the VM's status:" + e.getCause());
					m_logger.severe("Error to modify the VM's status:" + e.getCause());
				} finally {
					Event item = new Event();
					ObjectReference involvedObject = new ObjectReference();
					involvedObject.setKind(VirtualMachine.class.getSimpleName());
					involvedObject.setName(vm.getMetadata().getName());
					involvedObject.setNamespace(vm.getMetadata().getNamespace());
					item.setInvolvedObject(involvedObject );
					item.setReason("ShutdownVM");
					client.events().create(item );
				}
			}
		}
	}
}
