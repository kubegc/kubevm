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
import com.github.kubesys.kubernetes.api.model.UITStoragePool;
import com.github.kubesys.kubernetes.api.model.UITStoragePoolList;
import com.github.kubesys.kubernetes.api.model.UITStoragePoolSpec;
import com.github.kubesys.kubernetes.api.model.UITStoragePoolSpec.Lifecycle;
import com.github.kubesys.kubernetes.api.model.UITStoragePoolSpec.Lifecycle.CreateUITPool;
import com.github.kubesys.kubernetes.api.model.UITStoragePoolSpec.Lifecycle.DeleteUITPool;

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
public class UITPoolImpl {

	/**
	 * m_logger
	 */
	protected final static Logger m_logger = Logger.getLogger(UITPoolImpl.class.getName());

	/**
	 * client
	 */
	@SuppressWarnings("rawtypes")
	protected final MixedOperation client = ExtendedKubernetesClient.crdClients
			.get(UITStoragePool.class.getSimpleName());

	/**
	 * support commands
	 */
	public static List<String> cmds = new ArrayList<String>();

	static {
		cmds.add("createUITPool");
		cmds.add("deleteUITPool");
	}

	/*************************************************
	 * 
	 * Core
	 * 
	 **************************************************/

	/**
	 * return true or an exception
	 * 
	 * @param pool VM disk description
	 * @return true or an exception
	 * @throws Exception create VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean create(UITStoragePool pool) throws Exception {
		client.create(pool);
		m_logger.log(Level.INFO, "create VirtualMachinePool " + pool.getMetadata().getName() + " successful.");
		return true;
	}

	public String getEventId(String pool) {
		UITStoragePool uitp = get(pool);
		return uitp.getMetadata().getLabels().get("eventId");
	}
	
	/**
	 * @param pool VM disk description
	 * @return true or an exception
	 * @throws Exception delete VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean delete(UITStoragePool pool) throws Exception {
		client.delete(pool);
		m_logger.log(Level.INFO, "delete VirtualMachinePool " + pool.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param pool VM disk description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean update(UITStoragePool pool) throws Exception {
		client.createOrReplace(pool);
		m_logger.log(Level.INFO, "update VirtualMachinePool " + pool.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param operator operator
	 * @param pool     VM disk description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	protected boolean update(String operator, UITStoragePool pool) throws Exception {
		client.createOrReplace(pool);
		m_logger.log(Level.INFO, operator + " " + pool.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * return an object or null
	 * 
	 * @param name .metadata.name
	 * @return object or null
	 */
	@SuppressWarnings("unchecked")
	public UITStoragePool get(String name) {
		return ((Gettable<UITStoragePool>) client.withName(name)).get();
	}

	/**
	 * @return list all virtual machine disks or null
	 */
	public UITStoragePoolList list() {
		return (UITStoragePoolList) client.list();
	}

	/**
	 * list all VM disks with the specified labels
	 * 
	 * @param filter .metadata.labels
	 * @return all VM disk or null
	 */
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public UITStoragePoolList list(Map<String, String> labels) {
		return (UITStoragePoolList) ((FilterWatchListDeletable) client.withLabels(labels)).list();
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

		UITStoragePool pool = get(name);
		if (pool == null) {
			m_logger.log(Level.SEVERE, "Disk" + name + " not exist.");
			return;
		}

		Map<String, String> tags = pool.getMetadata().getLabels();
		tags = (tags == null) ? new HashMap<String, String>() : tags;
		tags.put(key, value);
		update(pool);
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

		UITStoragePool pool = get(name);
		if (pool == null) {
			m_logger.log(Level.SEVERE, "Disk " + name + " not exist.");
			return;
		}

		Map<String, String> tags = pool.getMetadata().getLabels();
		if (tags != null) {
			tags.remove(key);
		}

		update(pool);
	}

	/*************************************************
	 * 
	 * Generated
	 * 
	 **************************************************/

	public boolean createPool(String name, CreateUITPool createPool) throws Exception {
		return createPool(name, null, createPool);
	}

	public boolean createPool(String name, String nodeName, CreateUITPool createPool) throws Exception {
		UITStoragePool kind = new UITStoragePool();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITStoragePool");
		UITStoragePoolSpec spec = new UITStoragePoolSpec();
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
		lifecycle.setCreateUITPool(createPool);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deletePool(String name, DeleteUITPool deletePool) throws Exception {
		UITStoragePool kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		UITStoragePoolSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setDeleteUITPool(deletePool);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}

	//------------------------------------------------
	public boolean createPool(String name, CreateUITPool createPool, String eventId) throws Exception {
		return createPool(name, null, createPool, eventId);
	}

	public boolean createPool(String name, String nodeName, CreateUITPool createPool, String eventId) throws Exception {
		UITStoragePool kind = new UITStoragePool();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITStoragePool");
		UITStoragePoolSpec spec = new UITStoragePoolSpec();
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
		lifecycle.setCreateUITPool(createPool);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deletePool(String name, DeleteUITPool deletePool, String eventId) throws Exception {
		UITStoragePool kind = get(name);
		Map<String, String> labels = kind.getMetadata().getLabels();
		labels = (labels == null) ? new HashMap<String, String>() : labels;
		labels.put("eventId", eventId);
		kind.getMetadata().setLabels(labels);
		
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		
		UITStoragePoolSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setDeleteUITPool(deletePool);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}

}