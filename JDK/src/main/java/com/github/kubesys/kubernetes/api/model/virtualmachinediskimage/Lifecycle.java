/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinediskimage;

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
@ClassDescriber(value = "VirtualMachineDiskImage", desc = "云盘模板，主要是指大小和文件格式等")
public class Lifecycle {
	
	@FunctionDescriber(shortName = "从云盘创建云盘镜像", description = "从云盘创建云盘镜像，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
			prerequisite = AnnotationUtils.DESC_FUNCTION_VMD, 
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateDiskImageFromDisk createDiskImageFromDisk;
	
	@FunctionDescriber(shortName = "创建云盘镜像", description = "创建云盘镜像，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
			prerequisite = "", 
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateDiskImage createDiskImage;

	@FunctionDescriber(shortName = "删除云盘镜像", description = "删除云盘镜像，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMDI, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteDiskImage deleteDiskImage;
	
	public CreateDiskImageFromDisk getCreateDiskImageFromDisk() {
		return createDiskImageFromDisk;
	}

	public void setCreateDiskImageFromDisk(CreateDiskImageFromDisk createDiskImageFromDisk) {
		this.createDiskImageFromDisk = createDiskImageFromDisk;
	}

	public DeleteDiskImage getDeleteDiskImage() {
		return deleteDiskImage;
	}
	
	public void setDeleteDiskImage(DeleteDiskImage deleteDiskImage) {
		this.deleteDiskImage = deleteDiskImage;
	}
	
	public CreateDiskImage getCreateDiskImage() {
		return createDiskImage;
	}
	
	public void setCreateDiskImage(CreateDiskImage createDiskImage) {
		this.createDiskImage = createDiskImage;
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteDiskImage {
		
		@ParameterDescriber(required = true, description = "源存储池名，源云盘所在的存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String sourcePool;

		public String getSourcePool() {
			return sourcePool;
		}

		public void setSourcePool(String sourcePool) {
			this.sourcePool = sourcePool;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateDiskImageFromDisk {
		
		@ParameterDescriber(required = true, description = "目标存储池名，用于存储创建的云盘镜像", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String targetPool;
		
		@ParameterDescriber(required = true, description = "源存储池名，源云盘所在的存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String sourcePool;
		
		@ParameterDescriber(required = true, description = "源云盘名称，用于创建云盘镜像的云盘名称", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "volume1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String sourceVolume;

		public String getSourcePool() {
			return sourcePool;
		}

		public void setSourcePool(String sourcePool) {
			this.sourcePool = sourcePool;
		}

		public String getSourceVolume() {
			return sourceVolume;
		}

		public void setSourceVolume(String sourceVolume) {
			this.sourceVolume = sourceVolume;
		}

		public String getTargetPool() {
			return targetPool;
		}

		public void setTargetPool(String targetPool) {
			this.targetPool = targetPool;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateDiskImage {

//		@ParameterDescriber(required = true, description = "要转化为云盘镜像的源文件路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/test.qcow2")
////		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
//		protected String source;
		
		@ParameterDescriber(required = true, description = "目标存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String targetPool;

		public String getTargetPool() {
			return targetPool;
		}

		public void setTargetPool(String targetPool) {
			this.targetPool = targetPool;
		}

//		public String getSource() {
//			return source;
//		}
//
//		public void setSource(String source) {
//			this.source = source;
//		}
	}
	
}
