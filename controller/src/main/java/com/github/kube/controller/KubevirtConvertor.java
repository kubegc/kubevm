/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import io.fabric8.kubernetes.api.model.Affinity;
import io.fabric8.kubernetes.api.model.Container;
import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodSpec;
import io.fabric8.kubernetes.api.model.ResourceRequirements;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * 
 * KubevirtConvertor is used for converting VM-related CRD to Pod.
 * 
 **/
public class KubevirtConvertor {
	
	/**
	 * @param om                         CRD's ObjectMeta
	 * @param annotations                annotations
	 * @param spec                       CRD's Spec
	 * @param resInfo                    resource demands
	 * @param nodeSelector               node selector
	 * @param nodeName                   node name
	 * @param podName                    pod name
	 * @return                           Pod
	 * @throws Exception                 exception
	 */
	protected Pod createPod(ObjectMeta om, Map<String, String> annotations, Object spec, ResourceRequirements resInfo, Map<String, String> nodeSelector, Affinity affinity, String podName) throws Exception {
		Pod pod = new Pod();
		// metadata and podSpec
		pod.setMetadata(createMetadataFrom(om, annotations, spec, podName));
		pod.setSpec(createPodSpecFrom(resInfo, nodeSelector, affinity, podName));
		return pod;
	}
	
	/************************************************************************
	 * 
	 *                       Pod's ObjectMeta
	 * 
	 ************************************************************************/
	
	/**
	 * @param meta                       CRD's ObjectMeta
	 * @param anns                       annotations
	 * @param spec                       CRD's Spec
	 * @param name                       pod name
	 * @return                           pod ObjectMeta
	 * @throws Exception                 exception
	 */
	protected ObjectMeta createMetadataFrom(ObjectMeta meta, Map<String, String> anns, 
											Object spec, String name) throws Exception {
		ObjectMeta metadata = new ObjectMeta();
		metadata.setName(name);
		metadata.setLabels(meta.getLabels());
		metadata.setAnnotations(anns);
		return metadata;
	}
	
	
	/************************************************************************
	 * 
	 *                       Pod's Spec
	 * 
	 ************************************************************************/
	
	/**
	 * convert CRD to Pod spec
	 * 
	 * @param resInfo            resource info     
	 * @param nodeName           node name
	 * @param nodeSelector       node selector
	 * @param podName            pod name
	 * @return  PodSpec object
	 */
	
	/**
	 * scheduler name
	 */
	public final static String DEFAULT_SCHEDULER        = "kubevirt-scheduler";
	
	
	protected PodSpec createPodSpecFrom(ResourceRequirements resInfo, Map<String, String> nodeSelector, Affinity affinity, String podName) {
		PodSpec spec = new PodSpec();
		spec.setNodeSelector(nodeSelector);
		spec.setAffinity(affinity);
		spec.setContainers(createContainerFrom(resInfo, podName));
		spec.setSchedulerName(System.getProperty(
							"scheduler-name", DEFAULT_SCHEDULER));
		return spec;
	}
	
	/**
	 * image
	 */
	public final static String DEFAULT_IMAGE = "fake";
	
	/**
	 * convert CRD to Pod's container
	 * 
	 * @param resInfo         resource info     
	 * @param podName         pod name
	 * @return                containers
	 */
	protected List<Container> createContainerFrom(ResourceRequirements resInfo, String podName) {
		List<Container> containers = new ArrayList<Container>();
		Container container = new Container();
		container.setName(podName);
		container.setImage(DEFAULT_IMAGE);
		container.setResources(resInfo);
		containers.add(container);
		return containers;
	}
	
}
