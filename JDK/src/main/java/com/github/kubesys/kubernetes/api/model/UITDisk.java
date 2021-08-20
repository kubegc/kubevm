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
 * @since Thu July 8 21:39:55 CST 2019
 **/
@Deprecated
public class UITDisk extends CustomResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = -5561963208233608008L;
	
	private UITDiskSpec spec;

	public UITDiskSpec getSpec() {
		return spec;
	}

	public void setSpec(UITDiskSpec spec) {
		this.spec = spec;
	}

}

