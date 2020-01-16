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

import com.github.kube.controller.ha.NodeStatusWatcher;
import com.github.kube.controller.ha.VirtualMachineStatusWatcher;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;

import io.fabric8.kubernetes.client.Config;
import io.fabric8.kubernetes.client.ConfigBuilder;
import io.fabric8.kubernetes.client.Watcher;
import io.fabric8.kubernetes.client.dsl.MixedOperation;

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
public final class KubevirtController {
	
	/**
	 * m_logger
	 */
	protected final static Logger m_logger  = Logger.getLogger(KubevirtController.class.getName());

	/**
	 * default token
	 */
	public final static String DEFAULT_TOKEN = "admin.conf";
	
	/**
	 * Kubernetes client, please see https://github.com/uit-plus/kubeext-jdk
	 */
	protected final ExtendedKubernetesClient client;
	
	/************************************************************************
	 * 
	 *                       Constructors
	 * 
	 ************************************************************************/
	
	/**
	 * initialize the client with the default token
	 * 
	 * @throws Exception         exception
	 */
	public KubevirtController() throws Exception {
		this(DEFAULT_TOKEN);
	}
	
	/**
	 * initialize the client with the specified token
	 * 
	 * @param  token              token
	 * @throws Exception          exception
	 */
	public KubevirtController(String token) throws Exception {
		Map<String, Object> config = new Yaml().load(
							new FileInputStream(new File(token)));
		Map<String, Map<String, Object>> clusdata = get(config, "clusters");
		Map<String, Map<String, Object>> userdata = get(config, "users");
		this.client = initKubeClient(clusdata, userdata);
	}
	
	/**
	 * initialize the client with the specified client
	 * 
	 * @param client             client
	 */
	public KubevirtController(ExtendedKubernetesClient client) {
		this.client = client;
	}

	/**
	 * @param data                data set
	 * @param key                 key
	 * @return                    the related data
	 */
	@SuppressWarnings({ "unchecked", "rawtypes" })
	protected Map<String, Map<String, Object>> get(Map<String, Object> data, String key) {
		return (Map<String, Map<String, Object>>)
					((List) data.get(key)).get(0);
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
	
	/************************************************************************
	 * 
	 *                       Core
	 * 
	 ************************************************************************/
	/**
	 * start all watchers based on Java reflect mechanism
	 * 
	 * @throws Exception               exception 
	 */
	@SuppressWarnings({ "rawtypes", "unchecked" })
	public void startAllWatchers() throws Exception {
		
		for (Method watcher : findAllWatchersBy(client.getClass())) {
			startWatcher(watcher);
		}
		MixedOperation vmWatcher = ExtendedKubernetesClient.crdClients.get(
										VirtualMachine.class.getSimpleName());
		vmWatcher.watch(new VirtualMachineStatusWatcher(client));
		client.nodes().watch(new NodeStatusWatcher(client));
	}

	/**
	 * start a watcher based on Java reflect mechanism
	 * 
	 * @param watcher                   watcher
	 */
	protected void startWatcher(Method watcher) {
		try {
			watcher.invoke(client, getWatcherParam(watcher));
			m_logger.log(Level.INFO, "start controller " + getWatcherName(watcher) + " successful");
		} catch (Exception ex) {
			m_logger.log(Level.SEVERE, "Fail to start controller:" + ex);
		}
	}

	/**
	 * @param watcher                   watcher
	 * @return                          watcher object
	 * @throws Exception                exception
	 */
	protected Object getWatcherParam(Method watcher) throws Exception {
		
		Class<?> watcherType = Class.forName(getClassName(watcher));
		
		for (Constructor<?> constructor : watcherType.getDeclaredConstructors()) {
			
			if (constructor.getParameterCount() == 1 && 
					subclassOfClient(constructor.getParameterTypes()[0])) {
				
				return constructor.newInstance(client);
			}
		}
		return null;
	}

	/**
	 * @param watcher                 watcher
	 * @return                        classname
	 */
	protected String getClassName(Method watcher) {
		return KubevirtWatcher.class.getPackage().getName() 
				+ ".watchers." + getWatcherName(watcher);
	}
	
	/**
	 * @param watcher                 watcher
	 * @return                        watcher name
	 */
	protected String getWatcherName(Method watcher) {
		return watcher.getName().substring("watch".length(), 
				watcher.getName().length() -1) + "Watcher";
	}

	/**
	 * @param typeName                  typename  
	 * @return                          true or false
	 */
	private boolean subclassOfClient(Class<?> typeName) {
		try {
			typeName.asSubclass(ExtendedKubernetesClient.class);
			return true;
		} catch (Exception ex) {
			m_logger.log(Level.WARNING, "ignore this constructor:" + ex);
			return false;
		}
	}

	/**
	 * @param clazz                     clazz
	 * @return                          all watchers
	 */
	protected List<Method> findAllWatchersBy(Class<?> clazz) {
		
		List<Method> watchers = new ArrayList<Method>();
		if (!clazz.getName().equals(Object.class.getName())) {
			for (Method method : clazz.getDeclaredMethods()) {
				if (isWatcherMethod(method) && isWatcherParam(method)) {
					watchers.add(method);
				}
			}
			watchers.addAll(findAllWatchersBy(clazz.getSuperclass()));
		}
		return watchers;
	}

	/**
	 * @param method              method
	 * @return                    true or flase
	 */
	protected boolean isWatcherParam(Method method) {
		return method.getParameterCount() == 1 && 
				method.getParameterTypes()[0].getName()
						.equals(Watcher.class.getName());
	}

	/**
	 * @param method               method
	 * @return                     true or false
	 */
	protected boolean isWatcherMethod(Method method) {
		return method.getName().startsWith("watch");
	}
	

	/************************************************************************
	 * 
	 *                       Main
	 * 
	 ************************************************************************/
	/**
	 * @param  args               args
	 * @throws Exception          cannot start controller manager
	 */
	public static void main(String[] args) throws Exception {
		KubevirtController controller = new KubevirtController();
		controller.startAllWatchers();
	}
}
