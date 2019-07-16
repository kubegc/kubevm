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
import com.github.kubesys.kubernetes.api.model.VirtualMachineDisk;

import io.fabric8.kubernetes.api.model.Container;
import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.api.model.PodSpec;
import io.fabric8.kubernetes.api.model.Quantity;
import io.fabric8.kubernetes.api.model.ResourceRequirements;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed July 08 17:26:22 CST 2019
 * 
 *        https://www.json2yaml.com/ http://www.bejson.com/xml2json/
 * 
 *        debug at runWatch method of
 *        io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class VirtualMachineDiskWatcher extends AbstractWatcher implements Watcher<VirtualMachineDisk> {

	protected final static Logger m_logger = Logger.getLogger(VirtualMachineDiskWatcher.class.getName());

	public VirtualMachineDiskWatcher(ExtendedKubernetesClient client) {
		super(client);
	}

	// actions
	public final static String ACTION_CREATE = "ADDED";

	public final static String ACTION_REMOVE = "DELETED";

	// pod attributions
	public final static String POD_PREFIX = "disk2pod";

	public final static String POD_NAMESPACE = "default";
	
	public void eventReceived(Action action, VirtualMachineDisk disk) {

		String namespace = disk.getMetadata().getNamespace();
		String podName = POD_PREFIX + "-" + disk.getMetadata().getName() + "-" + namespace;
		
		if (action.toString().equals(ACTION_CREATE)) {
			Pod pod = null;;
			try {
				pod = createPod(disk, podName);
			} catch (Exception e) {
				e.printStackTrace();
			}
			
			if (client.pods().inNamespace(namespace).withName(podName).get() == null) {

				client.pods().inNamespace(namespace).create(pod);
				m_logger.log(Level.INFO, "Create Disk '" + disk.getMetadata().getName() + "' in namespace '"
						+ disk.getMetadata().getNamespace() + "'");
				m_logger.log(Level.INFO, "Create Pod '" + podName + "' in namespace '" + namespace + "'");
			}
		} else if (action.toString().equals(ACTION_REMOVE)) {
			if (client.pods().inNamespace(namespace).withName(podName).get() != null) {
				client.pods().inNamespace(namespace).withName(podName).delete();
				m_logger.log(Level.INFO, "Delete Pod '" + podName + "' in namespace '" + namespace + "'");
				m_logger.log(Level.INFO, "Delete Disk '" + disk.getMetadata().getName() + "' in namespace '"
						+ disk.getMetadata().getNamespace() + "'");
			}
		}
	}

	private Pod createPod(VirtualMachineDisk disk, String podName) throws Exception {
		Pod pod = new Pod();
		// metadata and podSpec
		pod.setMetadata(createMetadataFrom(disk, podName));
		pod.setSpec(createPodSpecFrom(disk, podName));
		return pod;
	}

	// default values

	public final static String DEFAULT_SCHEDULER = "kubevirt-scheduler";

	private PodSpec createPodSpecFrom(VirtualMachineDisk disk, String podName) {
		PodSpec spec = new PodSpec();
		spec.setContainers(createContainerFrom(disk, podName));
		spec.setSchedulerName(System.getProperty("scheduler-name", DEFAULT_SCHEDULER));
		return spec;
	}

	public final static String DEFAULT_IMAGE = "fake";

	private List<Container> createContainerFrom(VirtualMachineDisk disk, String podName) {
		List<Container> containers = new ArrayList<Container>();
		Container container = new Container();
		container.setName(podName);
		container.setImage(DEFAULT_IMAGE);
		container.setResources(createResourceDemands(disk));
		containers.add(container);
		return containers;
	}

	// resources
	public final static String CPU_RESOURCE = "cpu";

	public final static String RAM_RESOURCE = "memory";

	private ResourceRequirements createResourceDemands(VirtualMachineDisk disk) {
		ResourceRequirements resources = new ResourceRequirements();
		Map<String, Quantity> requests = new HashMap<String, Quantity>();
		requests.put(CPU_RESOURCE, new Quantity("100m"));
		requests.put(RAM_RESOURCE, new Quantity("64Mi"));
		resources.setRequests(requests);
		return resources;
	}

	private ObjectMeta createMetadataFrom(VirtualMachineDisk disk, String podName) throws Exception {
		ObjectMeta metadata = new ObjectMeta();
		metadata.setName(podName);
		metadata.setAnnotations(createAnnotations(disk));
		return metadata;
	}

	// annotations
	public final static String KIND_ANNOTATION = "crdKind";

	public final static String NS_ANNOTATION = "crdNamespace";

	public final static String VERSION_ANNOTATION = "crdVersion";

	public final static String GROUP_ANNOTATION = "crdGroup";

	public final static String NAME_ANNOTATION = "crdName";

	public final static String CONTENT_ANNOTATION = "crdYaml";

	public final static String PLURAL = "virtualmachinedisks";

	public final static String GROUP = "cloudplus.io";

	public final static String VERSION = "v1alpha3";
	

	private Map<String, String> createAnnotations(VirtualMachineDisk disk) throws Exception {
		Map<String, String> annotations = new HashMap<String, String>();
		annotations.put(KIND_ANNOTATION, PLURAL);
		annotations.put(GROUP_ANNOTATION, GROUP);
		annotations.put(VERSION_ANNOTATION, VERSION);
		annotations.put(NAME_ANNOTATION, disk.getMetadata().getName());
		annotations.put(NS_ANNOTATION, disk.getMetadata().getNamespace());
		annotations.put(CONTENT_ANNOTATION, JSON.toJSONString(disk.getSpec()));
		return annotations;
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop VirtualMachineDiskWatcher");
	}

}
