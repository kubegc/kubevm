/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.assistant.generators.deprecated;

import java.io.File;
import java.io.FileInputStream;
import java.util.List;
import java.util.Map;

import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

import io.fabric8.kubernetes.api.model.KubernetesResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since 2019/6/14
 *
 */
public class ResourceSpecGenerator extends AbstractClassGenerator {

	public static int num = 0;
	
	public final static String ANNOTATION     = "@JsonDeserialize(\n\tusing = JsonDeserializer.None.class\n)";
	
	public final static String CLASS          = "\npublic class CLASSSpec implements KubernetesResource {\n";
	
	public final static String SUBCLASS       = "\n@JsonInclude(JsonInclude.Include.NON_NULL)" 
													+ "\n@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)" 
													+ "\npublic static class CLASS {\n";
	
	public final static String FIELD          = "\n\tprotected FTYPE FNAME;\n";
	
	public final static String SET_METHOD     =  "\n\t/**\n\t*  Ignore the user setting, use 'lifecycle' to update VM's info \n\t*\n\t*/"
							+ "\n\tpublic void setMNAME(FTYPE FNAME) {\n" 
							+ "\t\tthis.FNAME = FNAME;\n\t}\n";
	
	public final static String GET_METHOD     = "\n\tpublic FTYPE getMNAME() {\n" 
							+ "\t\treturn this.FNAME;\n\t}\n";
	
	public final static String CONSTRUCTOR    = "\n\tpublic CLASS() {\nINITIAL\n\t}\n";

	protected Map objMap;
	
	public ResourceSpecGenerator(String pkgName) {
		super(pkgName);
	}
	
	public Map getObjMap() {
		return objMap;
	}

	public void setObjMap(Map objMap) {
		this.objMap = objMap;
	}

	
	public String autoGen(String classname) {
		return autoGen(objMap, classname, false);
	}

	protected String autoGen(Map map, String classname, boolean subClass) {
		
		StringBuffer sb = new StringBuffer();
		if (!subClass) {
			sb.append(dsb).append(CLASS.replaceAll("CLASS", classname));
		} else {
			sb.append(SUBCLASS.replaceAll("CLASS", classname));
		}
		
		StringBuffer methods  =  new StringBuffer();
		
		StringBuffer subclass = new StringBuffer();
		
		StringBuffer constor  = new StringBuffer();
		
		for (Object key : map.keySet()) {
			
			Object value = map.get(key);
			
			String valueType = value.getClass().getName();
			
			String mname = key.toString().substring(0, 1).toUpperCase() + key.toString().substring(1);
			if (valueType.equals(JSONObject.class.getName())) {
				sb.append(FIELD.replaceAll("FTYPE", mname).replaceAll("FNAME", key.toString()));
				methods.append(SET_METHOD.replaceAll("FTYPE", mname).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
				methods.append(GET_METHOD.replaceAll("FTYPE", mname).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
				subclass.append(autoGen((Map) value, mname, true));
			} else if (valueType.equals(JSONArray.class.getName())) {
				String valueStr = map.get(key).toString();
				String fType = "";
				if (valueStr.startsWith("[{")) {
					fType = "ArrayList<" + mname + ">";
					subclass.append(autoGen((Map) ((List)map.get(key)).get(0), mname, true));
				} else if (valueStr.startsWith("[")) {
					fType = "ArrayList<String>";
				} 
				sb.append(FIELD.replaceAll("FTYPE", fType).replaceAll("FNAME", key.toString()));
				methods.append(SET_METHOD.replaceAll("FTYPE", fType).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
				methods.append(GET_METHOD.replaceAll("FTYPE", fType).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
			}	else {
				if (map.get(key).toString().equals("string")) {
					sb.append(FIELD.replaceAll("FTYPE", String.class.getSimpleName())
							.replaceAll("FNAME", key.toString()));
				} else {
					sb.append(FIELD.replaceAll("FTYPE", String.class.getSimpleName()).replaceAll("FNAME", key.toString()));
					constor.append("\t\tthis.").append(key.toString()).append(" = \"").append(map.get(key).toString()).append("\";\n");
				}
				methods.append(SET_METHOD.replaceAll("FTYPE", String.class.getSimpleName()).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
				methods.append(GET_METHOD.replaceAll("FTYPE", String.class.getSimpleName()).replaceAll("MNAME", mname).replaceAll("FNAME", key.toString()));
			}
		}
			
		String realName = (subClass == false) ? classname + "Spec" : classname;
		return sb.append(CONSTRUCTOR.replaceAll("CLASS", realName).replaceAll("INITIAL", constor.toString()))
						.append(methods).append(subclass).append(END_CLASS).toString();
	}

	@Override
	protected String getClassAnnotation() {
		return ANNOTATION;
	}

	@Override
	protected List<String> getPackages() {
		packages.add(JsonDeserializer.class.getName());
		packages.add(JsonDeserialize.class.getName());
		packages.add(KubernetesResource.class.getName());
		return packages;
	}
	
	public static void main(String[] args) throws Exception {
		ResourceSpecGenerator gen = new ResourceSpecGenerator("com.github.kubesys.kubernetes.api.model");
//		Map parseObject = JSON.parseObject(new FileInputStream(new File("conf/domain.json")), Map.class);
//		Map parseObject = JSON.parseObject(new FileInputStream(new File("conf/lifecycle.json")), Map.class);
//		Map parseObject = JSON.parseObject(new FileInputStream(new File("conf/volume.json")), Map.class);
//		Map parseObject = JSON.parseObject(new FileInputStream(new File("conf/snapshot.json")), Map.class);
		Map parseObject = JSON.parseObject(new FileInputStream(new File("conf/uitvol.json")), Map.class);
		gen.setObjMap(parseObject);
		System.out.println(gen.autoGen("VirtualMachine"));
		
	}
}
