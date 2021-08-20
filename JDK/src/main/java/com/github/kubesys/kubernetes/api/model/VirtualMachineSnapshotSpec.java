/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Domainsnapshot;
import com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Lifecycle;

import io.fabric8.kubernetes.api.model.KubernetesResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/4
 * 
 **/
@JsonDeserialize(using = JsonDeserializer.None.class)
public class VirtualMachineSnapshotSpec extends ExtendedCustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1171174592223281364L;

	protected Domainsnapshot domainsnapshot;
	
	protected Lifecycle lifecycle;
	
	public VirtualMachineSnapshotSpec() {

	}

	public Domainsnapshot getDomainsnapshot() {
		return domainsnapshot;
	}

	public void setDomainsnapshot(Domainsnapshot domainsnapshot) {
		this.domainsnapshot = domainsnapshot;
	}

	public Lifecycle getLifecycle() {
		return lifecycle;
	}

	public void setLifecycle(Lifecycle lifecycle) {
		this.lifecycle = lifecycle;
	}

}
