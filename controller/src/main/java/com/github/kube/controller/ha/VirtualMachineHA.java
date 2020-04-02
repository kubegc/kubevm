/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.ha;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kube.controller.KubevirtUtils;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StartVM;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl.Policy;

import io.fabric8.kubernetes.api.model.Node;
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
public class VirtualMachineHA implements Watcher<Node> {

	protected final static Logger m_logger = Logger.getLogger(VirtualMachineHA.class.getName());

	protected final ExtendedKubernetesClient client;

	public VirtualMachineHA(ExtendedKubernetesClient client) {
		this.client = client;
	}

	protected boolean isShutDown(Map<String, Object> status) {
		return status.get("reason").equals("ShutDown");
	}

	public void onClose(KubernetesClientException cause) {
		System.out.println(cause);
		m_logger.log(Level.INFO, "Stop NodeStatusWatcher:" + cause);
		m_logger.log(Level.INFO, "Restart VirtualMachineHA service");
		client.nodes().watch(new VirtualMachineHA(client));
	}

	@Override
	public synchronized void eventReceived(Action action, Node node) {

		usingAnotherMachineToStartVMsOn(node);
	}

	public void usingAnotherMachineToStartVMsOn(Node node) {
		String fromNode = node.getMetadata().getName();

		if (NodeSelectorImpl.isMaster(node) 
				|| !fromNode.startsWith("vm") 
				|| !NodeSelectorImpl.notReady(node)) {
			return;
		}
		
		m_logger.log(Level.INFO, "Node " + fromNode + " is shutdown.");
		
		for (VirtualMachine vm : findAllVMsOn(fromNode)) {
			
			try {
				
				updateVMPowerstateToShutdownIfNeed(vm);
				
				if(!KubevirtUtils.enableHA(vm) || KubevirtUtils.localVM(vm)) {
					m_logger.log(Level.INFO, "VM " + vm.getMetadata().getName() + " disable HA or it is a local VM.");
					continue;
				}
				
				String toNode = selectNewNode(vm);
				m_logger.log(Level.INFO, "Select node " + toNode + " for VM " + vm.getMetadata().getName());
				// just start VM
				restartVM(vm, fromNode, toNode);
				
			} catch (Exception e) {
				System.out.println("Error to modify the VM's status:" + e.getCause());
				m_logger.severe("Error to modify the VM's status:" + e.getCause());
			} 
		}
	}

	public String selectNewNode(VirtualMachine vm) {
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
		
		return client.getNodeSelector()
				.getNodename(Policy.minimumCPUUsageHostAllocatorStrategyMode, filters);
		
		
	}
	
	public void restartVM(VirtualMachine vm, String fromNode, String toNode) {
		try {
			if (toNode == null || toNode.length() == 0) {
				m_logger.log(Level.SEVERE, "cannot find avaiable nodes");
			} else if (fromNode.equals(toNode)) {
				m_logger.log(Level.INFO, "Cannot start VM " + vm.getMetadata().getName() + " on the same machine.");
			} else {
				client.virtualMachines().startVMWithPower(
						vm.getMetadata().getName(), toNode, new StartVM(), "Starting");
				client.virtualMachines().get(vm.getMetadata().getName());
				m_logger.log(Level.INFO, "Start VM " + vm.getMetadata().getName() + " on the node " + toNode);
			}
		} catch (Exception e) {
			m_logger.log(Level.SEVERE, "cannot start vm for " + e);
		}
	}
	
	public List<VirtualMachine> findAllVMsOn(String nodeName) {
		Map<String, String> labels = new HashMap<String, String>();
		labels.put("host", nodeName);
		return client.virtualMachines().list(labels).getItems();
	}
	
	public void updateVMPowerstateToShutdownIfNeed (VirtualMachine vm) {
		m_logger.log(Level.INFO, "Check VM " + vm.getMetadata().getName() + "'s power status.");
		String power = vm.getSpec().getPowerstate();
		if (power != null && !"Shutdown".equals(power)) {
			vm.getSpec().setPowerstate("Shutdown");
			m_logger.log(Level.INFO, "Update VM " + vm.getMetadata().getName() + " status to Shutdown.");
		} else {
			m_logger.log(Level.INFO, "VM " + vm.getMetadata().getName() + "'s status is already Shutdown.");
		}
	}
	
}
