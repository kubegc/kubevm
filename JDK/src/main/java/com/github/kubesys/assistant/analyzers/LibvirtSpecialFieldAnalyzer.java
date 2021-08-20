/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.analyzers;

import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import com.github.kubesys.kubernetes.api.model.virtualmachine.Domain;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Volume;
import com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot.Domainsnapshot;


/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/3
 * 
 * Libvirt use the xml style, some attributes should 
 * convert from String to ArrayList
 */
public class LibvirtSpecialFieldAnalyzer {

	public static Set<String>  primitives = new HashSet<String>();
	
	public static List<String> results    = new ArrayList<String>();
	
	static {
		primitives.add(String.class.getName());
		primitives.add(Integer.class.getName());
		primitives.add(Boolean.class.getName());
		primitives.add(Long.class.getName());
		primitives.add("int");
		primitives.add("boolean");
		primitives.add("long");
	}
	
	protected static void analyser(Class<?> clazz) throws Exception {
		analyser(clazz.getSimpleName().toLowerCase(), clazz);
	}
	
	protected static void analyser(String parent, Class<?> clazz) throws Exception {
		for (Field field : clazz.getDeclaredFields()) {
			String typename = field.getType().getName();
			if (primitives.contains(typename)) {
				continue;
			} else if (typename.equals(ArrayList.class.getName())) {
				results.add(parent + "-" + field.getName());
			} else {
				analyser(parent + "-" + field.getName(), Class.forName(typename));
			}
		}
	}
	
	public static void main(String[] args) throws Exception {
		analyser(Class.forName(Domain.class.getName()));
		analyser(Class.forName(Volume.class.getName()));
		analyser(Class.forName(Domainsnapshot.class.getName()));
		for (String res : results) {
			System.out.println(res);
		}
		
	}
	
}
