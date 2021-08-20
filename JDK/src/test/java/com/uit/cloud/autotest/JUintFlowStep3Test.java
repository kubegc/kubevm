/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.autotest;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.validation.constraints.Pattern;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.henry.AbstractTest;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineDisk;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSnapshot;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ChangeNumberOfCPU;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CloneVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromImage;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeleteVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.PlugDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResizeRAM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StartVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StopVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StopVMForce;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnplugNIC;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CloneDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateDiskInternalSnapshot;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.DeleteDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.DeleteDiskInternalSnapshot;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.ResizeDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Lifecycle.CreateSnapshot;
import com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Lifecycle.DeleteSnapshot;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

import io.fabric8.kubernetes.api.model.Status;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/4
 * 
 **/
public class JUintFlowStep3Test {
	
	
	public final static JUintFlowStep3Test jfs3 = new JUintFlowStep3Test();
	
	public final static RegExpUtils reu = new RegExpUtils();
	
	/**********************************************************************
	 * 
	 *         Please ensure the following values are correct 
	 * 
	 **********************************************************************/
	
	// RegisterISO
	public final static String ISO = "/var/lib/libvirt/iso/centos7-minimal-1511.iso";
	
	// CreateVMImage
	public final static String IMAGE = "/var/lib/libvirt/templates/950646e8c17a49d0b83c1c797811e002";
	
	// CreateVPC
	public final static String SWITCH = "switchtest";
	
	// CreateVMDisk
	public final static String ROOTDISK = "/var/lib/libvirt/images/rootdisk";
	
	// NodeName
	public final static String NODENAME = "vm.node30";
	
	/**********************************************************************
	 * 
	 *                    Global variables
	 * 
	 **********************************************************************/
	
	public static int total   = 0;
	
	public static int sucess  = 0;
	
	public static int failure = 0;
	
	public static int testId = 0;
	
	
	/**********************************************************************
	 * 
	 *                    Default Test value
	 * 
	 **********************************************************************/
	
	public final static String NAME_CorrectValue             = "vm.auto.test-004";
	
	public final static String NAME_UnsupportSymbol          = "auto_test";
	
	public final static String NAME_TooShort                 = "";
	
	public final static String NAME_TooLong                  = "auto.test-auto.test-auto.test-ahahhaa";

	public final static String UUID_CorrectValue             = "uuid=150646e8-c17a-49d0-b83c-1c797811e545";
	
	public final static String UUID_WrongFormat              = "auto.test";
	
	public final static String UUID_UnsupportSymbol          = "uuid=auto_test";
	
	public final static String UUID_TooShort                 = "uuid=";
	
	public final static String UUID_TooLong                  = "uuid=auto.test-auto.test-auto.test-asddddddddddddddddd";
	
	public final static String PATH_CorrectValue             = "/var/lib/libvirt/images/rootdisk";
	
	public final static String PATH_WrongFormat              = "/var/lib/libvirt2/";
	
	public final static String PATH_UnsupportSymbol          = "/var/lib/lib_virt/";
	
	public final static String OS_CorrectValue               =  "centos7.0";
	
	public final static String OS_WrongValue                 =  "cent777";
	
	public final static String MAC_CorrectValue              = "52:54:29:16:e0:cc";
	
	public final static String MAC_WrongFormat               = "52:54:EF:16:e0:cc";
	
	public final static String MAC_UnsupportSymbol           = "fe:54:29:16:e0:cc";
	
	public final static String MAC_TooShort                  = "52:54:EF:16:e0";
	
	public final static String MAC_TooLong                   = "52:54:EF:16:e0:cc:cc";
	
	public final static String VCPU_CorrectValue             = "2";
	
	public final static String VCPU_TooSmall                 = "0";
	
	public final static String VCPU_TooLarger                = "100";
	
	public final static String RAM_CorrectValue              = "4096";
	
	public final static String RAM_TooSmall                  = "99";
	
	public final static String RAM_TooLarger                 = "100000";
	
	public final static String DISK_TYPE_CorrectValue        = "qcow2";
	
	public final static String DISK_TYPE_WrongFormat         = "abc2";
	
	public final static String FDISK_TYPE_CorrectValue       = "vdc";
	
	public final static String FDISK_TYPE_WrongValue         =  "abd2";
	
	public final static String DISK_MODE_CorrectValue        = "shareable";
	
	public final static String DISK_MODE_WrongValue          = "read";
	
	public final static String DISK_DRIVER_CorrectValue      = "qemu";
	
	public final static String DISK_DRIVER_WrongValue        = "read";
	
	public final static String VIRT_TYPE_CorrectValue        = "kvm";
	
	public final static String SWITCH_TYPE_CorrectValue1     = "bridge";
	
	public final static String SWITCH_TYPE_CorrectValue2     = "l2bridge";
	
	public final static String SWITCH_TYPE_CorrectValue3     = "l3bridge";
	
	public final static String SWITCH_TYPE_WrongValue        = "l3b";
	
	public final static String GRAPHICS_CorrectValue         = "vnc,listen=0.0.0.0";
	
	public final static String DISK_SIZE_CorrectValue        = "20000000000";
	
	public final static String DISK_SIZE_TooSmall            = "1000000000";
	
	public final static String DISK_SIZE_TooLarger           = "19999999999999";
	
	public final static String IP_CorrectValue               = "192.168.5.12";
	
	public final static String IP_WrongRange1                = "256.168.5.12";
	
	public final static String IP_WrongRange2                = "192.168.5.256";
	
	public final static String IP_WrongFormat1               = "192.168";
	
	public final static String IP_WrongFormat2               = "192.168.5.12.1";
	
	public final static String VCPUSET_CorrectValue          = "1,cpuset=1";
	
	public final static String VCPUSET_WrongValue            = "192.168.5.12,cpuset=1000";
	
	public final static String IP_SWITCH_CorrectValue1       = "source=virbr0";
	
	public final static String IP_SWITCH_CorrectValue2       = "source=br-native";
	
	public final static String IP_SWITCH_CorrectValue3       = "source=br-int,ip=192.168.5.2,switch=switch";
	
	public final static String IP_SWITCH_WrongValue1         = "source=cni0";
	
	public final static String IP_SWITCH_WrongValue2         = "cni0";
	
	public final static String IP_SWITCH_WrongValue3         = "source=br-int,ip=192";
	
	public final static String NETWORK_TYPE_CorrectValue1    = "type=bridge,source=virbr0";

	public final static String NETWORK_TYPE_CorrectValue2    = "type=l2bridge,source=br-native";
	
	public final static String NETWORK_TYPE_CorrectValue3    = "type=l3bridge,source=br-int,ip=192.168.5.12,switch=" + SWITCH + ",inbound=102400,outbound=102400,mac=52:54:29:16:e0:cc";
	
	public final static String NETWORK_TYPE_WrongValue1      = "type=bri";

	public final static String NETWORK_TYPE_WrongValue2      = "l2bridge";
	
	public final static String NETWORK_TYPE_WrongValue3      = "type=l3bridge,source=bri";
	
	public final static String ISO_Cdrom_CorrectValue        = ISO;
	
	public final static String ISO_Cdrom_WrongValue          = ISO.toUpperCase();
	
	public final static String ISO_Disk_CorrectValue         = ROOTDISK;
	
	public final static String ISO_Disk_WrongValue           = ROOTDISK.toUpperCase();
	
	public final static String IMAGE_Cdrom_CorrectValue      = IMAGE;
	
	public final static String IMAGE_Cdrom_WrongValue        = IMAGE.toUpperCase();
	
	public final static String IMAGE_Disk_CorrectValue       = ROOTDISK;
	
	public final static String IMAGE_Disk_WrongValue         = ROOTDISK.toUpperCase();
	

	/**********************************************************************
	 * 
	 *                    Parameters and steps
	 * 
	 **********************************************************************/
	
	public final static List<Map<String, Map<String,String>>> paramValues = new ArrayList<Map<String, Map<String, String>>>();
	
	public final static List<List<String>> testRounds = new ArrayList<List<String>>();
	
	public final static Map<String, String> pregexpMap = new HashMap<String, String>();
	
	
	/**********************************************************************
	 * 
	 *                    init parameters and steps
	 * 
	 **********************************************************************/
	
	static {
		{
			List<String> testRound1 = new ArrayList<String>();
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + CreateAndStartVMFromISO.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + StopVMForce.class.getName());
//			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + UpdateOS.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + StartVM.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + ChangeNumberOfCPU.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + ResizeRAM.class.getName());
	
			testRound1.add(VirtualMachineSnapshot.class.getSimpleName() + "=" + CreateSnapshot.class.getName());
			testRound1.add(VirtualMachineSnapshot.class.getSimpleName() + "=" + DeleteSnapshot.class.getName());
			
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + CreateDisk.class.getName());
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + ResizeDisk.class.getName());
			
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + PlugDisk.class.getName());
			
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + CreateDiskInternalSnapshot.class.getName());
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + DeleteDiskInternalSnapshot.class.getName());
			
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + UnplugNIC.class.getName());
			
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + CloneDisk.class.getName());
			testRound1.add(VirtualMachineDisk.class.getSimpleName() + "=" + DeleteDisk.class.getName());
			
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + StopVM.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + CloneVM.class.getName());
			testRound1.add(VirtualMachine.class.getSimpleName() + "=" + DeleteVM.class.getName());
			testRounds.add(testRound1);
		}
		
		{
			List<String> testRound2 = new ArrayList<String>();
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + CreateAndStartVMFromImage.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + StopVM.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + StartVM.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + ChangeNumberOfCPU.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + ResizeRAM.class.getName());
	
			testRound2.add(VirtualMachineSnapshot.class.getSimpleName() + "=" + CreateSnapshot.class.getName());
			testRound2.add(VirtualMachineSnapshot.class.getSimpleName() + "=" + DeleteSnapshot.class.getName());
			
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + CreateDisk.class.getName());
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + ResizeDisk.class.getName());
			
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + PlugDisk.class.getName());
			
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + CreateDiskInternalSnapshot.class.getName());
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + DeleteDiskInternalSnapshot.class.getName());
			
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + UnplugNIC.class.getName());
			
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + CloneDisk.class.getName());
			testRound2.add(VirtualMachineDisk.class.getSimpleName() + "=" + DeleteDisk.class.getName());
			
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + StopVM.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + CloneVM.class.getName());
			testRound2.add(VirtualMachine.class.getSimpleName() + "=" + DeleteVM.class.getName());
//			testRounds.add(testRound2);
		}
	}
	
	
	protected static void initParamValues() throws IllegalAccessException {
		Map<String, Map<String, String>> map1 = new HashMap<String, Map<String, String>>();
		Map<String, Map<String, String>> map2 = new HashMap<String, Map<String, String>>();
		Map<String, Map<String, String>> map3 = new HashMap<String, Map<String, String>>();
		
		for (Field f: JUintFlowStep3Test.class.getDeclaredFields()) {
			String name  = f.getName();
			Object value = f.get(jfs3);
			if ((value instanceof String && name.indexOf("_") != -1)) {
				int pos = name.lastIndexOf("_");
				String key = name.substring(0, pos) + "_PATTERN";

				if (name.endsWith("CorrectValue1")) {
					Map<String, String> v1 = map1.get(key);
					v1 = (v1 == null) ? new HashMap<String, String>() : v1;
					v1.put(name, (String) value);
					map1.put(key, v1);
				} else if (name.endsWith("CorrectValue2")) {
					Map<String, String> v2 = map2.get(key);
					v2 = (v2 == null) ? new HashMap<String, String>() : v2;
					v2.put(name, (String) value);
					map2.put(key, v2);
				} else if (name.endsWith("CorrectValue3")) {
					Map<String, String> v3 = map3.get(key);
					v3 = (v3 == null) ? new HashMap<String, String>() : v3;
					v3.put(name, (String) value);
					map3.put(key, v3);
				} else {
					Map<String, String> v1 = map1.get(key);
					v1 = (v1 == null) ? new HashMap<String, String>() : v1;
					v1.put(name, (String) value);
					map1.put(key, v1);
					
					Map<String, String> v2 = map2.get(key);
					v2 = (v2 == null) ? new HashMap<String, String>() : v2;
					v2.put(name, (String) value);
					map2.put(key, v2);
					
					Map<String, String> v3 = map3.get(key);
					v3 = (v3 == null) ? new HashMap<String, String>() : v3;
					v3.put(name, (String) value);
					map3.put(key, v3);
				}
			}
			
			}
		paramValues.add(map1);
		paramValues.add(map2);
		paramValues.add(map3);
			
	}
	
	protected static void initRegExpMap() throws IllegalAccessException {
		
		for (Field field : reu.getClass().getDeclaredFields()) {
			if (field.getName().endsWith("PATTERN")) {
				pregexpMap.put((String)field.get(reu), field.getName());
			}
		}
		
	}
	
	/**********************************************************************
	 * 
	 *                    Kubernetes connect
	 * 
	 **********************************************************************/
	protected ExtendedKubernetesClient client;
	
	public JUintFlowStep3Test() {
		try {
			this.client = AbstractTest.getClient();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	
	public void startTesting() throws Exception {
		
		for (Map<String, Map<String, String>> params: paramValues) {
			
			System.out.println(params);
			
			for(List<String> round : testRounds) {
				for (String step : round) {
					Map<Object, Boolean> testcases = new LinkedHashMap<Object, Boolean>();
					String[] values = step.split("=");
					// 
					{
						Class<?> clazz = Class.forName(values[1]);
						// all parameters
						Map<String, Map<String, String>> allParams = generateAllParameters(params, clazz);
						
						// all objects
						List<Object> objList = generateAllObjects(clazz, allParams);
						
						// expected results
						expectedResults(testcases, objList);
					}
					
					{
						startTesting(testcases, values);
					}
				}
			}
		}
	}

	protected void startTesting(Map<Object, Boolean> testcases, String[] values)
			throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
		String category = values[0].substring(0, 1).toLowerCase() + values[0].substring(1) + "s";
		int pos = values[1].lastIndexOf("$");
		String lastname = values[1].substring(pos + 1);
		String methodName = lastname.substring(0, 1).toLowerCase() + lastname.substring(1);
		
		Set<String> whitelist = new HashSet<String>();
		
		for (Object param : testcases.keySet()) {
			Method method = client.getClass().getMethod(category);
			Object object = method.invoke(client);
			
			if (testcases.get(param) == false) {
				System.out.println("## Test"+ testId++ + ", " + param.getClass().getSimpleName() + "(Invalid parameters):\n\n ```\n" + JSON.toJSONString(param, true) + "\n```\n\n");
				
				if (methodName.startsWith("create") && !methodName.equals("createDiskSnapshot")) {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, NODENAME, param);
						System.out.println("Failure.\n\n");
						failure++;
					} catch (Exception ex) {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
					total++;
				} else {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, param);
						System.out.println("Failure.\n\n");
						failure++;
					} catch (Exception ex) {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
					total++;
				}
				continue;
			} else {
				
				if (whitelist.contains(param.getClass().getSimpleName() + "(Valid parameters)")) {
					continue;
				} else {
					whitelist.add(param.getClass().getSimpleName() + "(Valid parameters)");
				}
				
				System.out.println("## Test"+ testId++ + ", " + param.getClass().getSimpleName() + "(Valid parameters):\n\n ```\n" + JSON.toJSONString(param, true) + "\n```\n\n");
				
				if (methodName.startsWith("create") && !methodName.equals("createDiskSnapshot")) {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, NODENAME, param);
						check(object, false);
					} catch (Exception ex) {
						System.out.println("Failure.\n\n");
						failure++;
					}
					total++;
				} else if (methodName.startsWith("delete") || methodName.startsWith("remove")) {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, param);
						Thread.sleep(5000);
						Method get = object.getClass().getMethod("get");
						get.invoke(NAME_CorrectValue);
						failure++;
						
					} catch (Exception ex) {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
					total++;
				} else {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, param);
						check(object, false);
					} catch (Exception ex) {
						System.out.println("Failure.\n\n");
						failure++;
					}
					total++;
				}
				
				
				if (methodName.equals("changeNumberOfCPU") 
						|| methodName.equals("resizeRAM")
						|| methodName.equals("resizeDisk")) {
					continue;
				}
				
				System.out.println("## Test"+ testId++ + ", " + param.getClass().getSimpleName() + "(Duplicated parameters):\n\n ```\n" + JSON.toJSONString(param, true) + "\n```\n\n");
				
				if (methodName.startsWith("create") && !methodName.equals("createDiskSnapshot")) {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, NODENAME, param);
						check(object, true);
					} catch (Exception ex) {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
					total++;
				} else if (methodName.startsWith("delete") || methodName.startsWith("remove")) {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, param);
						Thread.sleep(5000);
						Method get = object.getClass().getMethod("get");
						get.invoke(NAME_CorrectValue);
						failure++;
						
					} catch (Exception ex) {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
					total++;
				} else {
					Method ref = object.getClass().getDeclaredMethod(methodName, String.class, param.getClass());
					try {
						ref.invoke(object, NAME_CorrectValue, param);
						check(object, true);
					} catch (Exception ex) {
						System.out.println("Failure.\n\n");
						failure++;
					}
					total++;
				}
			}
			
		}
	}

	@SuppressWarnings("unchecked")
	protected void check(Object object, boolean isExecption) throws Exception {
		Thread.sleep(5000);
		Method getObj = object.getClass().getMethod("get", String.class);
		Object obj = getObj.invoke(object, NAME_CorrectValue);
		
		Method getSpec = obj.getClass().getMethod("getSpec");
		
		Object spec = getSpec.invoke(obj);
		
		Method getStatus = spec.getClass().getMethod("getStatus");
		Status status = (Status) getStatus.invoke(spec); 
		
		int oo = 0;
		while (oo++ < 10) {
			if (status != null) {
				Map<String, Object> statusProps = status.getAdditionalProperties();	
				Map<String, Object> statusCond = (Map<String, Object>) (statusProps.get("conditions"));
				Map<String, Object> statusStat = (Map<String, Object>) (statusCond.get("state"));
				Map<String, Object> statusWait = (Map<String, Object>) (statusStat.get("waiting"));
				if (statusWait.get("reason").equals("Exception")
						|| statusWait.get("reason").equals("VirtctlError")
						|| statusWait.get("reason").equals("LibvirtError")
						|| statusWait.get("reason").equals("VirtletError")) {
					if (!isExecption) {
						System.out.println("Failure.\n\n");
						failure++;
					} else {
						System.out.println("Sucess.\n\n");
						sucess++;
					}
				} else {
					if (!isExecption) {
						System.out.println("Sucess.\n\n");
						sucess++;
					} else {
						System.out.println("Failure.\n\n");
						failure++;
					}
				}
				break;
			} else {
				Thread.sleep(3000);
				getObj = object.getClass().getMethod("get", String.class);
				obj = getObj.invoke(object, NAME_CorrectValue);
				
				getSpec = obj.getClass().getMethod("getSpec");
				
				spec = getSpec.invoke(obj);
				
				getStatus = spec.getClass().getMethod("getStatus");
				status = (Status) getStatus.invoke(spec); 
			}
		}
	}

	protected void expectedResults(Map<Object, Boolean> testcases, List<Object> objList)
			throws IllegalAccessException, InvocationTargetException, NoSuchMethodException {
		for (Object obj : objList) {
			
			boolean isTrue = true;
			// JSR 303
			for (Field field : obj.getClass().getDeclaredFields()) {
				ParameterDescriber param = field.getAnnotation(ParameterDescriber.class);
				if (param == null) {
					continue;
				}
				
				
				String fieldName = field.getName();
				String method = "get" + fieldName.substring(0, 1)
							.toUpperCase() + fieldName.substring(1);
				Object value = obj.getClass()
						.getMethod(method).invoke(obj);
				
				if (param.required() == false && value == null) {
					continue;
				}
				
				if (!(value instanceof String)) {
					continue;
				}
				
				Pattern pattern = field.getAnnotation(Pattern.class);
				
				if (pattern == null || pattern.regexp() == null) {
					continue;
				}
				
				String regexp = pattern.regexp();
				
				java.util.regex.Pattern checker = java.util.regex.Pattern.compile(regexp);
				if (!checker.matcher((String)value).matches()) {
					isTrue = false;
					break;
				}
			}
			
			testcases.put(obj, isTrue);
		}
	}

	protected List<Object> generateAllObjects(Class<?> clazz, Map<String, Map<String, String>> allParams)
			throws InstantiationException, IllegalAccessException, NoSuchMethodException, InvocationTargetException {
		// total Instances
		int totalIns = 1;
		
		for (String key : allParams.keySet()) {
			if (allParams == null || allParams.get(key) == null) {
				continue;
			}
			totalIns *= allParams.get(key).size();
		}
		
		List<Object> objList = new ArrayList<Object>();
		
		for (int ii = 0; ii < totalIns; ii++) {
			objList.add(clazz.newInstance());
		}
		
		// setvalues
		
		int rrr = 1;
		for (String name : allParams.keySet()) {
			if (name.equals("setLive") || name.equals("setConfig")) {
				Method methodRef = clazz.getDeclaredMethod(name, Boolean.class);
				for (Object obj : objList) {
					methodRef.invoke(obj, true);
				}
			} else if (name.equals("setPool")) {
				Method methodRef = clazz.getDeclaredMethod(name, String.class);
				for (Object obj : objList) {
					methodRef.invoke(obj, "default");
				}
			}else {
				try {
					Method methodRef = clazz.getDeclaredMethod(name, String.class);
					List<Object> objValues = new ArrayList<Object>();
				
					for (int ppp = 0; ppp < rrr; ppp++) {
						objValues.addAll(allParams.get(name).values());
					}
					
					for (int mm = 0; mm < objList.size(); mm++) {
						
						int idx = mm/(objList.size()/objValues.size());
						
						Object methodValue = objValues.get(idx);
						methodRef.invoke(objList.get(mm), methodValue);
					}
				} catch (Exception ex) {
					// ignore here
//					System.err.println(clazz + ":" + name);
				}
			}
			if (allParams.get(name) != null) {
				rrr *= allParams.get(name).size();
			}
		}
		return objList;
	}
			
			

	protected Map<String, Map<String, String>> generateAllParameters(Map<String, Map<String, String>> params, Class<?> clazz) {
		
		Map<String, Map<String, String>> allParams = new HashMap<String, Map<String, String>>();
		
		for (Field field : clazz.getDeclaredFields()) {
			ParameterDescriber param = field.getAnnotation(ParameterDescriber.class);
			if (param == null) {
				continue;
			}
			
			String methodName = "set" + field.getName().substring(0, 1).toUpperCase()
						+ field.getName().substring(1);
			
			if (field.getType().getName().equals(Boolean.class.getName())) {
				if (field.getName().equals("live") || field.getName().equals("config")) {
					allParams.put(methodName, null);
				}
				continue;
			} 
			
			if(!field.getType().getName().equals(String.class.getName())) {
				continue;
			}
			
			Pattern pattern = field.getAnnotation(Pattern.class);
			String regexp = pattern.regexp();
			Map<String, String> valueList = params.get(pregexpMap.get(regexp));
			
			if (clazz.getName().equals(CreateAndStartVMFromISO.class.getName())) {
				if (field.getName().equals("cdrom")) {
					Map<String, String> mv = new HashMap<String, String>();
					mv.put("ISO_Cdrom_CorrectValue", ISO_Cdrom_CorrectValue);
					mv.put("ISO_Cdrom_WrongValue", ISO_Cdrom_WrongValue);
					allParams.put(methodName, mv);
				} else if (field.getName().equals("disk")) {
					Map<String, String> mv = new HashMap<String, String>();
					mv.put("ISO_Disk_CorrectValue", ISO_Disk_CorrectValue);
					mv.put("ISO_Disk_WrongValue", ISO_Disk_WrongValue);
					allParams.put(methodName, mv);
				} else {
					allParams.put(methodName, valueList);
				}
			} else if (clazz.getName().equals(CreateAndStartVMFromImage.class.getName())) {
				if (field.getName().equals("cdrom")) {
					Map<String, String> mv = new HashMap<String, String>();
					mv.put("IMAGE_Cdrom_CorrectValue", IMAGE_Cdrom_CorrectValue);
					mv.put("IMAGE_Cdrom_WrongValue", IMAGE_Cdrom_WrongValue);
					allParams.put(methodName, mv);
				} else if (field.getName().equals("disk")) {
					Map<String, String> mv = new HashMap<String, String>();
					mv.put("IMAGE_Disk_CorrectValue", IMAGE_Disk_CorrectValue);
					mv.put("IMAGE_Disk_WrongValue", IMAGE_Disk_WrongValue);
					allParams.put(methodName, mv);
				} else {
					allParams.put(methodName, valueList);
				}
			} else {
				allParams.put(methodName, valueList);
			}
			
		}
		return allParams;
	}
			
	
	public static void main(String[] args) throws Exception {
		JUintFlowStep3Test jfs3 = new JUintFlowStep3Test();
		initParamValues();
		initRegExpMap();
		jfs3.startTesting();
		System.out.println("Total: " + total);
		System.out.println("Sucess:"  + sucess);
		System.out.println("Fail:"  + failure);
	}
	
}
