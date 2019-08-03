/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import com.github.kube.ha.KubevirtVMHA;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed May 01 17:26:22 CST 2019
 * 
 * https://www.json2yaml.com/
 * http://www.bejson.com/xml2json/
 * 
 * debug at runWatch method of io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class KubevirtControllerTest {
	
	public static void main(String[] args) throws Exception {
		KubevirtVMHA scheduler = new KubevirtVMHA("admin.conf");
		scheduler.start();
	}

}
