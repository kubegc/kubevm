/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot;

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
@ClassDescriber(value = "VirtualMachineSnapshot", desc = "虚拟机/云盘快照")
public class Lifecycle {

	@FunctionDescriber(shortName = "删除虚拟机和挂载到虚拟机的云盘快照", description = "删除虚拟机和挂载到虚拟机的云盘快照，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMSN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteSnapshot deleteSnapshot;

	@FunctionDescriber(shortName = "创建虚拟机快照和挂载到虚拟机的云盘快照", description = "创建虚拟机快照和挂载到虚拟机的云盘快照，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateSnapshot createSnapshot;
	
	@FunctionDescriber(shortName = "恢复成虚拟机和挂载到虚拟机的云盘快照", description = "恢复成虚拟机和挂载到虚拟机的云盘快照，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMSN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected RevertVirtualMachine revertVirtualMachine;
	
	@FunctionDescriber(shortName = "全拷贝快照到文件", description = "全拷贝快照到文件，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMD, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected CopySnapshot copySnapshot;
	
	@FunctionDescriber(shortName = "合并快照到叶子节点", description = "合并快照到叶子节点，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMD, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected MergeSnapshot mergeSnapshot;
	
	public MergeSnapshot getMergeSnapshot() {
		return mergeSnapshot;
	}

	public void setMergeSnapshot(MergeSnapshot mergeSnapshot) {
		this.mergeSnapshot = mergeSnapshot;
	}

	public CopySnapshot getCopySnapshot() {
		return copySnapshot;
	}

	public void setCopySnapshot(CopySnapshot copySnapshot) {
		this.copySnapshot = copySnapshot;
	}

	public Lifecycle() {

	}

	public DeleteSnapshot getDeleteSnapshot() {
		return deleteSnapshot;
	}

	public void setDeleteSnapshot(DeleteSnapshot deleteSnapshot) {
		this.deleteSnapshot = deleteSnapshot;
	}

	public CreateSnapshot getCreateSnapshot() {
		return createSnapshot;
	}

	public void setCreateSnapshot(CreateSnapshot createSnapshot) {
		this.createSnapshot = createSnapshot;
	}
	
	public RevertVirtualMachine getRevertVirtualMachine() {
		return revertVirtualMachine;
	}

	public void setRevertVirtualMachine(RevertVirtualMachine revertVirtualMachine) {
		this.revertVirtualMachine = revertVirtualMachine;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class CreateSnapshot {

		@ParameterDescriber(required = true, description = "虚拟机快照的设置", 
				constraint = "vda(对哪个磁盘做快照，多个请参考示例),snapshot=external/internal/no(快照类型，支持external：外部,internal:内部,no:不做快照),file=/var/lib/libvirt/snapshots/snapshot1(快照文件的存放路径),drvier=qcow2（只支持qcow2）", 
				example = "只对系统盘做快照示例：vda,snapshot=external,file=/var/lib/libvirt/snapshots/snapshot1,drvier=qcow2 --diskspec vdb,snapshot=no")
		protected String diskspec;
		
		protected Boolean no_metadata;

		protected Boolean disk_only;

		protected String memspec;

		protected String description;

		protected Boolean quiesce;

		protected Boolean reuse_external;

		protected Boolean halt;

		protected Boolean atomic;

		@ParameterDescriber(required = true, description = "与快照关联的虚拟机名字", constraint = "已存在的虚拟机名，由4-100位的数字和小写字母组成", example = "950646e8c17a49d0b83c1c797811e001")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		protected Boolean live;
		
		@ParameterDescriber(required = false, description = "是否为外部快照", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean isExternal;

		public Boolean getIsExternal() {
			return isExternal;
		}

		public void setIsExternal(Boolean isExternal) {
			this.isExternal = isExternal;
		}

		public CreateSnapshot() {

		}

		public void setDiskspec(String diskspec) {
			this.diskspec = diskspec;
		}

		public String getDiskspec() {
			return this.diskspec;
		}

		public void setNo_metadata(Boolean no_metadata) {
			this.no_metadata = no_metadata;
		}

		public Boolean getNo_metadata() {
			return this.no_metadata;
		}

		public void setDisk_only(Boolean disk_only) {
			this.disk_only = disk_only;
		}

		public Boolean getDisk_only() {
			return this.disk_only;
		}

		public void setMemspec(String memspec) {
			this.memspec = memspec;
		}

		public String getMemspec() {
			return this.memspec;
		}

		public void setDescription(String description) {
			this.description = description;
		}

		public String getDescription() {
			return this.description;
		}

		public void setQuiesce(Boolean quiesce) {
			this.quiesce = quiesce;
		}

		public Boolean getQuiesce() {
			return this.quiesce;
		}

		public void setReuse_external(Boolean reuse_external) {
			this.reuse_external = reuse_external;
		}

		public Boolean getReuse_external() {
			return this.reuse_external;
		}

		public void setHalt(Boolean halt) {
			this.halt = halt;
		}

		public Boolean getHalt() {
			return this.halt;
		}

		public void setAtomic(Boolean atomic) {
			this.atomic = atomic;
		}

		public Boolean getAtomic() {
			return this.atomic;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getDomain() {
			return this.domain;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getLive() {
			return this.live;
		}
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class DeleteSnapshot {

		protected Boolean metadata;

		protected Boolean children;

		protected Boolean children_only;
		
		@ParameterDescriber(required = true, description = "要删除快照的虚拟机名字", constraint = "由4-100位的数字和小写字母组成，已存在的虚拟机名", example = "centos1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;
		
		@ParameterDescriber(required = false, description = "是否为外部快照", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean isExternal;

		public Boolean getIsExternal() {
			return isExternal;
		}

		public void setIsExternal(Boolean isExternal) {
			this.isExternal = isExternal;
		}

		public DeleteSnapshot() {

		}

		public void setMetadata(Boolean metadata) {
			this.metadata = metadata;
		}

		public Boolean getMetadata() {
			return this.metadata;
		}

		public void setChildren(Boolean children) {
			this.children = children;
		}

		public Boolean getChildren() {
			return this.children;
		}

		public void setChildren_only(Boolean children_only) {
			this.children_only = children_only;
		}

		public Boolean getChildren_only() {
			return this.children_only;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getDomain() {
			return this.domain;
		}

	}
	

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class RevertVirtualMachine {

		@ParameterDescriber(required = true, description = "要恢复到快照状态的虚拟机name", constraint = "由4-100位的数字和小写字母组成，已存在的虚拟机名", example = "centos1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = false, description = "恢复到快照的状态后，是否将虚拟机转换到开机状态", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean running;
		
		protected Boolean paused;
		
		protected Boolean force;
		
		@ParameterDescriber(required = false, description = "是否为外部快照", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean isExternal;

		public Boolean getIsExternal() {
			return isExternal;
		}

		public void setIsExternal(Boolean isExternal) {
			this.isExternal = isExternal;
		}

		public Boolean getRunning() {
			return running;
		}
		
		public String getDomain() {
			return domain;
		}
		
		public void setDomain(String domain) {
			this.domain = domain;
		}

		public void setRunning(Boolean running) {
			this.running = running;
		}

		public Boolean getPaused() {
			return paused;
		}

		public void setPaused(Boolean paused) {
			this.paused = paused;
		}

		public Boolean getForce() {
			return force;
		}

		public void setForce(Boolean force) {
			this.force = force;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class MergeSnapshot {
		
		protected String bandwidth;
		
		@ParameterDescriber(required = true, description = "对该虚拟机进行快照合并，合并到叶子节点。假设当前快照链为root->snapshot1->snapshot2->current，则mergeSnapshot(snapshot1)的结果为把snapshot1,snapshot2合并到current，快照链变为root->top", constraint= "由4-100位的数字和小写字母组成，已存在的虚拟机名", example = "centos1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;
		
		@ParameterDescriber(required = false, description = "是否为外部快照", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean isExternal;
		
		public Boolean getIsExternal() {
			return isExternal;
		}

		public void setIsExternal(Boolean isExternal) {
			this.isExternal = isExternal;
		}

		public String getBandwidth() {
			return bandwidth;
		}

		public void setBandwidth(String bandwidth) {
			this.bandwidth = bandwidth;
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
	@Deprecated
	public static class CopySnapshot extends MergeSnapshot {
		
		@ParameterDescriber(required = false, description = "是否为外部快照", constraint=AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean isExternal;
		
		protected String dest;
		
		protected String granularity;
		
		protected String buf_size;
		
		protected Boolean shallow;
		
		protected Boolean reuse_external;
		
		protected Boolean blockdev;
		
		protected Boolean pivot;
		
		protected Boolean finish;
		
		protected Boolean transient_job;

		public Boolean getIsExternal() {
			return isExternal;
		}

		public void setIsExternal(Boolean isExternal) {
			this.isExternal = isExternal;
		}

		public String getDest() {
			return dest;
		}

		public void setDest(String dest) {
			this.dest = dest;
		}

		public String getGranularity() {
			return granularity;
		}

		public void setGranularity(String granularity) {
			this.granularity = granularity;
		}

		public String getBuf_size() {
			return buf_size;
		}

		public void setBuf_size(String buf_size) {
			this.buf_size = buf_size;
		}

		public Boolean getShallow() {
			return shallow;
		}

		public void setShallow(Boolean shallow) {
			this.shallow = shallow;
		}

		public Boolean getReuse_external() {
			return reuse_external;
		}

		public void setReuse_external(Boolean reuse_external) {
			this.reuse_external = reuse_external;
		}

		public Boolean getBlockdev() {
			return blockdev;
		}

		public void setBlockdev(Boolean blockdev) {
			this.blockdev = blockdev;
		}

		public Boolean getPivot() {
			return pivot;
		}

		public void setPivot(Boolean pivot) {
			this.pivot = pivot;
		}

		public Boolean getFinish() {
			return finish;
		}

		public void setFinish(Boolean finish) {
			this.finish = finish;
		}

		public Boolean getTransient_job() {
			return transient_job;
		}

		public void setTransient_job(Boolean transient_job) {
			this.transient_job = transient_job;
		}
		
	}
	
}
