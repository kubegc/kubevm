/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinebackup;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.annotations.ClassDescriber;
import com.github.kubesys.kubernetes.annotations.FunctionDescriber;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;
import com.github.kubesys.kubernetes.utils.AnnotationUtils;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

import javax.validation.constraints.Pattern;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/4
 * 
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
@ClassDescriber(value = "VirtualMachineBackup", desc = "扩展支持各种容灾功能")
public class Lifecycle {
	
//	@FunctionDescriber(shortName = "清理本地存储服务器虚拟机无效备份", description = "开机启动存储池，否则开机该存储池会连接不上，导致不可用。适用libvirt指令创建存储池情况。"
//			+ AnnotationUtils.DESC_FUNCTION_DESC,
//		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP,
//		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
//	protected CleanVMBackup cleanVMBackup;
//
//	public CleanVMBackup getCleanVMBackup() {
//		return cleanVMBackup;
//	}
//
//	public void setCleanVMBackup(CleanVMBackup cleanVMBackup) {
//		this.cleanVMBackup = cleanVMBackup;
//	}
//
//	@JsonInclude(JsonInclude.Include.NON_NULL)
//	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
//	public static class CleanVMBackup {
//
//		protected String domain;
//
//	    protected String pool;
//
//		protected String version;
//
//		public String getDomain() {
//			return domain;
//		}
//
//		public void setDomain(String domain) {
//			this.domain = domain;
//		}
//
//		public String getPool() {
//			return pool;
//		}
//
//		public void setPool(String pool) {
//			this.pool = pool;
//		}
//
//		public String getVersion() {
//			return version;
//		}
//
//		public void setVersion(String version) {
//			this.version = version;
//		}
//	}

}
