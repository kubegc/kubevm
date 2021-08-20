/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachineimage;

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
@ClassDescriber(value = "VirtualMachineImage", desc = "虚拟机模板，包括CPU、内存、OS等信息")
public class Lifecycle {

	@FunctionDescriber(shortName = "创建虚拟机镜像", description = "创建虚拟机镜像，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected CreateImage createImage;
	
	@FunctionDescriber(shortName = "删除虚拟机镜像", description = "删除虚拟机镜像，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMI, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected DeleteImage deleteImage;
	
	@FunctionDescriber(shortName = "将虚拟机镜像转化为虚拟机", description = "将虚拟机镜像转化为虚拟机，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMI, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected ConvertImageToVM convertImageToVM;

	public Lifecycle() {

	}

	public ConvertImageToVM getConvertImageToVM() {
		return convertImageToVM;
	}

	public void setConvertImageToVM(ConvertImageToVM convertImageToVM) {
		this.convertImageToVM = convertImageToVM;
	}

	public CreateImage getCreateImage() {
		return createImage;
	}

	public void setCreateImage(CreateImage createImage) {
		this.createImage = createImage;
	}

	public DeleteImage getDeleteImage() {
		return deleteImage;
	}

	public void setDeleteImage(DeleteImage deleteImage) {
		this.deleteImage = deleteImage;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class CreateImage {

		@ParameterDescriber(required = true, description = "用于创建虚拟机镜像的源文件", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/aaa.qcow2")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String disk;
		
		@ParameterDescriber(required = true, description = "目标存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String targetPool;

		public CreateImage() {
			super();
		}

		public String getTargetPool() {
			return targetPool;
		}

		public void setTargetPool(String targetPool) {
			this.targetPool = targetPool;
		}

		public String getDisk() {
			return disk;
		}

		public void setDisk(String disk) {
			this.disk = disk;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class DeleteImage {
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class ConvertImageToVM {
		
		@ParameterDescriber(required = true, description = "目标存储池名", constraint = "由4-100位的数字和小写字母组成，已创建出的存储池", example = "pool2")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String targetPool;

		public String getTargetPool() {
			return targetPool;
		}

		public void setTargetPool(String targetPool) {
			this.targetPool = targetPool;
		}
		
	}
	
}
