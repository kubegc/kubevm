/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.client.Watcher.Action;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * 
 * KubevirtExecutor is used to manage Pod's lifecycle.
 * 
 **/
public class KubevirtExecutor {
	
	/**
	 * m_logger
	 */
	protected final static Logger m_logger   = Logger.getLogger(KubevirtExecutor.class.getName());
	
	/************************************************************************
	 * 
	 *                       Core
	 * 
	 ************************************************************************/
	
	/**
	 * @param client          client
	 * @param action          action
	 * @param type            from type to pod
	 * @param objMeta         object metadata
	 * @param spec            spec
	 */
	public void execute(ExtendedKubernetesClient client, Action action, String type, Pod pod) {

		// if user assign a node for a CRD, then
		// our process will skip the scheduling step
		if (pod.getSpec().getNodeName() != null) {
			return;
		}
		
		// if it is a 'ADDED' command, 
		// we will create a pod based on the CRD's info 
		String podName = pod.getMetadata().getName();
		if (action == Action.ADDED) {
			try {
				doCreate(client, podName, pod);
			} catch (Exception e) {
				// this means we cannot create a pod based on the CRD's info 
				m_logger.log(Level.SEVERE, "cannot create object because of " + e);
				doDelete(client, podName);
			}
		} else if (action == Action.DELETED) {
			doDelete(client, podName);
		}
	}

	/**
	 * @param podName            pod name
	 */
	protected void doDelete(ExtendedKubernetesClient client, String podName) {
		if (client.pods().inNamespace(KubevirtConstants.POD_NAMESPACE).withName(podName).get() != null) {
			client.pods().inNamespace(KubevirtConstants.POD_NAMESPACE).withName(podName).delete();
			logDeleteInfo(podName);
		}
	}


	/**
	 * @param podName            pod name
	 * @param pod                pod
	 */
	protected void doCreate(ExtendedKubernetesClient client, String podName, Pod pod) {
		if (client.pods().inNamespace(KubevirtConstants.POD_NAMESPACE).withName(podName).get() == null) {
			client.pods().inNamespace(KubevirtConstants.POD_NAMESPACE).create(pod);
			logCreateInfo(podName);
		}
	}
	
	/**
	 * @param podName         pod name
	 */
	public void logCreateInfo(String podName) {
		m_logger.log(Level.INFO, "Create Pod '" + podName + "' in namespace '" 
									+ KubevirtConstants.POD_NAMESPACE + "'");
	}
	
	/**
	 * @param podName         pod name
	 */
	public void logDeleteInfo(String podName) {
		m_logger.log(Level.INFO, "Delete Pod '" + podName + "' in namespace '" 
									+ KubevirtConstants.POD_NAMESPACE + "'");
	}
}
