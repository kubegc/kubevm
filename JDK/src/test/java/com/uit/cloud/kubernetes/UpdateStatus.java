/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;

import io.fabric8.kubernetes.api.model.Status;
import io.fabric8.kubernetes.client.utils.URLUtils;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class UpdateStatus {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		System.out.println(JSON.toJSONString(client.virtualMachines().get("vm006"), true));
//		VirtualMachine vm = client.virtualMachines().get("wyw1234");
//		Status status = vm.getSpec().getStatus();
//		Map<String, Object> statusProps = status.getAdditionalProperties();	
//		Map<String, Object> statusCond = (Map<String, Object>) (statusProps.get("conditions"));
//		Map<String, Object> statusStat = (Map<String, Object>) (statusCond.get("state"));
//		Map<String, Object> statusWait = (Map<String, Object>) (statusStat.get("waiting"));
//		statusWait.put("reason", "Shutdown");
//		
//	 final String statusUri = URLUtils.join(client.getMasterUrl().toString(), "apis", "cloudplus.io", "v1alpha3", "namespaces",
//             "default", "virtualmachines", "wyw1234");
//     final RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"), JSON.toJSONString(vm));
//     client.getHttpClient().newCall(new Request.Builder()
//             .method("PUT", requestBody)
//             .url(statusUri)
//             .build())
//             .execute()
//             .close();
	}
		
}
