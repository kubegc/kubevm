/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Pool;

import io.fabric8.kubernetes.api.model.KubernetesResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/4
 **/
@JsonDeserialize(using = JsonDeserializer.None.class)
public class VirtualMachinePoolSpec extends ExtendedCustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = -5134652268821098029L;
	

	protected Pool pool;

	protected Lifecycle lifecycle;
	
	public VirtualMachinePoolSpec() {

	}

	public Pool getPool() {
		return pool;
	}

	public void setPool(Pool pool) {
		this.pool = pool;
	}

	public Lifecycle getLifecycle() {
		return lifecycle;
	}

	public void setLifecycle(Lifecycle lifecycle) {
		this.lifecycle = lifecycle;
	}

}
