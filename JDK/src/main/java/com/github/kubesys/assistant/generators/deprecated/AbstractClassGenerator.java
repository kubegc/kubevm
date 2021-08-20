/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators.deprecated;

import java.util.ArrayList;
import java.util.Date;
import java.util.List;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since 2019/6/14
 * This class is used for generating various classes automatically. <br>
 * A typical class includes: <br>
 * 1. copyright
 * 2. package name <br>
 * 3. import packages <br>
 * 4. authors <br>
 * 5. class annotations <br>
 * 6. class <br>
 * 
 */
public abstract class AbstractClassGenerator {

	public final static String COPYRIGHT = "/**\r\n" + " * Copyright (2019, ) Institute of Software, "
									+ "Chinese Academy of Sciences\r\n" + " */\n";

	public final static String PACKAGE = "package PACKAGE;\n\n";
	
	public final static String IMPORT = "import IMPORT;\n";
	
	public final static String AUTHOR = "\n\n/**\r\n" 
									+ " * @author wuheng@otcaix.iscas.ac.cn\r\n"
									+ " * @author xuyuanjia2017@otcaix.iscas.ac.cn\r\n" 
									+ " * @author xianghao16@otcaix.iscas.ac.cn\r\n" 
									+ " * @author yangchen18@otcaix.iscas.ac.cn\r\n" 
									+ " * @since " + new Date() + "\r\n"
									+ " **/";
	
	public final static String END_CLASS = "}\n";
	
	public final static String DEFAULT_ANNOTATION = "";

	protected final static List<String> packages = new ArrayList<String>();
	
	static {
		packages.add(List.class.getName());
		packages.add(ArrayList.class.getName());
	}
	
	protected final StringBuffer dsb = new StringBuffer();
	
	/**
	 * @param pkg package name
	 */
	public AbstractClassGenerator(String pkg) {
		dsb.append(COPYRIGHT)
			.append(PACKAGE.replaceAll("PACKAGE", pkg))
			.append(getImports())
			.append(AUTHOR)
			.append(getClassAnnotation());
	}
	
	/**
	 * @return imports
	 */
	public String getImports() {
		StringBuffer sb = new StringBuffer();
		for (String pkg : getPackages()) {
			sb.append(IMPORT.replaceAll("IMPORT", pkg));
		}
		return sb.toString();
	}
	
	/**
	 * @param classname class name
	 * @return class content
	 */
	public abstract String autoGen(String classname);
	
	/**
	 * @return annotation
	 */
	protected abstract String getClassAnnotation();
	
	/**
	 * @return package list
	 */
	protected abstract List<String> getPackages();
	
}
