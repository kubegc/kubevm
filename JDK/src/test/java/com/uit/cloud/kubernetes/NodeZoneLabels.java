/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Map;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.api.model.Node;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class NodeZoneLabels {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		Node[] nodes = client.nodes().list().getItems().toArray(new Node[] {});
		
		sortByMinimumCPUUsage(nodes);
//		Map<String, String> labels = node.getMetadata().getLabels();
//		// 可以添加多个标签
//		labels = (labels == null) ? new HashMap<String, String>() : labels;
//		labels.put("zone", "rackA");
//		client.nodes().create(node);
//		System.out.println(stringToLong(node.getStatus().getAllocatable().get("cpu").getAmount()));
//		System.out.println(stringToLong(node.getStatus().getAllocatable().get("memory").getAmount()));
//		System.out.println(stringToLong(node.getStatus().getAllocatable().get("pods").getAmount()));
	}
	
	protected static long stringToLong(String value) {
		long weight = 1;
		if (value.endsWith("Ki")) {
			value = value.substring(0, value.length() - 2);
			weight = 1;
		} else if (value.endsWith("Mi")) {
			value = value.substring(0, value.length() - 2);
			weight = 1024;
		} else if (value.endsWith("Gi")) {
			value = value.substring(0, value.length() - 2);
			weight = 1024*1024;
		} else if (value.endsWith("Ti")) {
			value = value.substring(0, value.length() - 2);
			weight = 1024*1024*1024;
		} 
		
		return Long.parseLong(value) * weight;
	}

	protected static void sortByMinimumCPUUsage(Node[] nodes) {
		Arrays.sort(nodes, new Comparator<Node>() {

			@Override
			public int compare(Node o1, Node o2) {
				long lo1 = stringToLong(o1.getStatus()
						.getAllocatable().get("cpu").getAmount());
				long lo2 = stringToLong(o2.getStatus()
						.getAllocatable().get("cpu").getAmount());
				return (lo2 - lo1 < 0) ? -1 : 1;
			}
			
		});
	}
}
