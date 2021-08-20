/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators.deprecated;

import java.util.List;

import io.fabric8.kubernetes.api.builder.Function;
import io.fabric8.kubernetes.client.CustomResourceDoneable;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since 2019/6/14
 * 
 * This code is used for generating Doneable class
 *
 */
public class DoneableResourceGenerator extends AbstractClassGenerator{

	public DoneableResourceGenerator(String pkgName) {
		super(pkgName);
	}

	public final static String CLASS = "\npublic class DoneableCLASS "
							+ "extends CustomResourceDoneable<CLASS> {\n";
	
	public final static String METHOD = "\n\tpublic DoneableCLASS"
							+ "(CLASS resource, Function function) {\n" 
							+ "\t\tsuper(resource, function);\n" 
							+ "\t}\n";
	

	public String autoGen(String classname) {
		dsb.append(CLASS.replaceAll("CLASS", classname))
			.append(METHOD.replaceAll("CLASS", classname)).append(END_CLASS);
		return dsb.toString();
	}

	@Override
	protected String getClassAnnotation() {
		return DEFAULT_ANNOTATION;
	}

	@Override
	protected List<String> getPackages() {
		packages.add(Function.class.getName());
		packages.add(CustomResourceDoneable.class.getName());
		return packages;
	}
	
	public static void main(String[] args) throws Exception {
		DoneableResourceGenerator gen = new DoneableResourceGenerator("com.uit.cloud.kubernetes.api.model");
		System.out.println(gen.autoGen("VirtualMachine"));
	}
}
