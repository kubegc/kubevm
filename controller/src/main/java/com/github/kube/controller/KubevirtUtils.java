/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.util.logging.Logger;

import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Domain.Devices.Disk;


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
public class KubevirtUtils {
	
	/**
	 * m_logger
	 */
	protected final static Logger m_logger  = Logger.getLogger(KubevirtUtils.class.getName());
	
	public final static String LOCAL_VM_PREFIX = "/mnt/localfs";
	
	public static boolean enableHA(VirtualMachine vm) {
		String ha = vm.getMetadata().getLabels().get("ha");
		// VM without HA setting
		if (ha == null || ha.length() == 0 
					|| !ha.equals("true")) {
			return false;
		}
		return true;
	}
	
	public static boolean localVM(VirtualMachine vm) {
		try {
			for (Disk disk : vm.getSpec().getDomain().getDevices().getDisk()) {
				if (disk.getSource().get_file().startsWith(LOCAL_VM_PREFIX)) {
					return true;
				}
			}
		} catch (Exception ex) {
			
		}
		return false;
	}
	
	public static String getStatus(VirtualMachine vm) {
		return vm.getSpec().getPowerstate();
	}
	
	public static boolean isShutDown(String status) {
		return (status == null) || status.equals("Shutdown");
	}
	
}
