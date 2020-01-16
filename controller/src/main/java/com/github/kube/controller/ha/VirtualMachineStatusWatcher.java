/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.ha;

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
		
		String ha = vm.getMetadata().getLabels().get("ha");
		// VM without HA setting
		if (ha == null || ha.length() == 0 
					|| !ha.equals("true")) {
			return;
		}

		// ignore this status
		if (action == Action.MODIFIED) {
			return;
		}
		
		// this vm is running or the vm is not marked as HA
		if (isShutDown(getStatus(vm))) {
			
			// get nodeName
			String nodeName = vm.getSpec().getNodeName();
			
			String newNode = invalidNodeStatus(getNode(nodeName)) ? client.getNodeSelector()
					.getNodename(Policy.minimumCPUUsageHostAllocatorStrategyMode, nodeName) : nodeName;
			
			// just start VM
			try {
				if (nodeName.equals(newNode)) {
					client.virtualMachines().startVM(
							vm.getMetadata().getName(), new StartVM());
				} else {
					client.virtualMachines().startVM(
							vm.getMetadata().getName(), nodeName, new StartVM());
				}
			} catch (Exception e) {
				m_logger.log(Level.SEVERE, "cannot start vm for " + e);
			}
		}
	}


	protected boolean invalidNodeStatus(Node node) {
		return node == null 
				|| NodeSelectorImpl.isMaster(node) 
				|| NodeSelectorImpl.notReady(node) 
				|| NodeSelectorImpl.unSched(node);
	}

	protected Node getNode(String nodeName) {
		try {
			return client.nodes().withName(nodeName).get();
		} catch (Exception ex) {
			return null;
		}
	}

	protected boolean isShutDown(Map<String, Object> status) {
		return status.get("reason").equals("Shutdown");
	}

	@SuppressWarnings("unchecked")
	protected Map<String, Object> getStatus(VirtualMachine vm) {
		Map<String, Object> statusProps = vm.getSpec().getStatus().getAdditionalProperties();	
		Map<String, Object> statusCond = (Map<String, Object>) (statusProps.get("conditions"));
		Map<String, Object> statusStat = (Map<String, Object>) (statusCond.get("state"));
		return (Map<String, Object>) (statusStat.get("waiting"));
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineStatusWatcher");
	}

}
