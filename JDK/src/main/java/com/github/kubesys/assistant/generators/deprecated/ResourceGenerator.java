/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators.deprecated;

import java.util.List;

import io.fabric8.kubernetes.client.CustomResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since 2019/6/14
 *
 */
public class ResourceGenerator extends AbstractClassGenerator {

	public final static String CLASS = "\npublic class CLASS "
								+ "extends CustomResource {\n";
	
	public final static String FIELD = "\n\tprivate CLASSSpec spec;\n";
	
	public final static String SET_METHOD = "\n\tpublic void setSpec"
								+ "(CLASSSpec spec) {\n" 
								+ "\t\tthis.spec = spec;\n\t}\n";
	
	public final static String GET_METHOD = "\n\tpublic CLASSSpec getSpec() {\n" 
							+ "\t\treturn this.spec;\n\t}\n";
	
	public ResourceGenerator(String pkgName) {
		super(pkgName);
	}

	public String autoGen(String classname) {
		dsb.append(CLASS.replaceAll("CLASS", classname))
			.append(FIELD.replaceAll("CLASS", classname))
			.append(SET_METHOD.replaceAll("CLASS", classname))
			.append(GET_METHOD.replaceAll("CLASS", classname))
			.append(END_CLASS);
		return dsb.toString();
	}

	@Override
	protected String getClassAnnotation() {
		return DEFAULT_ANNOTATION;
	}

	@Override
	protected List<String> getPackages() {
		packages.add(CustomResource.class.getName());
		return packages;
	}
	
	public static void main(String[] args) throws Exception {
		ResourceGenerator gen = new ResourceGenerator("com.uit.cloud.kubernetes.api.model");
		System.out.println(gen.autoGen("VirtualMachine"));
	}
}
