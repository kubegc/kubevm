/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.watchers;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineDisk;

import io.fabric8.kubernetes.api.model.Container;
import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodSpec;
import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed July 08 17:26:22 CST 2019
 * 
 **/
public abstract class AbstractWatcher {

	protected final ExtendedKubernetesClient client;

	// actions
	public final static String ACTION_CREATE = "ADDED";

	public final static String ACTION_REMOVE = "DELETED";
	
	public final static String POD_NAMESPACE = "default";

	public AbstractWatcher(ExtendedKubernetesClient client) {
		super();
		this.client = client;
	}
	
	public abstract String getPrefix();
	
	public abstract String getPlural();
	
	public abstract ResourceRequirements getResourceDemands(Object spec);
	
	public String getGroup() {
		return "cloudplus.io";
	}
	
	public String getVersion() {
		return "v1alpha3";
	}
	
	protected Pod createPod(ObjectMeta om, Object spec, String podName) throws Exception {
		Pod pod = new Pod();
		// metadata and podSpec
		pod.setMetadata(createMetadataFrom(om, om, podName));
		pod.setSpec(createPodSpecFrom(spec, podName));
		return pod;
	}
	
	protected ObjectMeta createMetadataFrom(ObjectMeta om, Object spec, String podName) throws Exception {
		ObjectMeta metadata = new ObjectMeta();
		metadata.setName(podName);
		metadata.setAnnotations(createAnnotations(om, spec));
		return metadata;
	}
	
	/*************************************
	 * 
	 *************************************/
	
	public final static String DEFAULT_IMAGE = "fake";

	protected List<Container> createContainerFrom(Object spec, String podName) {
		List<Container> containers = new ArrayList<Container>();
		Container container = new Container();
		container.setName(podName);
		container.setImage(DEFAULT_IMAGE);
		container.setResources(getResourceDemands(spec));
		containers.add(container);
		return containers;
	}
	
	/*************************************
	 * 
	 *************************************/
	
	public final static String CPU_RESOURCE = "cpu";

	public final static String RAM_RESOURCE = "memory";
	
	public final static String DEFAULT_SCHEDULER = "kubevirt-scheduler";

	protected PodSpec createPodSpecFrom(Object obj, String podName) {
		PodSpec spec = new PodSpec();
		spec.setContainers(createContainerFrom(obj, podName));
		spec.setSchedulerName(System.getProperty("scheduler-name", DEFAULT_SCHEDULER));
		return spec;
	}

	/*************************************
	 * 
	 *************************************/
	
	public final static String KIND_ANNOTATION = "crdKind";

	public final static String NS_ANNOTATION = "crdNamespace";

	public final static String VERSION_ANNOTATION = "crdVersion";

	public final static String GROUP_ANNOTATION = "crdGroup";

	public final static String NAME_ANNOTATION = "crdName";

	public final static String CONTENT_ANNOTATION = "crdYaml";
	
	protected Map<String, String> createAnnotations(ObjectMeta om, Object spec) throws Exception {
		Map<String, String> annotations = new HashMap<String, String>();
		annotations.put(KIND_ANNOTATION, getPlural());
		annotations.put(GROUP_ANNOTATION, getGroup());
		annotations.put(VERSION_ANNOTATION, getVersion());
		annotations.put(NAME_ANNOTATION, om.getName());
		annotations.put(NS_ANNOTATION, om.getNamespace());
		annotations.put(CONTENT_ANNOTATION, JSON.toJSONString(spec));
		return annotations;
	}
}
