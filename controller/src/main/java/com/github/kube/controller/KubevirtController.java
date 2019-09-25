/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller;

import java.io.File;
import java.io.FileInputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.yaml.snakeyaml.Yaml;

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
	 * 
	 */
	public KubevirtController() {
		this(DEFAULT_TOKEN);
	}
	
	/**
	 * @param token               token
	 */
	public KubevirtController(String token) {
		try {
			Map<String, Object> config = new Yaml().load(
								new FileInputStream(new File(token)));
			Map<String, Map<String, Object>> clusdata = get(config, "clusters");
			Map<String, Map<String, Object>> userdata = get(config, "users");
			this.client = initKubeClient(clusdata, userdata);
		} catch (Exception ex) {
			m_logger.log(Level.SEVERE, "unable to initial Kubernetes client:" + ex);
		}
	}
	
	/**
	 * @param client             client
	 */
	public KubevirtController(ExtendedKubernetesClient client) {
		this.client = client;
	}

	/**
	 * @param map                 map
	 * @param key                 key
	 * @return                    data
	 */
	@SuppressWarnings({ "unchecked", "rawtypes" })
	protected Map<String, Map<String, Object>> get(Map<String, Object> map, String key) {
		return (Map<String, Map<String, Object>>)
					((List) map.get(key)).get(0);
	}

	/**
	 * @param clusdata              cluster data
	 * @param userdata              user data
	 * @return                      client
	 */
	protected ExtendedKubernetesClient initKubeClient(Map<String, Map<String, Object>> clusdata,
									Map<String, Map<String, Object>> userdata) {
		
		Config config = new ConfigBuilder()
				.withApiVersion("v1")
				.withCaCertData((String) clusdata.get("cluster").get("certificate-authority-data"))
				.withClientCertData((String) userdata.get("user").get("client-certificate-data"))
				.withClientKeyData((String) userdata.get("user").get("client-key-data"))
				.withMasterUrl((String) clusdata.get("cluster").get("server"))
				.build();
		return new ExtendedKubernetesClient(config);
	}
	
	/**
	 * start controller manager based on watcher mechanism, each watcher 
	 * is used for one kind of CRD
	 */
	public void start() throws Exception {
		List<Method> watchers = new ArrayList<Method>();
		findAllWatchers(watchers, client.getClass());
		for (Method watcherMethod : watchers) {
			watcherMethod.invoke(client, getWatcherParam(watcherMethod));
		}
	}

	/**
	 * @param watcherMethod             method
	 * @return                          object
	 * @throws Exception                exception
	 */
	protected Object getWatcherParam(Method watcherMethod) throws Exception {
		for (Constructor<?> constructor : watcherMethod.getParameterTypes()[0]
												.getDeclaredConstructors()) {
			if (constructor.getParameterCount() == 1 && 
					subClassOfKubevirtWatcher(constructor.getParameterTypes()[0])) {
				return constructor.newInstance(client);
			}
		}
		return null;
	}

	/**
	 * @param wms
	 */
	protected void findAllWatchers(List<Method> wms, Class<?> clazz) {
		while (!clazz.getName().equals(Object.class.getName())) {
			
			for (Method method : clazz.getDeclaredMethods()) {
				
				if (method.getName().startsWith("watch") 
						&& method.getParameterCount() == 1
						&& subClassOfKubevirtWatcher(
								method.getParameterTypes()[0])) {
						
					wms.add(method);
				}
			}
			findAllWatchers(wms, clazz.getSuperclass());
		}
	}

	/**
	 * @param clazz                     clazz
	 * @return                          true or false
	 */
	protected boolean subClassOfKubevirtWatcher(Class<?> clazz) {
		try {
			clazz.asSubclass(KubevirtWatcher.class);
			return true;
		} catch (Exception ex) {
			return false;
		}
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
