/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.ha;

import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.impl.NodeSelectorImpl;

import io.fabric8.kubernetes.api.model.Node;
import io.fabric8.kubernetes.api.model.Status;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.utils.URLUtils;
import okhttp3.MediaType;
import okhttp3.Request;
import okhttp3.RequestBody;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed May 01 17:26:22 CST 2019
 * 
 *        https://www.json2yaml.com/ http://www.bejson.com/xml2json/
 * 
 *        debug at runWatch method of
 *        io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class NodeStatusWatcher implements Watcher<Node> {

	protected final static Logger m_logger = Logger.getLogger(NodeStatusWatcher.class.getName());

	protected final ExtendedKubernetesClient client;

	public NodeStatusWatcher(ExtendedKubernetesClient client) {
		this.client = client;
	}

	protected boolean isShutDown(Map<String, Object> status) {
		return status.get("reason").equals("ShutDown");
	}

	public void onClose(KubernetesClientException cause) {
		m_logger.log(Level.INFO, "Stop NodeStatusWatcher");
	}

	@SuppressWarnings("unchecked")
	@Override
	public void eventReceived(Action action, Node node) {
		
		if (action == Action.MODIFIED) {
			return;
		}
		
		String nodeName = node.getMetadata().getName();
		if (nodeName.startsWith("vm.") && NodeSelectorImpl.notReady(node)) {
			Map<String, String> labels = new HashMap<String, String>();
			labels.put("host", nodeName);
			for (VirtualMachine vm : client.virtualMachines().list(labels).getItems()) {
				try {
					Status status = vm.getSpec().getStatus();
					Map<String, Object> statusProps = status.getAdditionalProperties();
					Map<String, Object> statusCond = (Map<String, Object>) (statusProps.get("conditions"));
					Map<String, Object> statusStat = (Map<String, Object>) (statusCond.get("state"));
					Map<String, Object> statusWait = (Map<String, Object>) (statusStat.get("waiting"));
					statusWait.put("reason", "Shutdown");

					final String statusUri = URLUtils.join(client.getMasterUrl().toString(), "apis", "cloudplus.io",
							"v1alpha3", "namespaces", vm.getMetadata().getNamespace(), "virtualmachines",
							vm.getMetadata().getName());
					final RequestBody requestBody = RequestBody.create(MediaType.parse("application/json"),
							JSON.toJSONString(vm));
					client.getHttpClient()
							.newCall(new Request.Builder().method("PUT", requestBody).url(statusUri).build()).execute()
							.close();
				} catch (Exception e) {
					m_logger.severe("Error to modify the VM's status" + e);
				}
			}
		}
	}

}
