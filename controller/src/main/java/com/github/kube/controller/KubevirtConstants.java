/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.util.logging.Level;
import java.util.logging.Logger;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.api.model.ObjectMeta;
import io.fabric8.kubernetes.api.model.Pod;
import io.fabric8.kubernetes.client.Watcher.Action;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * 
 * KubevirtExecutor is used to manage Pod's lifecycle.
 * 
 **/
public final class KubevirtConstants {
	
	/**
	 * CPU demand
	 */
	public final static String CPU_RESOURCE         = "cpu";

	/**
	 * RAM demand
	 */
	public final static String RAM_RESOURCE          = "memory";
	
	/**
	 * pod namespace
	 */
	public final static String POD_NAMESPACE         = "default";
	
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
}
