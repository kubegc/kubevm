/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.henry;

import java.util.regex.Pattern;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  2019/7/15
 *
 */
public class RegExpTest {

	protected static String NAME_PATTERN = "[a-z0-9-]{8,32}";
	
	protected static String PATH_PATTERN = "[a-z0-9A-Z-_/./]{2,1024}";
	
	protected static String NUMB_PATTERN = "\\d{3,4}";
	
	protected static String ENUM_PATTERN = "qcow2|raw";

	public static void main(String[] args) {
		checkName();
//		checkPath();
//		checkNumber();
//		checkEnum();
	}

	protected static void checkEnum()  {
		Pattern r = Pattern.compile(ENUM_PATTERN);
		System.out.println(r.matcher("qcow2").matches());
	}

	protected static void checkNumber() {
		Pattern r = Pattern.compile(NUMB_PATTERN);
		System.out.println(r.matcher("700").matches());
	}

	protected static void checkPath() {
		Pattern r = Pattern.compile(PATH_PATTERN);
		System.out.println(r.matcher("/opt/ISO/CentOS-7-x86_64-Minimal-1511.iso").matches());
	}

	protected static void checkName() {
		Pattern r = Pattern.compile(NAME_PATTERN);
		System.out.println(r.matcher("650-----").matches());
//		System.out.println(r.matcher("650646e8c17a49d0b83c1c797811e064").matches());
	}
}
