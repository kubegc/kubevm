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
 * @since Thu Jun 13 21:39:55 CST 2019
 **/
public class VirtualMachineBackup extends CustomResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = 8153024376244249249L;
	
	private VirtualMachineBackupSpec spec;

	public VirtualMachineBackupSpec getSpec() {
		return spec;
	}

	public void setSpec(VirtualMachineBackupSpec spec) {
		this.spec = spec;
	}
}

