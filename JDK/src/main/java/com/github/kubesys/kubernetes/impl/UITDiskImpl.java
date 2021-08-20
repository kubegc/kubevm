/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.impl;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.UITDisk;
import com.github.kubesys.kubernetes.api.model.UITDiskList;
import com.github.kubesys.kubernetes.api.model.UITDiskSpec;
import com.github.kubesys.kubernetes.api.model.UITDiskSpec.Lifecycle;
import com.github.kubesys.kubernetes.api.model.UITDiskSpec.Lifecycle.CreateUITDisk;
import com.github.kubesys.kubernetes.api.model.UITDiskSpec.Lifecycle.DeleteUITDisk;
import com.github.kubesys.kubernetes.api.model.UITDiskSpec.Lifecycle.ExpandUITDisk;

import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.client.dsl.FilterWatchListDeletable;
import io.fabric8.kubernetes.client.dsl.Gettable;
import io.fabric8.kubernetes.client.dsl.MixedOperation;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @author xianghao16@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @since Thu Jun 13 21:39:55 CST 2019
 **/
@Deprecated
public class UITDiskImpl {

	/**
	 * m_logger
	 */
	protected final static Logger m_logger = Logger.getLogger(UITDiskImpl.class.getName());

	/**
	 * client
	 */
	@SuppressWarnings("rawtypes")
	protected final MixedOperation client = ExtendedKubernetesClient.crdClients
			.get(UITDisk.class.getSimpleName());

	/**
	 * support commands
	 */
	public static List<String> cmds = new ArrayList<String>();

	static {
		cmds.add("createUITDisk");
		cmds.add("deleteUITDisk");
		cmds.add("expandUITDisk");
	}

	/*************************************************
	 * 
	 * Core
	 * 
	 **************************************************/

	/**
	 * return true or an exception
	 * 
	 * @param disk VM disk description
	 * @return true or an exception
	 * @throws Exception create VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean create(UITDisk disk) throws Exception {
		client.create(disk);
		m_logger.log(Level.INFO, "create UITDisk " + disk.getMetadata().getName() + " successful.");
		return true;
	}

	public String getEventId(String name) {
		UITDisk vmd = get(name);
		return vmd.getMetadata().getLabels().get("eventId");
	}
	
	/**
	 * @param disk VM disk description
	 * @return true or an exception
	 * @throws Exception delete VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean delete(UITDisk disk) throws Exception {
		client.delete(disk);
		m_logger.log(Level.INFO, "delete UITDisk " + disk.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param disk VM disk description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean update(UITDisk disk) throws Exception {
		client.createOrReplace(disk);
		m_logger.log(Level.INFO, "update VirtualMachine " + disk.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param operator operator
	 * @param disk     VM disk description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	protected boolean update(String operator, UITDisk disk) throws Exception {
		client.createOrReplace(disk);
		m_logger.log(Level.INFO, operator + " " + disk.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * return an object or null
	 * 
	 * @param name .metadata.name
	 * @return object or null
	 */
	@SuppressWarnings("unchecked")
	public UITDisk get(String name) {
		return ((Gettable<UITDisk>) client.withName(name)).get();
	}

	/**
	 * @return list all virtual machine disks or null
	 */
	public UITDiskList list() {
		return (UITDiskList) client.list();
	}

	/**
	 * list all VM disks with the specified labels
	 * 
	 * @param filter .metadata.labels
	 * @return all VM disk or null
	 */
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public UITDiskList list(Map<String, String> labels) {
		return (UITDiskList) ((FilterWatchListDeletable) client.withLabels(labels)).list();
	}

	/**
	 * @param name  name
	 * @param key   key
	 * @param value value
	 * @throws Exception exception
	 */
	public void addTag(String name, String key, String value) throws Exception {

		if (key.equals("host")) {
			m_logger.log(Level.SEVERE, "'host' is a keyword.");
			return;
		}

		UITDisk disk = get(name);
		if (disk == null) {
			m_logger.log(Level.SEVERE, "Disk" + name + " not exist.");
			return;
		}

		Map<String, String> tags = disk.getMetadata().getLabels();
		tags = (tags == null) ? new HashMap<String, String>() : tags;
		tags.put(key, value);
		update(disk);
	}

	/**
	 * @param name name
	 * @param key  key
	 * @throws Exception exception
	 */
	public void deleteTag(String name, String key) throws Exception {

		if (key.equals("host")) {
			m_logger.log(Level.SEVERE, "'host' is a keyword.");
			return;
		}

		UITDisk disk = get(name);
		if (disk == null) {
			m_logger.log(Level.SEVERE, "Disk " + name + " not exist.");
			return;
		}

		Map<String, String> tags = disk.getMetadata().getLabels();
		if (tags != null) {
			tags.remove(key);
		}

		update(disk);
	}

	/*************************************************
	 * 
	 * Generated
	 * 
	 **************************************************/

	public boolean createDisk(String name, CreateUITDisk createDisk) throws Exception {
		return createDisk(name, null, createDisk);
	}

	public boolean createDisk(String name, String nodeName, CreateUITDisk createDisk) throws Exception {
		UITDisk kind = new UITDisk();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITDisk");
		UITDiskSpec spec = new UITDiskSpec();
		ObjectMeta om = new ObjectMeta();
		om.setName(name);
		if (nodeName != null) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			om.setLabels(labels);
			spec.setNodeName(nodeName);
		}
		kind.setMetadata(om);
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setCreateUITDisk(createDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deleteDisk(String name, DeleteUITDisk deleteDisk) throws Exception {
		UITDisk kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		UITDiskSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setDeleteUITDisk(deleteDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}

	public boolean resizeDisk(String name, ExpandUITDisk resizeDisk) throws Exception {
		UITDisk kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			throw new RuntimeException("UITDisk" + name + " is not exist or it is in a wrong status");
		}
		UITDiskSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setExpandUITDisk(resizeDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update("resizeDisk ", kind);
		return true;
	}

	
	//------------------------------------------------
	public boolean createDisk(String name, CreateUITDisk createDisk, String eventId) throws Exception {
		return createDisk(name, null, createDisk, eventId);
	}

	public boolean createDisk(String name, String nodeName, CreateUITDisk createDisk, String eventId) throws Exception {
		UITDisk kind = new UITDisk();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITDisk");
		UITDiskSpec spec = new UITDiskSpec();
		ObjectMeta om = new ObjectMeta();
		om.setName(name);
		if (nodeName != null) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			labels.put("eventId", eventId);
			om.setLabels(labels);
			spec.setNodeName(nodeName);
		}
		kind.setMetadata(om);
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setCreateUITDisk(createDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deleteDisk(String name, DeleteUITDisk deleteDisk, String eventId) throws Exception {
		UITDisk kind = get(name);
		Map<String, String> labels = kind.getMetadata().getLabels();
		labels = (labels == null) ? new HashMap<String, String>() : labels;
		labels.put("eventId", eventId);
		kind.getMetadata().setLabels(labels);
		
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		
		UITDiskSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setDeleteUITDisk(deleteDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}

	public boolean resizeDisk(String name, ExpandUITDisk resizeDisk, String eventId) throws Exception {
		UITDisk kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			throw new RuntimeException("UITDisk" + name + " is not exist or it is in a wrong status");
		}
		Map<String, String> labels = kind.getMetadata().getLabels();
		labels = (labels == null) ? new HashMap<String, String>() : labels;
		labels.put("eventId", eventId);
		kind.getMetadata().setLabels(labels);
		
		UITDiskSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setExpandUITDisk(resizeDisk);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update("resizeDisk ", kind);
		return true;
	}

	
}