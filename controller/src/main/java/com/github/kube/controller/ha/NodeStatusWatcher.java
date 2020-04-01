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
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StartVM;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl.Policy;

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
	public synchronized void eventReceived(Action action, Node node) {

		String nodeName = node.getMetadata().getName();

		if (nodeName.startsWith("vm.") && NodeSelectorImpl.notReady(node)) {
			m_logger.log(Level.INFO, "Node " + nodeName + " is shutdown.");
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			m_logger.log(Level.INFO, "Labels are " + labels);
			for (VirtualMachine vm : client.virtualMachines().list(labels).getItems()) {
				try {
					
					m_logger.log(Level.INFO, "Check VM " + vm.getMetadata().getName() + "'s power status.");
					String power = vm.getSpec().getPowerstate();
					if (power != null && !"Shutdown".equals(power)) {
						vm.getSpec().setPowerstate("Shutdown");
						m_logger.log(Level.INFO, "Update VM " + vm.getMetadata().getName() + " status to Shutdown.");
					} else {
						m_logger.log(Level.INFO, "VM " + vm.getMetadata().getName() + "'s status is already Shutdown.");
					}
					
					if(!enableHA(vm)) {
						continue;
					}
					
					m_logger.log(Level.INFO, "Plan to start VM " + vm.getMetadata().getName() + "on another machine.");
					Map<String, String> filters = new HashMap<String, String>();
					if (vm.getMetadata().getLabels() != null) {
						String cluster = vm.getMetadata().getLabels().get("cluster");
						String zone = vm.getMetadata().getLabels().get("zone");
						if (zone != null) {
							filters.put("zone", zone);
						} else if (cluster != null) {
							filters.put("cluster", cluster);
						} 
					}
					
					String newNode = client.getNodeSelector()
							.getNodename(Policy.minimumCPUUsageHostAllocatorStrategyMode, nodeName, filters);
					
					m_logger.log(Level.INFO, "Select node " + newNode + " for VM " + vm.getMetadata().getName());
					// just start VM
					try {
						if (newNode == null || newNode.length() == 0) {
							m_logger.log(Level.SEVERE, "cannot find avaiable nodes");
						} else if (nodeName.equals(newNode)) {
							m_logger.log(Level.INFO, "Cannot start VM " + vm.getMetadata().getName() + " on the same machine.");
						} else {
							client.virtualMachines().startVMWithPower(
									vm.getMetadata().getName(), newNode, new StartVM(), "Starting");
							client.virtualMachines().get(vm.getMetadata().getName());
							m_logger.log(Level.INFO, "Start VM " + vm.getMetadata().getName() + " on the node " + newNode);
						}
					} catch (Exception e) {
						m_logger.log(Level.SEVERE, "cannot start vm for " + e);
					}
					
				} catch (Exception e) {
					System.out.println("Error to modify the VM's status:" + e.getCause());
					m_logger.severe("Error to modify the VM's status:" + e.getCause());
				} 
//				finally {
//					Event item = new Event();
//					ObjectReference involvedObject = new ObjectReference();
//					involvedObject.setKind(VirtualMachine.class.getSimpleName());
//					involvedObject.setName(vm.getMetadata().getName());
//					involvedObject.setNamespace(vm.getMetadata().getNamespace());
//					item.setInvolvedObject(involvedObject );
//					item.setReason("ShutdownVM");
//					client.events().create(item );
//				}
			}
		}
	}
	
	
	public static boolean enableHA(VirtualMachine vm) {
		String ha = vm.getMetadata().getLabels().get("ha");
		// VM without HA setting
		if (ha == null || ha.length() == 0 
					|| !ha.equals("true")) {
			return false;
		}
		return true;
	}
}
