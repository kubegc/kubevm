/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import com.alibaba.fastjson.JSON;

/**
 * @version 1.0.0
 * @since   2019/9/3
 *
 */
public class JSONGenerator {
	
	public final static List<String> list = new ArrayList<String>();
	
	static {
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachineimage.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinediskimage.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinedisksnapshot.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinenetwork.Lifecycle");
		list.add("com.github.kubesys.kubernetes.api.model.virtualmachinebackup.Lifecycle");
	}
	
	@SuppressWarnings({ "rawtypes", "unchecked" })
	protected static void instance(Object obj) throws Exception {
		Class<? extends Object> clazz = obj.getClass();
		for (Field field : clazz.getDeclaredFields()) {
			if (field.getModifiers() == 26) {
				continue;
			}
			String typename = field.getType().getName();
			Method m = clazz.getMethod(
					setMethod(field.getName()), 
					field.getType());
			if (typename.equals(String.class.getName())) {
				m.invoke(obj, "String");
			} else if (typename.equals("boolean")
					|| typename.equals(Boolean.class.getName()))  {
				m.invoke(obj, true);
			} else if (typename.equals("int")
					|| typename.equals(Integer.class.getName()))  {
				m.invoke(obj, 1);
			} else if (typename.equals(ArrayList.class.getName())
					|| typename.equals(List.class.getName())
					|| typename.equals(Set.class.getName())) {
				String generictype = field.getGenericType().getTypeName();
				int start = generictype.indexOf("<");
				int end   = generictype.indexOf(">");
				String realtype = generictype.substring(start + 1, end);
				List list = new ArrayList();
				if (realtype.equals(String.class.getName())) {
					list.add("String");
					list.add("String");
				} else if (realtype.equals("boolean")
						|| realtype.equals(Boolean.class.getName()))  {
					list.add(true);
					list.add(true);
				} else if (realtype.equals("int")
						|| realtype.equals(Integer.class.getName()))  {
					list.add(1);
					list.add(1);
				} else {
					Object ins1 = Class.forName(realtype).newInstance();
					list.add(ins1);
					instance(ins1);
					
					Object ins2 = Class.forName(realtype).newInstance();
					list.add(ins2);
					instance(ins2);
				}
				m.invoke(obj, list);
			} else {
				
				if (typename.equals(obj.getClass().getTypeName())) {
					System.out.println("Warning: infinite loop for" + typename);
					continue;
				}
				
				Object param = Class.forName(typename).newInstance();
				m.invoke(obj, param);
				instance(param);
			}
		}
	}
	
	protected static String setMethod(String name) {
		return "set" + name.substring(0, 1).toUpperCase()
							+ name.substring(1);
	}
	
	public static void main(String[] args) throws Exception {
		for (String name : list) {
			Object obj = Class.forName(name).newInstance();
			instance(obj);
			System.out.println(JSON.toJSONString(obj, true));
		}
	}
	
}
