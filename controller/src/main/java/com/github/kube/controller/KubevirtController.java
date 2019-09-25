/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.io.File;
import java.io.FileInputStream;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.yaml.snakeyaml.Yaml;

import com.github.kube.controller.watchers.VirtualMachineDiskWatcher;
import com.github.kube.controller.watchers.VirtualMachineImageWatcher;
import com.github.kube.controller.watchers.VirtualMachineNetworkWatcher;
import com.github.kube.controller.watchers.VirtualMachinePoolWatcher;
import com.github.kube.controller.watchers.VirtualMachineSnapshotWatcher;
import com.github.kube.controller.watchers.VirtualMachineWatcher;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.ConfigBuilder;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since Wed Sep 25 17:26:22 CST 2019
 * 
 * KubevirtController is used for starting various wacthers.
 * 
 * Note that this progress is running on the master node of Kubernetes
 * with pre-installed CRDs.
 **/
public class KubevirtController {
	
	/**
	 * m_logger
	 */
	protected final static Logger m_logger  = Logger.getLogger(KubevirtController.class.getName());

	/**
	 * default token
	 */
	public final static String DEFAULT_TOKEN = "/etc/kubernetes/admin.conf";
	
	/**
	 * Kubernetes client, please see https://github.com/uit-plus/kubeext-jdk
	 */
	protected ExtendedKubernetesClient client;
	
	
	/**
	 * @throws Exception         token file does not exist
	 */
	public KubevirtController() throws Exception {
		this(DEFAULT_TOKEN);
	}
	
	/**
	 * @param token               token
	 * @throws Exception          token file does not exist or wrong token
	 */
	public KubevirtController(String token) throws Exception {
		Map<String, Object> config = new Yaml().load(
							new FileInputStream(new File(token)));
		Map<String, Map<String, Object>> clusdata = get(config, "clusters");
		Map<String, Map<String, Object>> userdata = get(config, "users");
		initKubeClient(clusdata, userdata);
	}

	@SuppressWarnings({ "unchecked", "rawtypes" })
	protected Map<String, Map<String, Object>> get(Map<String, Object> map, String key) {
		return (Map<String, Map<String, Object>>)
					((List) map.get(key)).get(0);
	}

	/**
	 * @param clusdata              cluster data
	 * @param userdata              user data
	 */
	protected void initKubeClient(Map<String, Map<String, Object>> clusdata,
									Map<String, Map<String, Object>> userdata) {
		
		Config config = new ConfigBuilder()
				.withApiVersion("v1")
				.withCaCertData((String) clusdata.get("cluster").get("certificate-authority-data"))
				.withClientCertData((String) userdata.get("user").get("client-certificate-data"))
				.withClientKeyData((String) userdata.get("user").get("client-key-data"))
				.withMasterUrl((String) clusdata.get("cluster").get("server"))
				.build();
		this.client = new ExtendedKubernetesClient(config);
	}
	
	/**
	 * start controller manager based on watcher mechanism, each watcher 
	 * is used for one kind of CRD
	 */
	public void start() {
		client.watchVirtualMachines(new VirtualMachineWatcher(client));
		client.watchVirtualMachinePools(new VirtualMachinePoolWatcher(client));
		client.watchVirtualMachineDisks(new VirtualMachineDiskWatcher(client));
		client.watchVirtualMachineImages(new VirtualMachineImageWatcher(client));
		client.watchVirtualMachineNetworks(new VirtualMachineNetworkWatcher(client));
		client.watchVirtualMachineSnapshots(new VirtualMachineSnapshotWatcher(client));
	}
	
	/**
	 * @param args                args
	 * @throws Exception          cannot start controller manager
	 */
	public static void main(String[] args) throws Exception {
		KubevirtController controller = new KubevirtController();
		try {
			controller.start();
		} catch (Exception ex) {
			m_logger.log(Level.SEVERE, "Fail to start controller:" + ex);
		}
	}
}
