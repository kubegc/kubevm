/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kube.controller.watchers.VirtualMachineWatcher;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.ExtendedCustomResourceDefinitionSpec;

import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher.Action;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * AbstractWatcher provides a common method to convert VM-related CRD to Pod. 
 **/
public abstract class KubevirtWatcher {

	/**
	 * m_logger
	 */
	protected final static Logger m_logger   = Logger.getLogger(VirtualMachineWatcher.class.getName());
	
	/**
	 * convertor
	 */
	protected final KubevirtConvertor convertor = new KubevirtConvertor();
	
	/**
	 * executor
	 */
	protected final KubevirtExecutor executor = new KubevirtExecutor();
	
	/**
	 * Kubernetes client
	 */
	protected final ExtendedKubernetesClient client;
	
	/**
	 * @param client           client
	 */
	public KubevirtWatcher(ExtendedKubernetesClient client) {
		this.client = client;
	}
	
	
	/************************************************************************
	 * 
	 *                       Core
	 * 
	 ************************************************************************/
	/**
	 * @param spec            spec
	 * @return                container's resource requirements
	 */
	public abstract ResourceRequirements getResourceDemands(Object spec);

	/**
	 * @param action           action
	 * @param meta             meta
	 * @param spec             spec
	 */
	public void eventReceived(Action action, ObjectMeta meta, Object spec) {
		try {
			ExtendedCustomResourceDefinitionSpec espec = (ExtendedCustomResourceDefinitionSpec) spec;
			Pod pod = convertor.createPod(meta, createAnnotations(meta.getName(), meta.getNamespace()), 
											espec, espec.getNodeName(), getResourceDemands(espec), 
											espec.getNodeSelector(), espec.getAffinity(), getPodName(meta));
			executor.execute(client, action, getKind(), pod);
		} catch (Exception ex) {
			m_logger.log(Level.SEVERE, ex.toString());
		}
	}
	
	/**
	 * 
	 * convert CRD to Pod annotations
	 * 
	 * @param name             name
	 * @param namespace        namespace
	 * @return                 annotations
	 * @throws Exception       wrong JSON format or invalid value in JSON
	 */
	protected Map<String, String> createAnnotations(String name, String namespace) throws Exception {
		Map<String, String> annotations = new HashMap<String, String>();
		annotations.put(KubevirtConstants.KIND_ANNOTATION, getPlural());
		annotations.put(KubevirtConstants.GROUP_ANNOTATION, getGroup());
		annotations.put(KubevirtConstants.VERSION_ANNOTATION, getVersion());
		annotations.put(KubevirtConstants.NAME_ANNOTATION,name);
		annotations.put(KubevirtConstants.NS_ANNOTATION, namespace);
		return annotations;
	}
	
	/************************************************************************
	 * 
	 *                       Commons
	 * 
	 ************************************************************************/
	
	/**
	 * @return              kind
	 */
	protected String getKind() {
		String classname = getClass().getSimpleName();
		return classname.substring(0, classname.length() - "Watcher".length());
	}
	
	/**
	 * @return               plural
	 */
	public String getPlural() {
		return getKind().toLowerCase() + "s";
	}
	
	/**
	 * @param meta            Metadata
	 * @return                pod name
	 */
	public String getPodName(ObjectMeta meta) {
		return getKind().toLowerCase() + "-" 
				+ meta.getName() + "-" + meta.getNamespace();
	}
	
	/**
	 * @return                 group
	 */
	public String getGroup() {
		return "cloudplus.io";
	}
	
	/**
	 * @return                  version
	 */
	public String getVersion() {
		return "v1alpha3";
	}
	
	
	/**
	 * @param logger             logger
	 * @param cause              cause
	 */
	public void logStopInfo(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop " 
				+ getClass().getSimpleName() + ":" + cause);
	}
	
	
	/**
	 * @param cause               cause
 	 */
	public void onClose(KubernetesClientException cause) {
		logStopInfo(cause);
	}
}
