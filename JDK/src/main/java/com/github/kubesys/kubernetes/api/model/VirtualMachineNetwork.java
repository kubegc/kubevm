/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import io.fabric8.kubernetes.client.CustomResource;


/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @author xianghao16@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @since Thu Aug 19 21:39:55 CST 2019
 **/
public class VirtualMachineNetwork extends CustomResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = 4669199871773009651L;
	
	private VirtualMachineNetworkSpec spec;

	public VirtualMachineNetworkSpec getSpec() {
		return spec;
	}

	public void setSpec(VirtualMachineNetworkSpec spec) {
		this.spec = spec;
	}

}

