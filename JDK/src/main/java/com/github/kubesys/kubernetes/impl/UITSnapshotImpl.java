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
import com.github.kubesys.kubernetes.api.model.UITSnapshot;
import com.github.kubesys.kubernetes.api.model.UITSnapshotList;
import com.github.kubesys.kubernetes.api.model.UITSnapshotSpec;
import com.github.kubesys.kubernetes.api.model.UITSnapshotSpec.Lifecycle;
import com.github.kubesys.kubernetes.api.model.UITSnapshotSpec.Lifecycle.CreateUITSnapshot;
import com.github.kubesys.kubernetes.api.model.UITSnapshotSpec.Lifecycle.RecoveryUITSnapshot;
import com.github.kubesys.kubernetes.api.model.UITSnapshotSpec.Lifecycle.RemoveUITSnapshot;

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
public class UITSnapshotImpl {

	/**
	 * m_logger
	 */
	protected final static Logger m_logger = Logger.getLogger(UITSnapshotImpl.class.getName());

	/**
	 * client
	 */
	@SuppressWarnings("rawtypes")
	protected final MixedOperation client = ExtendedKubernetesClient.crdClients
			.get(UITSnapshot.class.getSimpleName());

	/**
	 * support commands
	 */
	public static List<String> cmds = new ArrayList<String>();

	static {
		cmds.add("createUITSnapshot");
		cmds.add("deleteUITSnapshot");
		cmds.add("recoveryUITSnapshot");
	}

	/*************************************************
	 * 
	 * Core
	 * 
	 **************************************************/

	/**
	 * return true or an exception
	 * 
	 * @param snapshot VM snapshot description
	 * @return true or an exception
	 * @throws Exception create VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean create(UITSnapshot snapshot) throws Exception {
		client.create(snapshot);
		m_logger.log(Level.INFO, "create UITSnapshot " + snapshot.getMetadata().getName() + " successful.");
		return true;
	}

	public String getEventId(String name) {
		UITSnapshot vms = get(name);
		return vms.getMetadata().getLabels().get("eventId");
	}
	
	/**
	 * @param snapshot VM snapshot description
	 * @return true or an exception
	 * @throws Exception delete VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean delete(UITSnapshot snapshot) throws Exception {
		client.delete(snapshot);
		m_logger.log(Level.INFO, "delete UITSnapshot " + snapshot.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param snapshot VM snapshot description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	public boolean update(UITSnapshot snapshot) throws Exception {
		client.createOrReplace(snapshot);
		m_logger.log(Level.INFO, "update UITSnapshot " + snapshot.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * @param operator operator
	 * @param snapshot VM snapshot description
	 * @return true or an exception
	 * @throws Exception update VM disk fail
	 */
	@SuppressWarnings("unchecked")
	@Deprecated
	protected boolean update(String operator, UITSnapshot snapshot) throws Exception {
		client.createOrReplace(snapshot);
		m_logger.log(Level.INFO, operator + " " + snapshot.getMetadata().getName() + " successful.");
		return true;
	}

	/**
	 * return an object or null
	 * 
	 * @param name .metadata.name
	 * @return object or null
	 */
	@SuppressWarnings("unchecked")
	public UITSnapshot get(String name) {
		return ((Gettable<UITSnapshot>) client.withName(name)).get();
	}

	/**
	 * @return list all virtual machine snapshots or null
	 */
	public UITSnapshotList list() {
		return (UITSnapshotList) client.list();
	}

	/**
	 * list all VM disks with the specified labels
	 * 
	 * @param filter .metadata.labels
	 * @return all VM snapshots or null
	 */
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public UITSnapshotList list(Map<String, String> labels) {
		return (UITSnapshotList) ((FilterWatchListDeletable) client.withLabels(labels)).list();
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

		UITSnapshot snapshot = get(name);
		if (snapshot == null) {
			m_logger.log(Level.SEVERE, "Snapshot " + name + " not exist.");
			return;
		}

		Map<String, String> tags = snapshot.getMetadata().getLabels();
		tags = (tags == null) ? new HashMap<String, String>() : tags;
		tags.put(key, value);

		update(snapshot);
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

		UITSnapshot snapshot = get(name);
		if (snapshot == null) {
			m_logger.log(Level.SEVERE, "Snapshot " + name + " not exist.");
			return;
		}

		Map<String, String> tags = snapshot.getMetadata().getLabels();
		if (tags != null) {
			tags.remove(key);
		}

		update(snapshot);
	}

	/*************************************************
	 * 
	 * Generated
	 * 
	 **************************************************/

	public boolean createUITSnapshot(String name, CreateUITSnapshot createSnapshot) throws Exception {
		return createUITSnapshot(name, null, createSnapshot);
	}

	public boolean createUITSnapshot(String name, String nodeName, CreateUITSnapshot createSnapshot) throws Exception {
		UITSnapshot kind = new UITSnapshot();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITSnapshot");
		UITSnapshotSpec spec = new UITSnapshotSpec();
		ObjectMeta om = new ObjectMeta();
		if (nodeName != null) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			om.setLabels(labels);
			spec.setNodeName(nodeName);
		}
		om.setName(name);
		kind.setMetadata(om);
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setCreateUITSnapshot(createSnapshot);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deleteUITSnapshot(String name, RemoveUITSnapshot deleteSnapshot) throws Exception {
		UITSnapshot kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		UITSnapshotSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setRemoveUITSnapshot(deleteSnapshot);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}
	
	//------------------------------------------------------
	public boolean createUITSnapshot(String name, CreateUITSnapshot createSnapshot, String eventId) throws Exception {
		return createUITSnapshot(name, null, createSnapshot, eventId);
	}

	public boolean createUITSnapshot(String name, String nodeName, CreateUITSnapshot createSnapshot, String eventId) throws Exception {
		UITSnapshot kind = new UITSnapshot();
		kind.setApiVersion("cloudplus.io/v1alpha3");
		kind.setKind("UITSnapshot");
		UITSnapshotSpec spec = new UITSnapshotSpec();
		ObjectMeta om = new ObjectMeta();
		if (nodeName != null) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			labels.put("eventId", eventId);
			om.setLabels(labels);
			spec.setNodeName(nodeName);
		}
		
		om.setName(name);
		kind.setMetadata(om);
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setCreateUITSnapshot(createSnapshot);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		create(kind);
		return true;
	}

	public boolean deleteUITSnapshot(String name, RemoveUITSnapshot deleteSnapshot, String eventId) throws Exception {
		UITSnapshot kind = get(name);
		Map<String, String> labels = kind.getMetadata().getLabels();
		labels = (labels == null) ? new HashMap<String, String>() : labels;
		labels.put("eventId", eventId);
		kind.getMetadata().setLabels(labels);
		
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			delete(kind);
		}
		
		UITSnapshotSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setRemoveUITSnapshot(deleteSnapshot);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
//		delete(kind);
		return true;
	}
	
	public boolean recoveryUITSnapshot(String name, RecoveryUITSnapshot recoveryUITSnapshot) throws Exception {
		return recoveryUITSnapshot(name, recoveryUITSnapshot, null);
	}
	
	public boolean recoveryUITSnapshot(String name, RecoveryUITSnapshot recoveryUITSnapshot, String eventId) throws Exception {
		UITSnapshot kind = get(name);
		if (kind == null || kind.getSpec().getLifecycle() != null) {
			throw new RuntimeException("VirtualMachineSnapshot" + name + " is not exist or it is in a wrong status");
		}
		
		Map<String, String> labels = kind.getMetadata().getLabels();
		labels = (labels == null) ? new HashMap<String, String>() : labels;
		labels.put("eventId", eventId);
		kind.getMetadata().setLabels(labels);
		
		UITSnapshotSpec spec = kind.getSpec();
		Lifecycle lifecycle = new Lifecycle();
		lifecycle.setRecoveryUITSnapshot(recoveryUITSnapshot);
		spec.setLifecycle(lifecycle);
		kind.setSpec(spec);
		update(kind);
		return true;
	}
}
