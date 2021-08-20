/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.api.model.VirtualMachineBackup;
import com.github.kubesys.kubernetes.api.model.VirtualMachineBackupList;

import java.util.*;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class GetVirtualMachineBackupTest {
	
	public static void main(String[] args) throws Exception {
		System.out.println(AbstractTest.getVMBByName("vmbackup2"));
	}
	
}
