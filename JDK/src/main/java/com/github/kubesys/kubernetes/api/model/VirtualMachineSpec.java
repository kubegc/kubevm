/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Domain;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle;

import io.fabric8.kubernetes.api.model.KubernetesResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/4
 *
 * <p>
 * <code>ExtendedKubernetesClient<code> extends <code>DefaultKubernetesClient<code>
 * to provide the lifecycle of VirtualMachine, VirtualMachinePool, VirtualMachineDisk,
 * VirtualMachineImage, VirtualMachineSnapshot, VirtualMachineNetwork
 * 
 */
@JsonDeserialize(using = JsonDeserializer.None.class)
public class VirtualMachineSpec extends ExtendedCustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = -5134652268821098029L;
	

	protected Domain domain;

	protected Lifecycle lifecycle;
	
	protected String powerstate;
	
	public VirtualMachineSpec() {

	}

	public Domain getDomain() {
		return domain;
	}

	public void setDomain(Domain domain) {
		this.domain = domain;
	}

	public Lifecycle getLifecycle() {
		return lifecycle;
	}

	public void setLifecycle(Lifecycle lifecycle) {
		this.lifecycle = lifecycle;
	}

	public String getPowerstate() {
		return powerstate;
	}

	public void setPowerstate(String powerstate) {
		this.powerstate = powerstate;
	}
	
}
