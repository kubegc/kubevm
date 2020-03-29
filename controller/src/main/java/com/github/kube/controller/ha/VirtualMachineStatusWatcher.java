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
		
		System.out.println(vm.getMetadata().getName());
		
		String ha = vm.getMetadata().getLabels().get("ha");
		// VM without HA setting
		if (ha == null || ha.length() == 0 
					|| !ha.equals("true")) {
			return;
		}

		// get nodeName
		String nodeName = vm.getSpec().getNodeName();
					
		// this vm is running or the vm is not marked as HA
		if (isShutDown(getStatus(vm)) && nodeName != null) {
			
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
			
			// just start VM
			try {
				if (newNode == null || newNode.length() == 0) {
					m_logger.log(Level.SEVERE, "cannot find avaiable nodes");
				} else if (nodeName.equals(newNode)) {
					client.virtualMachines().startVMWithPower(
							vm.getMetadata().getName(), nodeName , new StartVM(), "Starting");
				} else {
					client.virtualMachines().startVMWithPower(
							vm.getMetadata().getName(), newNode, new StartVM(), "Starting");
				}
			} catch (Exception e) {
				m_logger.log(Level.SEVERE, "cannot start vm for " + e);
			}
		}
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
//		try {
//			Map<String, Object> statusProps = vm.getSpec().getStatus().getAdditionalProperties();	
//			Map<String, Object> statusCond = (Map<String, Object>) (statusProps.get("conditions"));
//			Map<String, Object> statusStat = (Map<String, Object>) (statusCond.get("state"));
//			return (Map<String, Object>) (statusStat.get("waiting"));
//		} catch (Exception ex) {
//			return null;
//		}
		return vm.getSpec().getPowerstate();
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineStatusWatcher");
	}

}
