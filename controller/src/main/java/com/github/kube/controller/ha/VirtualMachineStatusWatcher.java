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

import io.fabric8.kubernetes.api.model.Node;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.dsl.MixedOperation;

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
public class VirtualMachineStatusWatcher implements Watcher<VirtualMachine> {

	protected final static Logger m_logger = Logger.getLogger(VirtualMachineStatusWatcher.class.getName());

	protected final ExtendedKubernetesClient client;
	
	public VirtualMachineStatusWatcher(ExtendedKubernetesClient client) {
		this.client = client;
	}

	public void eventReceived(Action action, VirtualMachine vm) {
		
		if(!enableHA(vm)) {
			return;
		}

		// get nodeName
		String nodeName = vm.getSpec().getNodeName();
					
		// this vm is running or the vm is not marked as HA
		if (isShutDown(getStatus(vm)) && nodeName != null) {
			
			m_logger.log(Level.INFO, "Plan to start VM " + vm.getMetadata().getName());
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
			
			String newNode = invalidNodeStatus(getNode(nodeName)) ? client.getNodeSelector()
					.getNodename(Policy.minimumCPUUsageHostAllocatorStrategyMode, nodeName, filters) : nodeName;
			
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

	protected boolean invalidNodeStatus(Node node) {
		try {
			return node == null 
				|| NodeSelectorImpl.isMaster(node) 
				|| NodeSelectorImpl.notReady(node) 
				|| NodeSelectorImpl.unSched(node);
		} catch (Exception ex) {
			return true;
		}
	}

	protected Node getNode(String nodeName) {
		try {
			return client.nodes().withName(nodeName).get();
		} catch (Exception ex) {
			return null;
		}
	}

	protected boolean isShutDown(String status) {
		return (status == null) || status.equals("Shutdown");
	}
	

	protected String getStatus(VirtualMachine vm) {
		return vm.getSpec().getPowerstate();
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineStatusWatcher:" + cause);
		MixedOperation vmWatcher = ExtendedKubernetesClient.crdClients.get(
				VirtualMachine.class.getSimpleName());
		vmWatcher.watch(new VirtualMachineStatusWatcher(client));
	}

}
