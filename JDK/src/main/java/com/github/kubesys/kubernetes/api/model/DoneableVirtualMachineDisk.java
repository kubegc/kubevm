/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import io.fabric8.kubernetes.api.builder.Function;
import io.fabric8.kubernetes.client.CustomResourceDoneable;


/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @author xianghao16@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @since Thu July 08 21:36:39 CST 2019
 **/
public class DoneableVirtualMachineDisk extends CustomResourceDoneable<VirtualMachineDisk> {

	@SuppressWarnings({ "rawtypes", "unchecked" })
	public DoneableVirtualMachineDisk(VirtualMachineDisk resource, Function function) {
		super(resource, function);
	}
}

