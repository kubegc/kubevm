/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.annotations.ClassDescriber;
import com.github.kubesys.kubernetes.annotations.FunctionDescriber;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/3
 *
 */
public class APIGenerator {
	
	public static void main(String[] args) throws Exception {
		
		StringBuffer sb = new StringBuffer();
		
		sb.append("# 文档简介").append("\n\n")
			.append("\t本文档用于说明基于Kubernetes的虚拟机生命周期如何管理, 项目地址：https://github.com/kubesys/kubeext-jdk.\n");
		
		sb.append("\t").append("本文有两种通用的约束:\n");
		sb.append("\t\t").append("(1)名称：只允许小写字母和、数字、中划线和圆点组合，4-100位\n");
		sb.append("\t\t").append("(2)路径：必须是/xx/xx形式，且在/var/lib/libvirt、/mnt/localfs或/mnt/usb目录下，xx允许小写字母、数字、中划线和点，18-1024位\n\n\n");
		sb.append("\t\t").append("(3)目前JDK提供的参数数量多余文档，以文档为准，其它为预留参数，传入会导致系统失败\n\n\n");
		
		int i = 1; 
		for (String classname : JSONGenerator.list) {
			
			Class<?> forName = Class.forName(classname);
			ClassDescriber parent = forName.getAnnotation(ClassDescriber.class);
			if (parent == null) {
				continue;
			}
			
			sb.append("# ").append(i).append(" ")
				.append(parent.value()).append("\n\n");
			
			sb.append(parent.desc() + "." + parent.value() + "所有操作的返回值一样，见**[返回值]**\n\n");
			
			int j = 1;
			for (Field field : forName.getDeclaredFields()) {
				
				FunctionDescriber function = field.getAnnotation(FunctionDescriber.class);
				
				try {
					sb.append("## ").append(i).append(".").append(j++).append(" ")
						.append(field.getType().getSimpleName())
						.append("(").append(function.shortName()).append(")").append("\n\n");
				} catch (Exception ex) {
					System.out.println(ex);
				}
				if (function != null) {
					sb.append("**接口功能:**").append("\n");
					sb.append("\t").append(function.description()).append("\n\n");
					
					sb.append("**接口依赖:**").append("\n");
					sb.append("\t").append(function.prerequisite()).append("\n\n");
					
					sb.append("**接口所属:**").append("\n");
					sb.append("\t").append(classname).append(".").append(field.getType().getSimpleName()).append("\n\n");
					
					sb.append("**参数描述:**").append("\n\n");
					
					sb.append("| name | type | required | description | exampe |").append("\n");
					sb.append("| ----- | ------ | ------ | ------ | ------ |").append("\n");
					sb.append("| name | String | true | 资源名称 | " + field.getName() + ".name.001|").append("\n");
					if (field.getName().startsWith("create")) {
						sb.append("| nodeName | String | false | 选择部署的物理机，可以通过kubernetes.nodes().list进行查询 | node22 |").append("\n");
					}
					sb.append("| " + field.getName() + " | " + field.getType().getSimpleName() + " | true | " + function.shortName() + " | 详细见下 |").append("\n");
					sb.append("| eventId | String | fasle | 事件ID | " + field.getName() + ".event.001 |").append("\n\n");
					
					sb.append("对象" + field.getName() + "参数说明:\n\n");
					
					sb.append("| name | type | required | description | constraint | example |").append("\n");
					sb.append("| ----- | ------ | ------ | ------ | ------ | ------ |").append("\n");
					
					List<Field> fileds = new ArrayList<Field>();
					
					Class<?> nameType = field.getType();
					while (nameType.getName() != Object.class.getName()) {
						fileds.addAll(Arrays.asList(nameType.getDeclaredFields()));
						nameType = nameType.getSuperclass();
					}
					
					for(Field ff : fileds) {
						ParameterDescriber ffp = ff.getAnnotation(ParameterDescriber.class);
						if (ffp == null) {
							continue;
						}
						
						sb.append("| ").append(ff.getName()).append("|")
							.append(ff.getType().getSimpleName()).append("|")
							.append(ffp.required()).append("|")
							.append(ffp.description()).append("|")
							.append(ffp.constraint()).append("|")
							.append(ffp.example()).append("|\n");
					}
					sb.append("|  |  |  |  |  |").append("\n\n");
					
					sb.append("**接口异常:**").append("\n\n");
					sb.append("(1)在调用本方法抛出;").append("\n\n");
					
					sb.append("| name  | description | ").append("\n");
					sb.append("| ----- | ----- | ").append("\n");
					sb.append("| RuntimeException |  重名，或则资源(VirtualMachine, VirtualMachinePool等)不存在   |").append("\n");
					sb.append("| IllegalFormatException | 传递的参数不符合约束条件    |").append("\n");
					sb.append("| Exception    | 后台代码异常，比如未安装VM的Kubernets插件    |").append("\n\n");
					
					sb.append("(2)调用本方法返回True，因本API是异步处理，开发者需要进一步监听是否正确执行。本文考虑第(2)种情况"
							+ "请查看" + field.getType().getSimpleName() + "spec下的status域，从message中获取详细异常信息").append("\n\n");
					
					sb.append("| name  | description | ").append("\n");
					sb.append("| ----- | ----- | ").append("\n");
					sb.append("| LibvirtError | 因传递错误参数，或者后台缺少软件包导致执行Libvirt命令出错   |").append("\n");
					sb.append("| VirtctlError | Libvirt不支持的生命周期    |").append("\n");
					sb.append("| VirtletError | Libvirt监听事件错误，比如绕开Kubernetes,后台执行操作  |").append("\n");
					sb.append("| Exception    | 后台代码异常退出,比如主机的hostname变化    |").append("\n\n");
					
				}
			}
			sb.append("## **返回值:**").append("\n\n");
			sb.append("```").append("\n");
			Object obj = Class.forName("com.github.kubesys.kubernetes.api.model." + parent.value()).newInstance();
			JSONGenerator.instance(obj);
			sb.append(JSON.toJSONString(obj, true)).append("\n");
			sb.append("```").append("\n");
			i++;
		}
		
		System.out.println(sb.toString());
	}
}
