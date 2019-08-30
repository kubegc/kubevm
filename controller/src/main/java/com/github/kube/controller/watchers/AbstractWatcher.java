/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.ExtendedCustomResourceDefinitionSpec;

import io.fabric8.kubernetes.api.model.Container;
import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodSpec;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since Wed Aug 29 17:26:22 CST 2019
 * 
 * AbstractWatcher provides a common method to convert VM-related CRD to Pod. 
 **/
public abstract class AbstractWatcher {

	/**
	 * m_logger
	 */
	protected final static Logger m_logger = Logger.getLogger(VirtualMachineWatcher.class.getName());
	
	/**
	 * Kubernetes client
	 */
	protected final ExtendedKubernetesClient client;

	/**
	 * pod action is ADDED
	 */
	public final static String ACTION_ADDED = "ADDED";

	/**
	 * pod action is DELETED
	 */
	public final static String ACTION_DELETED = "DELETED";
	
	/**
	 * pod namespace
	 */
	public final static String POD_NAMESPACE = "default";

	/**
	 * @param client           client
	 */
	public AbstractWatcher(ExtendedKubernetesClient client) {
		super();
		this.client = client;
	}
	
	
	/**
	 * @param om                      CRD's ObjectMeta
	 * @param spec                    CRD's Spec
	 * @param nodeSelector            node selector
	 * @param nodeName                node name
	 * @param podName                 pod name
	 * @return                        Pod
	 * @throws Exception              exception
	 */
	protected Pod createPod(ObjectMeta om, Object spec, Map<String, String> nodeSelector, String podName) throws Exception {
		Pod pod = new Pod();
		// metadata and podSpec
		pod.setMetadata(createMetadataFrom(om, spec, podName));
		pod.setSpec(createPodSpecFrom(spec, nodeSelector, podName));
		return pod;
	}
	
	/*************************************
	 * 
	 *  convert CRD to Pod's metadata
	 * 
	 *************************************/
	
	/**
	 * @param om                         CRD's ObjectMeta
	 * @param spec                       CRD's Spec
	 * @param podName                    pod name
	 * @return                           pod ObjectMeta
	 * @throws Exception                 exception
	 */
	protected ObjectMeta createMetadataFrom(ObjectMeta om, Object spec, String podName) throws Exception {
		ObjectMeta metadata = new ObjectMeta();
		metadata.setName(podName);
		metadata.setLabels(om.getLabels());
		metadata.setAnnotations(createAnnotations(om, spec));
		return metadata;
	}
	
	/*************************************
	 * 
	 *  convert CRD to Pod's container
	 * 
	 *************************************/
	
	/**
	 * image
	 */
	public final static String DEFAULT_IMAGE = "fake";
	
	/**
	 * @param resInfo         resource info
	 * @return                container's resource requirements
	 */
	public abstract ResourceRequirements getResourceDemands(Object resInfo);

	/**
	 * convert CRD to Pod's container
	 * 
	 * @param resInfo         resource info     
	 * @param podName         pod name
	 * @return                containers
	 */
	protected List<Container> createContainerFrom(Object resInfo, String podName) {
		List<Container> containers = new ArrayList<Container>();
		Container container = new Container();
		container.setName(podName);
		container.setImage(DEFAULT_IMAGE);
		container.setResources(getResourceDemands(resInfo));
		containers.add(container);
		return containers;
	}
	
	/*************************************
	 * 
	 *  convert CRD to Pod spec
	 * 
	 *************************************/
	
	/**
	 * CPU demand
	 */
	public final static String CPU_RESOURCE             = "cpu";

	/**
	 * RAM demand
	 */
	public final static String RAM_RESOURCE             = "memory";
	
	/**
	 * scheduler name
	 */
	public final static String DEFAULT_SCHEDULER        = "kubevirt-scheduler";

	/**
	 * convert CRD to Pod spec
	 * 
	 * @param resInfo            resource info     
	 * @param nodeName           node name
	 * @param nodeSelector       node selector
	 * @param podName            pod name
	 * @return  PodSpec object
	 */
	protected PodSpec createPodSpecFrom(Object resInfo, Map<String, String> nodeSelector, String podName) {
		PodSpec spec = new PodSpec();
		spec.setNodeSelector(nodeSelector);
		spec.setContainers(createContainerFrom(resInfo, podName));
		spec.setSchedulerName(System.getProperty("scheduler-name", DEFAULT_SCHEDULER));
		return spec;
	}

	/*************************************
	 * 
	 *  convert CRD to Pod annotations
	 * 
	 *************************************/
	
	/**
	 * CRD's kind
	 */
	public final static String KIND_ANNOTATION       = "crdKind";

	/**
	 * CRD's namespace
	 */
	public final static String NS_ANNOTATION         = "crdNamespace";

	/**
	 * CRD's version
	 */
	public final static String VERSION_ANNOTATION    = "crdVersion";

	/**
	 * CRD's group
	 */
	public final static String GROUP_ANNOTATION      = "crdGroup";

	/**
	 * CRD's metadata name
	 */
	public final static String NAME_ANNOTATION       = "crdName";
	
	
	/**
	 * @return      prefix
	 */
	public String getPrefix() {
		return getWatcherType() + "-";
	}
	
	/**
	 * @return       plural
	 */
	public String getPlural() {
		return getWatcherType() + "s";
	}


	/**
	 * @return
	 */
	protected String getWatcherType() {
		String classname = getClass().getSimpleName().toLowerCase();
		return classname.substring(0, classname.length() - "Watcher".length());
	}
	
	/**
	 * @return       group
	 */
	public String getGroup() {
		return "cloudplus.io";
	}
	
	/**
	 * @return       version
	 */
	public String getVersion() {
		return "v1alpha3";
	}
	
	/**
	 * 
	 * convert CRD to Pod annotations
	 * 
	 * @param om               CRD objectMeta
	 * @param spec             CRD spec 
	 * @return                 annotations
	 * @throws Exception       wrong JSON format or invalid value in JSON
	 */
	protected Map<String, String> createAnnotations(ObjectMeta om, Object spec) throws Exception {
		Map<String, String> annotations = new HashMap<String, String>();
		annotations.put(KIND_ANNOTATION, getPlural());
		annotations.put(GROUP_ANNOTATION, getGroup());
		annotations.put(VERSION_ANNOTATION, getVersion());
		annotations.put(NAME_ANNOTATION, om.getName());
		annotations.put(NS_ANNOTATION, om.getNamespace());
		return annotations;
	}
	
	/*************************************
	 * 
	 *  Some common methods
	 * 
	 *************************************/
	
	/**
	 * @param logger             logger
	 * @param cause              cause
	 */
	public void logStopInfo(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop " 
				+ getClass().getSimpleName() + ":" + cause);
	}
	
	
	/**
	 * @param podName         pod name
	 */
	public void logCreateInfo(String podName) {
		m_logger.log(Level.INFO, "Create Pod '" + podName + "' in namespace '" + POD_NAMESPACE + "'");
	}
	
	/**
	 * @param podName         pod name
	 */
	public void logDeleteInfo(String podName) {
		m_logger.log(Level.INFO, "Delete Pod '" + podName + "' in namespace '" + POD_NAMESPACE + "'");
	}
	
	/**
	 * @param data            Metadata
	 * @return                pod name
	 */
	public String getPodName(ObjectMeta data) {
		return getPrefix() + "-" + data.getName() 
					+ "-" + data.getNamespace();
	}
	
	/**
	 * @param action        action
	 * @param objMeta       object metadata
	 * @param spec          spec
	 */
	public void doConvert(String action, ObjectMeta objMeta, 
				ExtendedCustomResourceDefinitionSpec spec) {

		// if user assign a node for a CRD, then
		// our process will skip the scheduling step
		if (spec.getNodeName() != null) {
			return;
		}
		
		// if it is a 'ADDED' command, 
		// we will create a pod based on the CRD's info 
		String podName = getPodName(objMeta);
		if (action.equals(ACTION_ADDED)) {
			try {
				Pod pod = createPod(objMeta, spec, spec.getNodeSelector(), podName);
				doCreate(podName, pod);
			} catch (Exception e) {
				// this means we cannot create a pod based on the CRD's info 
				m_logger.log(Level.SEVERE, "cannot create object because of " + e);
				doDelete(podName);
			}
		} else if (action.equals(ACTION_DELETED)) {
			doDelete(podName);
		}
	}


	/**
	 * @param podName            pod name
	 */
	protected void doDelete(String podName) {
		if (client.pods().inNamespace(POD_NAMESPACE).withName(podName).get() != null) {
			client.pods().inNamespace(POD_NAMESPACE).withName(podName).delete();
			logDeleteInfo(podName);
		}
	}


	/**
	 * @param podName            pod name
	 * @param pod                pod
	 */
	protected void doCreate(String podName, Pod pod) {
		if (client.pods().inNamespace(POD_NAMESPACE).withName(podName).get() == null) {
			client.pods().inNamespace(POD_NAMESPACE).create(pod);
			logCreateInfo(podName);
		}
	}
}
