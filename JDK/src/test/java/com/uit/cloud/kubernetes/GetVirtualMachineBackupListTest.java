/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.api.model.VirtualMachineBackup;
import com.github.kubesys.kubernetes.api.model.VirtualMachineBackupList;
import com.github.kubesys.kubernetes.api.model.virtualmachinebackup.Backup;

import java.util.ArrayList;
import java.util.List;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class GetVirtualMachineBackupListTest {
	
	public static void main(String[] args) throws Exception {

//		getBackup("cloudinitbackup5555");
		getBackup("cloudinitbackup5555", "e8c9b41664584253afa43592d5efeafb");
	}
	public static List<Backup> getBackup(String domain) throws Exception {
		List<VirtualMachineBackup> list = AbstractTest.getVMBList(domain);
		List<Backup> res = new ArrayList<>();
		for (VirtualMachineBackup vmb : list) {
			Backup backup = vmb.getSpec().getBackup();
			System.out.println(JSON.toJSONString(backup, true));
			res.add(backup);
		}
		return res;
	}

	public static List<Backup> getBackup(String domain, String disk) throws Exception {
		List<VirtualMachineBackup> list = AbstractTest.getVMBList(domain);
		List<Backup> res = new ArrayList<>();
		for (VirtualMachineBackup vmb : list) {
			Backup backup = vmb.getSpec().getBackup();
			if (backup.getDisk() != null && backup.getDisk().equals(disk)) {
				System.out.println(JSON.toJSONString(backup, true));
				res.add(backup);
			}
		}
		return res;
	}
}
