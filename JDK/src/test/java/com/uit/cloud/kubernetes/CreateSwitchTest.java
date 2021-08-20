/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinenetwork.Lifecycle.CreateBridge;
import com.github.kubesys.kubernetes.api.model.virtualmachinenetwork.Lifecycle.CreateSwitch;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateSwitchTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineNetworks()
				.createSwitch("switch22", "vm.node22", get());
		System.out.println(successful);
	}

	protected static CreateSwitch get() {
		CreateSwitch vxlan = new CreateSwitch();
		vxlan.setSubnet("192.168.2.0/24");
		vxlan.setMtu("1450");
		vxlan.setGateway("192.168.2.1");
		vxlan.setBridge("br-ex");
		vxlan.setVlanId("20");
		vxlan.setDhcp("192.168.2.1");
		vxlan.setIpv6("false");
		return vxlan;
	}
	
	protected static CreateSwitch getIpv6() {
		CreateSwitch vxlan = new CreateSwitch();
		vxlan.setSubnet("2001:198:10::/64");
		vxlan.setMtu("1450");
		vxlan.setGateway("2001:1::1");
		vxlan.setBridge("br-ex");
		vxlan.setVlanId("20");
		vxlan.setDhcp("2001:1::1");
		vxlan.setIpv6("true");
		return vxlan;
	}
}
