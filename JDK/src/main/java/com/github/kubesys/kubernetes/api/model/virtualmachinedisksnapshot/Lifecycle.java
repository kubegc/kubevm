/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinedisksnapshot;

import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.annotations.FunctionDescriber;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;
import com.github.kubesys.kubernetes.annotations.ClassDescriber;
import com.github.kubesys.kubernetes.utils.AnnotationUtils;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/4
 * 
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
@ClassDescriber(value = "VirtualMachineDiskSnapshot", desc = "云盘快照是指云盘的外部快照，目前支持QCOW2格式")
public class Lifecycle {

	@FunctionDescriber(shortName = "创建云盘外部快照", description = "创建云盘外部快照，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMDSN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateDiskExternalSnapshot createDiskExternalSnapshot;
	
	@FunctionDescriber(shortName = "从云盘外部快照恢复", description = "从云盘外部快照恢复，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMDSN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected RevertDiskExternalSnapshot revertDiskExternalSnapshot;
	
	@FunctionDescriber(shortName = "删除云盘外部快照", description = "删除云盘外部快照，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMDSN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteDiskExternalSnapshot deleteDiskExternalSnapshot;
	
	public CreateDiskExternalSnapshot getCreateDiskExternalSnapshot() {
		return createDiskExternalSnapshot;
	}

	public void setCreateDiskExternalSnapshot(CreateDiskExternalSnapshot createDiskExternalSnapshot) {
		this.createDiskExternalSnapshot = createDiskExternalSnapshot;
	}

	public DeleteDiskExternalSnapshot getDeleteDiskExternalSnapshot() {
		return deleteDiskExternalSnapshot;
	}

	public void setDeleteDiskExternalSnapshot(DeleteDiskExternalSnapshot deleteDiskExternalSnapshot) {
		this.deleteDiskExternalSnapshot = deleteDiskExternalSnapshot;
	}

	public RevertDiskExternalSnapshot getRevertDiskExternalSnapshot() {
		return revertDiskExternalSnapshot;
	}

	public void setRevertDiskExternalSnapshot(RevertDiskExternalSnapshot revertDiskExternalSnapshot) {
		this.revertDiskExternalSnapshot = revertDiskExternalSnapshot;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateDiskExternalSnapshot{
		@ParameterDescriber(required = true, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
		protected String type;

		@ParameterDescriber(required = true, description = "云盘所在的存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池，只支持localfs、nfs和glusterfs类型", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "云盘文件的类型", constraint = "qcow2", example = "qcow2")
		@Pattern(regexp = RegExpUtils.DISK_SUBDRIVER_PATTERN)
		protected String format;

		@ParameterDescriber(required = true, description = "云盘名", constraint = "磁盘和快照", example = "disk1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;
		
		@ParameterDescriber(required = false, description = "若该云盘加载到虚拟机内（包括系统盘、数据盘），则需要填写该虚拟机名，否则将报错Write lock", constraint = "已存在的虚拟机名，由4-100位的数字和小写字母组成", example = "950646e8c17a49d0b83c1c797811e001")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getFormat() {
			return format;
		}

		public void setFormat(String format) {
			this.format = format;
		}

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RevertDiskExternalSnapshot {

		@ParameterDescriber(required = true, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
		protected String type;
		
		@ParameterDescriber(required = true, description = "云盘所在的存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "云盘名", constraint = "磁盘和快照", example = "disk1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "云盘文件的类型", constraint = "qcow2", example = "qcow2")
		@Pattern(regexp = RegExpUtils.DISK_SUBDRIVER_PATTERN)
		protected String format;

		@ParameterDescriber(required = false, description = "若该云盘加载到虚拟机内（包括系统盘、数据盘），虚拟机需要处于关机状态，且需要填写该虚拟机名，否则将报错Write lock", constraint = "已存在的虚拟机名，由4-100位的数字和小写字母组成", example = "950646e8c17a49d0b83c1c797811e001")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}

		public String getFormat() {
			return format;
		}

		public void setFormat(String format) {
			this.format = format;
		}

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteDiskExternalSnapshot{
		@ParameterDescriber(required = true, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
		protected String type;

		@ParameterDescriber(required = true, description = "云盘所在的存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "云盘名", constraint = "磁盘和快照", example = "disk1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;
		
		@ParameterDescriber(required = false, description = "若该云盘加载到虚拟机内（包括系统盘、数据盘），则需要填写该虚拟机名，否则将报错Write lock", constraint = "已存在的虚拟机名，由4-100位的数字和小写字母组成", example = "950646e8c17a49d0b83c1c797811e001")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}

	}
	
}
