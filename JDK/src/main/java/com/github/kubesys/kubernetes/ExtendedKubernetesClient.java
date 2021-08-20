/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes;

import java.io.ByteArrayInputStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.api.model.*;
import com.github.kubesys.kubernetes.impl.*;

import io.fabric8.kubernetes.api.model.HasMetadata;
import io.fabric8.kubernetes.api.model.KubernetesResource;
import io.fabric8.kubernetes.api.model.apiextensions.CustomResourceDefinition;
import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.CustomResource;
import io.fabric8.kubernetes.client.CustomResourceDoneable;
import io.fabric8.kubernetes.client.CustomResourceList;
import io.fabric8.kubernetes.client.DefaultKubernetesClient;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.dsl.MixedOperation;
import io.fabric8.kubernetes.client.dsl.ParameterNamespaceListVisitFromServerGetDeleteRecreateWaitApplicable;
import io.fabric8.kubernetes.internal.KubernetesDeserializer;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/3
 *
 * <code>ExtendedKubernetesClient<code> extends <code>DefaultKubernetesClient<code>
 * to provide the lifecycle of VirtualMachine, VirtualMachinePool, VirtualMachineDisk,
 * VirtualMachineImage, VirtualMachineSnapshot, VirtualMachineNetwork
 * 
 */
public class ExtendedKubernetesClient extends DefaultKubernetesClient {

	/**
	 * m_logger
	 */
	public final static Logger m_logger = Logger.getLogger(ExtendedKubernetesClient.class.getName());

	/**
	 * root package
	 */
	public final static String ROOT_PKG = ExtendedKubernetesClient.class.getPackage().getName();

	/**
	 * sub-package
	 */
	public final static String SUB_PKG = ".api.model.";

	/**
	 * all watchers
	 */
	@SuppressWarnings("rawtypes")
	public final static Map<String, MixedOperation> crdClients = new HashMap<String, MixedOperation>();

	/**
	 * all configurations
	 */
	public final static List<String> configs = new ArrayList<String>();
	
	/**
	 * @param config     the configuration contains token, 
	 */
	public ExtendedKubernetesClient(Config config)  {
		super(config);
		initKube();
	}

	/***************************************************************
	 * 
	 *                        Core
	 * 
	 * 1. initKube: read and initialize all configuration in variable configs. 
	 *    1.1 loadConfigFile:     load each configuration
	 *    1.2 registerCrdToKube:  register each configuration as a Kubernetes CRD   
	 *    1.3 registerCrdClients: generate a CRD client for each registered Kubernetes CRD 
	 * 
	 * Here, CRD is a concept of Kubernetes, please see
	 * https://kubernetes.io/docs/tasks/access-kubernetes-api
	 *  		/custom-resources/custom-resource-definitions/
	 *  
	 ****************************************************************/
	
	/**
	 * extend Kubernetes to support custom resources
	 */
	protected void initKube() {
		for (String configFile : configs) {
			try {
				Properties props = loadConfigFile(configFile);
				registerCrdToKube(props);
				registerCrdClients(props);
			} catch (Exception e) {
				m_logger.log(Level.SEVERE, e.getMessage());
			}
		}
	}

	/**
	 * @param configFile           file 
	 * @return                     properties
	 * @throws Exception           if the file not exist
	 */
	protected Properties loadConfigFile(String configFile) throws Exception {
		Properties props =  new Properties();
		props.load(getClass().getResourceAsStream(configFile));
		return props;
	}
	
	/**
	 * @param props            props
	 * @throws Exception       if the customResource is not found.
	 */
	protected void registerCrdToKube(Properties props) throws Exception {
		String kind = props.getProperty("KIND");
		registerCustomResource(kind, props);
		m_logger.log(Level.INFO, "register CustomResource [" + kind + "] successful.");
	}

	/**
	 * @param kind               kind
	 * @param props              properties
	 * @throws Exception         if the class in the properties cannot be loaded
	 */
	protected void registerCustomResource(String kind, Properties props) throws Exception {
		KubernetesDeserializer.registerCustomKind(
				props.getProperty("GROUP") + "/" + props.getProperty("VERSION"), 
				kind, Class.forName(ROOT_PKG + SUB_PKG + kind).asSubclass(KubernetesResource.class));
	}
	/**
	 * @param props             props
	 * @throws Exception        if the customResource is not found.
	 */
	protected void registerCrdClients(Properties props) throws Exception {
		String kind = props.getProperty("KIND");
		CustomResourceDefinition crd = getCustomResourceDefinition(
				props.getProperty("PLURAL") + "." + props.getProperty("GROUP"));
		if (crd == null) {
			throw new Exception("cannot find CustomResourceDefinition [" + kind + "]");
		}
		crdClients.put(kind, getCrdClient(kind, crd));
		m_logger.log(Level.INFO, "register crdClient [" + kind + "] successful.");
	}

	/**
	 * @param name               name
	 * @return                   customResourceDefinitions
	 */
	public CustomResourceDefinition getCustomResourceDefinition(String name) {
		return this.customResourceDefinitions().withName(name).get();
	}

	
	/**
	 * @param kind                 kind
	 * @param crd                  CustomeResourceDefinition
	 * @return                     CRDClient
	 * @throws Exception           if the customResource is not found.
	 */
	@SuppressWarnings({ "rawtypes", "unchecked"})
	protected MixedOperation getCrdClient(String kind, CustomResourceDefinition crd) throws Exception {
		return (MixedOperation) customResources(crd,
				Class.forName(ROOT_PKG + SUB_PKG + kind).asSubclass(CustomResource.class), 
				Class.forName(ROOT_PKG + SUB_PKG + kind + "List").asSubclass(CustomResourceList.class), 
				Class.forName(ROOT_PKG + SUB_PKG + "Doneable" + kind).asSubclass(CustomResourceDoneable.class))
					.inNamespace("default");
	}

	@SuppressWarnings("unchecked")
	public ParameterNamespaceListVisitFromServerGetDeleteRecreateWaitApplicable<HasMetadata, Boolean> load(String kind, String jsonStr) {
		try {
			return new JSONImpl(this, kind, jsonStr);
		} catch (Exception ex) {
			return load(new ByteArrayInputStream(jsonStr.getBytes()));
		}
	}
	
	/***************************************************************
	 * 
	 *                         Utils
	 *  following the fabric8 JDK style and providing CRD 
	 *  
	 *  Here, CRD is a concept of Kubernetes, please see
	 *  https://kubernetes.io/docs/tasks/access-kubernetes-api
	 *  		/custom-resources/custom-resource-definitions/
	 * 
	 ****************************************************************/
	
	static {
		configs.add("/VirtualMachine.conf");
		configs.add("/VirtualMachineImage.conf");
		configs.add("/VirtualMachineDisk.conf");
		configs.add("/VirtualMachineDiskSnapshot.conf");
		configs.add("/VirtualMachineSnapshot.conf");
		configs.add("/VirtualMachineNetwork.conf");
		configs.add("/VirtualMachinePool.conf");
		configs.add("/VirtualMachineDiskImage.conf");
		configs.add("/VirtualMachineBackup.conf");
	}
	
	/**
	 * @return        VirtualMachines
	 */
	public VirtualMachineImpl virtualMachines() {
		return new VirtualMachineImpl();
	}
	
	/**
	 * @return        VirtualMachines 
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachines(Watcher<VirtualMachine> watcher) {
		crdClients.get(VirtualMachine.class.getSimpleName()).watch(watcher);
	}
	
	
	/**
	 * @return        VirtualMachineImages
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineImages(Watcher<VirtualMachineImage> watcher) {
		crdClients.get(VirtualMachineImage.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return        VirtualMachineImages
	 */
	public VirtualMachineImageImpl virtualMachineImages() {
		return new VirtualMachineImageImpl();
	}
	
	/**
	 * @return        VirtualMachineDisks
	 */
	public VirtualMachineDiskImpl virtualMachineDisks() {
		return new VirtualMachineDiskImpl();
	}

	/**
	 * @return        virtualMachineBackups
	 */
	public VirtualMachineBackupImpl virtualMachineBackups() {
		return new VirtualMachineBackupImpl();
	}
	
	/**
	 * @return        VirtualMachineDisks
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineDisks(Watcher<VirtualMachineDisk> watcher) {
		crdClients.get(VirtualMachineDisk.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return        VirtualMachineDiskSnapshots
	 */
	public VirtualMachineDiskSnapshotImpl virtualMachineDiskSnapshots() {
		return new VirtualMachineDiskSnapshotImpl();
	}
	
	/**
	 * @return        VirtualMachineDiskSnapshots
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineDiskSnapshots(Watcher<VirtualMachineDiskSnapshot> watcher) {
		crdClients.get(VirtualMachineDiskSnapshot.class.getSimpleName()).watch(watcher);
	}	
	
	/**
	 * @return        VirtualMachinePools
	 */
	public VirtualMachinePoolImpl virtualMachinePools() {
		return new VirtualMachinePoolImpl();
	}
	
	/**
	 * @return        VirtualMachinePools
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachinePools(Watcher<VirtualMachinePool> watcher) {
		crdClients.get(VirtualMachinePool.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return        VirtualMachineNetworks
	 */
	public VirtualMachineNetworkImpl virtualMachineNetworks() {
		return new VirtualMachineNetworkImpl();
	}
	
	/**
	 * @return        VirtualMachineNetworks
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineNetworks(Watcher<VirtualMachineNetwork> watcher) {
		crdClients.get(VirtualMachineNetwork.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return        VirtualMachineSnapshots
	 */
	public VirtualMachineSnapshotImpl virtualMachineSnapshots() {
		return new VirtualMachineSnapshotImpl();
	}
	
	/**
	 * @return        VirtualMachineSnapshots
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineSnapshots(Watcher<VirtualMachineSnapshot> watcher) {
		crdClients.get(VirtualMachineSnapshot.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return        VirtualMachineDiskImages
	 */
	public VirtualMachineDiskImageImpl virtualMachineDiskImages() {
		return new VirtualMachineDiskImageImpl();
	}
	
	/**
	 * @return        VirtualMachineDiskImages
	 */
	@SuppressWarnings("unchecked")
	public void watchVirtualMachineDiskImages(Watcher<VirtualMachineDiskImage> watcher) {
		crdClients.get(VirtualMachineDiskImage.class.getSimpleName()).watch(watcher);
	}
	
	/**
	 * @return NodeSelector
	 */
	public NodeSelectorImpl getNodeSelector() {
		return new NodeSelectorImpl(this);
	}
	
	/**
	 * the same as  'virtualMachines'
	 * 
	 * @return                    virtualMachines
	 */
	public VirtualMachineImpl getVirtualMachineImpl() {
		return virtualMachines();
	}
	
	/**
	 * the same as  'virtualMachineDisks'
	 * 
	 * @return                    virtualMachineDisks
	 */
	public VirtualMachineDiskImpl getVirtualMachineDiskImpl() {
		return virtualMachineDisks();
	}
	
	/**
	 * the same as  'virtualMachineDiskSnapshots'
	 * 
	 * @return                    virtualMachineDiskSnapshots
	 */
	public VirtualMachineDiskSnapshotImpl getVirtualMachineDiskSnapshotImpl() {
		return virtualMachineDiskSnapshots();
	}
	
	/**
	 * the same as  'virtualMachineImages'
	 * 
	 * @return                    virtualMachineImages
	 */
	public VirtualMachineImageImpl getVirtualMachineImageImpl() {
		return virtualMachineImages();
	}
	
	/**
	 * the same as  'virtualMachineSnapshots'
	 * 
	 * @return                    virtualMachineSnapshots
	 */
	public VirtualMachineSnapshotImpl getVirtualMachineSnapshotImpl() {
		return virtualMachineSnapshots();
	}
	
	/**
	 * the same as  'virtualMachinePools'
	 * 
	 * @return                    virtualMachinePools
	 */
	public VirtualMachinePoolImpl getVirtualMachinePoolImpl() {
		return virtualMachinePools();
	}
	
	/**
	 * the same as  'virtualMachineDiskImages'
	 * 
	 * @return                    virtualMachineDiskImages
	 */
	public VirtualMachineDiskImageImpl getVirtualMachineDiskImageImpl() {
		return virtualMachineDiskImages();
	}
	
	/**
	 * the same as  'virtualMachineNetworks'
	 * 
	 * @return                    virtualMachineNetworks
	 */
	public VirtualMachineNetworkImpl getVirtualMachineNetworkImpl() {
		return virtualMachineNetworks();
	}

}
