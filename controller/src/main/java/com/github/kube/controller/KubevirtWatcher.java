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
	
	
	/**
	 * @param spec            spec
	 * @return                container's resource requirements
	 */
	public abstract ResourceRequirements getResourceDemands(Object spec);

	/**
	 * @param action           action
	 * @param om               om
	 * @param spec             spec
	 */
	public void eventReceived(Action action, ObjectMeta om, Object spec) {
		try {
			ExtendedCustomResourceDefinitionSpec extSpec = (ExtendedCustomResourceDefinitionSpec) spec;
			Pod pod = convertor.createPod(om, createAnnotations(om), 
					                     spec, getResourceDemands(spec), 
					                     extSpec.getNodeSelector(), 
					                     extSpec.getAffinity(), 
					                     getPodName(om));
			executor.execute(client, action, getWatcherType(), pod);
		} catch (Exception ex) {
			m_logger.log(Level.SEVERE, ex.toString());
		}
	}
	
	/**
	 * 
	 * convert CRD to Pod annotations
	 * 
	 * @param om               CRD objectMeta
	 * @return                 annotations
	 * @throws Exception       wrong JSON format or invalid value in JSON
	 */
	protected Map<String, String> createAnnotations(ObjectMeta om) throws Exception {
		Map<String, String> annotations = new HashMap<String, String>();
		annotations.put(KubevirtConstants.KIND_ANNOTATION, getPlural());
		annotations.put(KubevirtConstants.GROUP_ANNOTATION, getGroup());
		annotations.put(KubevirtConstants.VERSION_ANNOTATION, getVersion());
		annotations.put(KubevirtConstants.NAME_ANNOTATION, om.getName());
		annotations.put(KubevirtConstants.NS_ANNOTATION, om.getNamespace());
		return annotations;
	}
	
	/**
	 * @return               plural
	 */
	public String getPlural() {
		return getWatcherType() + "s";
	}
	
	/**
	 * @param data            Metadata
	 * @return                pod name
	 */
	public String getPodName(ObjectMeta data) {
		return getWatcherType() + "-" + data.getName() 
					+ "-" + data.getNamespace();
	}
	
	/**
	 * @return
	 */
	protected String getWatcherType() {
		String classname = getClass().getSimpleName().toLowerCase();
		return classname.substring(0, classname.length() - "Watcher".length());
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
