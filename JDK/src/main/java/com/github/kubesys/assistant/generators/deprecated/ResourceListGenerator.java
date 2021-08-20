/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators.deprecated;

import java.util.List;

import io.fabric8.kubernetes.client.CustomResourceList;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since 2019/6/14
 *
 */
public class ResourceListGenerator extends AbstractClassGenerator {

	public final static String CLASS = "\npublic class CLASSList "
								+ "extends CustomResourceList<CLASS> {\n";
	
	public ResourceListGenerator(String pkgName) {
		super(pkgName);
	}
	
	public String autoGen(String classname) {
		dsb.append(CLASS.replaceAll("CLASS", classname)).append(END_CLASS);
		return dsb.toString();
	}

	@Override
	protected String getClassAnnotation() {
		return "";
	}

	@Override
	protected List<String> getPackages() {
		packages.add(CustomResourceList.class.getName());
		return packages;
	}
	
	public static void main(String[] args) throws Exception {
		ResourceListGenerator gen = new ResourceListGenerator("com.uit.cloud.kubernetes.api.model");
		System.out.println(gen.autoGen("VirtualMachine"));
	
	}
}
