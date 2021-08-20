/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.autotest;

import com.alibaba.fastjson.JSON;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/4
 * 
 **/
public class TestCase {
	
	protected String _mode;
	
	protected Mode mode;

	public String get_mode() {
		return _mode;
	}

	public void set_mode(String _mode) {
		this._mode = _mode;
	}

	public Mode getMode() {
		return mode;
	}

	public void setMode(Mode mode) {
		this.mode = mode;
	}

	public static class Mode {
		
		protected String a;
		
		protected String b;

		public String getA() {
			return a;
		}

		public void setA(String a) {
			this.a = a;
		}

		public String getB() {
			return b;
		}

		public void setB(String b) {
			this.b = b;
		}
		
	}
	
	public static void main(String[] args) {
		TestCase tc = new TestCase();
		tc.set_mode("hello");
		System.out.println(JSON.toJSONString(tc));
	}
	
}
