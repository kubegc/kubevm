/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinepool;

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
@ClassDescriber(value = "VirtualMachinePool", desc = "扩展支持各种存储后端")
public class Lifecycle {
	
	@FunctionDescriber(shortName = "开机启动存储池", description = "开机启动存储池，否则开机该存储池会连接不上，导致不可用。适用libvirt指令创建存储池情况。" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected AutoStartPool autoStartPool;
	
	@FunctionDescriber(shortName = "创建存储池", description = "创建存储池，适用libvirt指令创建存储池情况。" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreatePool createPool;
	
	@FunctionDescriber(shortName = "启动存储池", description = "启动存储池，如果存储池处于Inactive状态，可以启动。适用libvirt指令创建存储池情况。" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected StartPool startPool;
	
//	@FunctionDescriber(shortName = "注册存储池", description = "注册存储池，将挂载的存储信息注册到Libvirt中，适用与采用外部存储池情况，与CreatePool等价"
//			+ AnnotationUtils.DESC_FUNCTION_DESC,
//		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP,
//		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
//	protected RegisterPool registerPool;
	
	@FunctionDescriber(shortName = "停止存储池", description = "停止存储池，将存储池状态设置为Inactive，适用libvirt指令创建存储池情况。" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected StopPool stopPool;
	
	@FunctionDescriber(shortName = "删除存储池", description = "删除存储池，适用libvirt指令创建存储池情况。" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeletePool deletePool;

	@FunctionDescriber(shortName = "查询存储池", description = "调用本接口后会同步存储池的当前状态并注册到k8s，再使用GetVMPool接口获得当前存储池状态，适用libvirt指令创建存储池情况。"
			+ AnnotationUtils.DESC_FUNCTION_DESC,
			prerequisite = AnnotationUtils.DESC_FUNCTION_VMP,
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ShowPool showPool;

	@FunctionDescriber(shortName = "恢复虚拟机", description = "恢复虚拟机，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected RestoreVMBackup restoreVMBackup;

	@FunctionDescriber(shortName = "删除远程备份", description = "删除远程备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteRemoteBackup deleteRemoteBackup;

	@FunctionDescriber(shortName = "拉取远程备份", description = "拉取远程备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PullRemoteBackup pullRemoteBackup;

	@FunctionDescriber(shortName = "上传备份", description = "上传备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PushRemoteBackup pushRemoteBackup;

	@FunctionDescriber(shortName = "删除本地备份", description = "删除本地备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteVMBackup deleteVMBackup;

	@FunctionDescriber(shortName = "清理本地备份", description = "清理本地备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CleanVMBackup cleanVMBackup;

	@FunctionDescriber(shortName = "清理远端备份", description = "清理远端备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CleanVMRemoteBackup cleanVMRemoteBackup;

	@FunctionDescriber(shortName = "扫描本地备份", description = "扫描本地备份，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ScanVMBackup scanVMBackup;

	@FunctionDescriber(shortName = "恢复云盘", description = "从备份恢复云盘，"
			+ AnnotationUtils.DESC_FUNCTION_DESC,
			prerequisite = AnnotationUtils.DESC_FUNCTION_VMD,
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected RestoreDisk restoreDisk;

	@FunctionDescriber(shortName = "删除本地云盘", description = "删除本地云盘，"
			+ AnnotationUtils.DESC_FUNCTION_DESC,
			prerequisite = AnnotationUtils.DESC_FUNCTION_VMD,
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected DeleteVMDiskBackup deleteVMDiskBackup;

	@FunctionDescriber(shortName = "删除远程ftp备份服务器", description = "删除远程ftp备份服务器，"
			+ AnnotationUtils.DESC_FUNCTION_DESC,
			prerequisite = AnnotationUtils.DESC_FUNCTION_VMD,
			exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected DeleteRemoteBackupServer deleteRemoteBackupServer;
	
//	@FunctionDescriber(shortName = "反注册存储池", description = "反注册存储池，将存储池信息从libvirt里面注销"
//			+ AnnotationUtils.DESC_FUNCTION_DESC,
//		prerequisite = AnnotationUtils.DESC_FUNCTION_VMP,
//		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
//	protected UnregisterPool unregisterPool;


	public DeleteRemoteBackupServer getDeleteRemoteBackupServer() {
		return deleteRemoteBackupServer;
	}

	public void setDeleteRemoteBackupServer(DeleteRemoteBackupServer deleteRemoteBackupServer) {
		this.deleteRemoteBackupServer = deleteRemoteBackupServer;
	}

	public RestoreDisk getRestoreDisk() {
		return restoreDisk;
	}

	public void setRestoreDisk(RestoreDisk restoreDisk) {
		this.restoreDisk = restoreDisk;
	}

	public DeleteVMDiskBackup getDeleteVMDiskBackup() {
		return deleteVMDiskBackup;
	}

	public void setDeleteVMDiskBackup(DeleteVMDiskBackup deleteVMDiskBackup) {
		this.deleteVMDiskBackup = deleteVMDiskBackup;
	}

	public RestoreVMBackup getRestoreVMBackup() {
		return restoreVMBackup;
	}

	public void setRestoreVMBackup(RestoreVMBackup restoreVMBackup) {
		this.restoreVMBackup = restoreVMBackup;
	}

	public DeleteRemoteBackup getDeleteRemoteBackup() {
		return deleteRemoteBackup;
	}

	public void setDeleteRemoteBackup(DeleteRemoteBackup deleteRemoteBackup) {
		this.deleteRemoteBackup = deleteRemoteBackup;
	}

	public PullRemoteBackup getPullRemoteBackup() {
		return pullRemoteBackup;
	}

	public void setPullRemoteBackup(PullRemoteBackup pullRemoteBackup) {
		this.pullRemoteBackup = pullRemoteBackup;
	}

	public PushRemoteBackup getPushRemoteBackup() {
		return pushRemoteBackup;
	}

	public void setPushRemoteBackup(PushRemoteBackup pushRemoteBackup) {
		this.pushRemoteBackup = pushRemoteBackup;
	}

	public DeleteVMBackup getDeleteVMBackup() {
		return deleteVMBackup;
	}

	public void setDeleteVMBackup(DeleteVMBackup deleteVMBackup) {
		this.deleteVMBackup = deleteVMBackup;
	}

	public CleanVMBackup getCleanVMBackup() {
		return cleanVMBackup;
	}

	public void setCleanVMBackup(CleanVMBackup cleanVMBackup) {
		this.cleanVMBackup = cleanVMBackup;
	}

	public CleanVMRemoteBackup getCleanVMRemoteBackup() {
		return cleanVMRemoteBackup;
	}

	public void setCleanVMRemoteBackup(CleanVMRemoteBackup cleanVMRemoteBackup) {
		this.cleanVMRemoteBackup = cleanVMRemoteBackup;
	}

	public ScanVMBackup getScanVMBackup() {
		return scanVMBackup;
	}

	public void setScanVMBackup(ScanVMBackup scanVMBackup) {
		this.scanVMBackup = scanVMBackup;
	}

	public AutoStartPool getAutoStartPool() {
		return autoStartPool;
	}

	public void setAutoStartPool(AutoStartPool autoStartPool) {
		this.autoStartPool = autoStartPool;
	}

	public CreatePool getCreatePool() {
		return createPool;
	}

	public void setCreatePool(CreatePool createPool) {
		this.createPool = createPool;
	}

	public StartPool getStartPool() {
		return startPool;
	}

	public void setStartPool(StartPool startPool) {
		this.startPool = startPool;
	}

//	public RegisterPool getRegisterPool() {
//		return registerPool;
//	}
//
//	public void setRegisterPool(RegisterPool registerPool) {
//		this.registerPool = registerPool;
//	}

	public StopPool getStopPool() {
		return stopPool;
	}

	public void setStopPool(StopPool stopPool) {
		this.stopPool = stopPool;
	}

	public DeletePool getDeletePool() {
		return deletePool;
	}

	public void setDeletePool(DeletePool deletePool) {
		this.deletePool = deletePool;
	}

	public ShowPool getShowPool() {
		return showPool;
	}

	public void setShowPool(ShowPool showPool) {
		this.showPool = showPool;
	}

	//	public UnregisterPool getUnregisterPool() {
//		return unregisterPool;
//	}
//
//	public void setUnregisterPool(UnregisterPool unregisterPool) {
//		this.unregisterPool = unregisterPool;
//	}
	
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class AutoStartPool {

		@ParameterDescriber(required = false, description = "存储池的类型", constraint = "只能是localfs，vdiskfs, nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
	    protected String type;

		@ParameterDescriber(required = true, description = "修改存储池autostart状态", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean disable;

		public Boolean getDisable() {
			return disable;
		}

		public void setDisable(Boolean disable) {
			this.disable = disable;
		}

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }
    }

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreatePool {

		@ParameterDescriber(required = true, description = "存储池的类型", constraint = "只能是localfs，uus，nfs，glusterfs, vdiskfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_PATTERN)
		protected String type;
		
		@ParameterDescriber(required = true, description = "存储池的内容，用于标识存储池的用途", constraint = "只能是vmd，vmdi，iso之一", example = "vmd")
		@Pattern(regexp = RegExpUtils.POOL_CONTENT_PATTERN)
		protected String content;
		
		protected String source_host;
		
		protected String source_path;

		@ParameterDescriber(required = true, description = "创建云存储池时的url", constraint = "建立云存储池时通过cstor-cli pool-list查询出的云存储池路径", example = "uus-iscsi-independent://admin:admin@192.168.3.10:7000/p1/4/2/0/32/0/3")
		@Pattern(regexp = RegExpUtils.POOL_URL_PATTERN)
		protected String url;

		@ParameterDescriber(required = false, description = "nfs、gfs挂载参数或uus的创建选项，为存储类型为uus和nfs、gfs时必填，本地存储和vdiskfs不填", constraint = "当type为nfs、gfs类型时，作为挂载参数", example = "nolock")
		protected String opt;

		@ParameterDescriber(required = true, description = "cstor存储池的名字，与挂载路径有关", constraint = "对所有类型必填，由数字和字母组成", example = "07098ca5fd174fccafed76b0d7fccde4")
		@Pattern(regexp = RegExpUtils.POOL_UUID)
		protected String uuid;

		protected String source_dev;
		
		protected String source_name;

		@ParameterDescriber(required = false, description = "创建存储池后是否设置为自动打开", constraint = "true或false", example = "true")
		protected boolean autostart;

//		@ParameterDescriber(required = false, description = "创建nfs或glusterfs存储池时的挂载路径，不填则默认在/var/lib/libvirt/cstor目录下挂载", constraint = "/nfs/pool", example = "/nfs/pool")
//		@Pattern(regexp = RegExpUtils.POOL_PATH)
//		protected String path;

		@ParameterDescriber(required = false, description = "强力创建vdiskfs", constraint = "True或False", example = "True")
		@Pattern(regexp = RegExpUtils.BOOL_TYPE_PATTERN)
		protected String force;

//		@ParameterDescriber(required = true, description = "创建存储池使用的存储路径", constraint = "完整有效的存储路径", example = "/var/lib/libvirt/poolg")
//		@Pattern(regexp = RegExpUtils.TARGET_PATTERN)
//		protected String target;
		
		protected String source_format;
		
		protected String auth_type;
		
		protected String auth_username;
		
		protected String secret_usage;
		
		protected String secret_uuid;
		
		protected String adapter_name;
		
		protected String adapter_wwnn;
		
		protected String adapter_wwpn;
		
		protected String adapter_parent;
		
		protected String adapter_parent_wwnn;
		
		protected String adapter_parent_wwpn;
		
		protected String adapter_parent_fabric_wwn;
		
		protected Boolean build;
		
		protected Boolean no_overwrite;
		
		protected Boolean overwrite;

		public String getUuid() {
			return uuid;
		}

		public void setUuid(String uuid) {
			this.uuid = uuid;
		}


//		public String getPath() {
//			return path;
//		}
//
//		public void setPath(String path) {
//			this.path = path;
//		}

		public String getForce() {
			return force;
		}

		public void setForce(String force) {
			this.force = force;
		}

		public String getContent() {
			return content;
		}

		public void setContent(String content) {
			this.content = content;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getSource_host() {
			return source_host;
		}

		public void setSource_host(String source_host) {
			this.source_host = source_host;
		}

		public String getSource_path() {
			return source_path;
		}

		public void setSource_path(String source_path) {
			this.source_path = source_path;
		}

		public String getSource_dev() {
			return source_dev;
		}

		public void setSource_dev(String source_dev) {
			this.source_dev = source_dev;
		}

		public String getSource_name() {
			return source_name;
		}

		public void setSource_name(String source_name) {
			this.source_name = source_name;
		}

//		public String getTarget() {
//			return target;
//		}
//
//		public void setTarget(String target) {
//			this.target = target;
//		}

		public String getSource_format() {
			return source_format;
		}

		public void setSource_format(String source_format) {
			this.source_format = source_format;
		}

		public String getAuth_type() {
			return auth_type;
		}

		public void setAuth_type(String auth_type) {
			this.auth_type = auth_type;
		}

		public String getAuth_username() {
			return auth_username;
		}

		public void setAuth_username(String auth_username) {
			this.auth_username = auth_username;
		}

		public String getSecret_usage() {
			return secret_usage;
		}

		public void setSecret_usage(String secret_usage) {
			this.secret_usage = secret_usage;
		}

		public String getSecret_uuid() {
			return secret_uuid;
		}

		public void setSecret_uuid(String secret_uuid) {
			this.secret_uuid = secret_uuid;
		}

		public String getAdapter_name() {
			return adapter_name;
		}

		public void setAdapter_name(String adapter_name) {
			this.adapter_name = adapter_name;
		}

		public String getAdapter_wwnn() {
			return adapter_wwnn;
		}

		public void setAdapter_wwnn(String adapter_wwnn) {
			this.adapter_wwnn = adapter_wwnn;
		}

		public String getAdapter_wwpn() {
			return adapter_wwpn;
		}

		public void setAdapter_wwpn(String adapter_wwpn) {
			this.adapter_wwpn = adapter_wwpn;
		}

		public String getAdapter_parent() {
			return adapter_parent;
		}

		public void setAdapter_parent(String adapter_parent) {
			this.adapter_parent = adapter_parent;
		}

		public String getAdapter_parent_wwnn() {
			return adapter_parent_wwnn;
		}

		public void setAdapter_parent_wwnn(String adapter_parent_wwnn) {
			this.adapter_parent_wwnn = adapter_parent_wwnn;
		}

		public String getAdapter_parent_wwpn() {
			return adapter_parent_wwpn;
		}

		public void setAdapter_parent_wwpn(String adapter_parent_wwpn) {
			this.adapter_parent_wwpn = adapter_parent_wwpn;
		}

		public String getAdapter_parent_fabric_wwn() {
			return adapter_parent_fabric_wwn;
		}

		public void setAdapter_parent_fabric_wwn(String adapter_parent_fabric_wwn) {
			this.adapter_parent_fabric_wwn = adapter_parent_fabric_wwn;
		}

		public Boolean getBuild() {
			return build;
		}

		public void setBuild(Boolean build) {
			this.build = build;
		}

		public Boolean getNo_overwrite() {
			return no_overwrite;
		}

		public void setNo_overwrite(Boolean no_overwrite) {
			this.no_overwrite = no_overwrite;
		}

		public Boolean getOverwrite() {
			return overwrite;
		}

		public void setOverwrite(Boolean overwrite) {
			this.overwrite = overwrite;
		}

		public String getUrl() {
			return url;
		}

		public void setUrl(String url) {
			this.url = url;
		}

		public String getOpt() {
			return opt;
		}

		public void setOpt(String opt) {
			this.opt = opt;
		}

		public boolean getAutostart() {
			return autostart;
		}

		public void setAutostart(boolean autostart) {
			this.autostart = autostart;
		}
	}
	
//	@JsonInclude(JsonInclude.Include.NON_NULL)
//	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
//	public static class RegisterPool {
//
//		protected String type;
//
//		protected String source_host;
//
//		protected String source_path;
//
//		protected String source_dev;
//
//		protected String source_name;
//
//		protected String target;
//
//		protected String source_format;
//
//		protected String auth_type;
//
//		protected String auth_username;
//
//		protected String secret_usage;
//
//		protected String secret_uuid;
//
//		protected String adapter_name;
//
//		protected String adapter_wwnn;
//
//		protected String adapter_wwpn;
//
//		protected String adapter_parent;
//
//		protected String adapter_parent_wwnn;
//
//		protected String adapter_parent_wwpn;
//
//		protected String adapter_parent_fabric_wwn;
//
//		public String getType() {
//			return type;
//		}
//
//		public void setType(String type) {
//			this.type = type;
//		}
//
//		public String getSource_host() {
//			return source_host;
//		}
//
//		public void setSource_host(String source_host) {
//			this.source_host = source_host;
//		}
//
//		public String getSource_path() {
//			return source_path;
//		}
//
//		public void setSource_path(String source_path) {
//			this.source_path = source_path;
//		}
//
//		public String getSource_dev() {
//			return source_dev;
//		}
//
//		public void setSource_dev(String source_dev) {
//			this.source_dev = source_dev;
//		}
//
//		public String getSource_name() {
//			return source_name;
//		}
//
//		public void setSource_name(String source_name) {
//			this.source_name = source_name;
//		}
//
//		public String getTarget() {
//			return target;
//		}
//
//		public void setTarget(String target) {
//			this.target = target;
//		}
//
//		public String getSource_format() {
//			return source_format;
//		}
//
//		public void setSource_format(String source_format) {
//			this.source_format = source_format;
//		}
//
//		public String getAuth_type() {
//			return auth_type;
//		}
//
//		public void setAuth_type(String auth_type) {
//			this.auth_type = auth_type;
//		}
//
//		public String getAuth_username() {
//			return auth_username;
//		}
//
//		public void setAuth_username(String auth_username) {
//			this.auth_username = auth_username;
//		}
//
//		public String getSecret_usage() {
//			return secret_usage;
//		}
//
//		public void setSecret_usage(String secret_usage) {
//			this.secret_usage = secret_usage;
//		}
//
//		public String getSecret_uuid() {
//			return secret_uuid;
//		}
//
//		public void setSecret_uuid(String secret_uuid) {
//			this.secret_uuid = secret_uuid;
//		}
//
//		public String getAdapter_name() {
//			return adapter_name;
//		}
//
//		public void setAdapter_name(String adapter_name) {
//			this.adapter_name = adapter_name;
//		}
//
//		public String getAdapter_wwnn() {
//			return adapter_wwnn;
//		}
//
//		public void setAdapter_wwnn(String adapter_wwnn) {
//			this.adapter_wwnn = adapter_wwnn;
//		}
//
//		public String getAdapter_wwpn() {
//			return adapter_wwpn;
//		}
//
//		public void setAdapter_wwpn(String adapter_wwpn) {
//			this.adapter_wwpn = adapter_wwpn;
//		}
//
//		public String getAdapter_parent() {
//			return adapter_parent;
//		}
//
//		public void setAdapter_parent(String adapter_parent) {
//			this.adapter_parent = adapter_parent;
//		}
//
//		public String getAdapter_parent_wwnn() {
//			return adapter_parent_wwnn;
//		}
//
//		public void setAdapter_parent_wwnn(String adapter_parent_wwnn) {
//			this.adapter_parent_wwnn = adapter_parent_wwnn;
//		}
//
//		public String getAdapter_parent_wwpn() {
//			return adapter_parent_wwpn;
//		}
//
//		public void setAdapter_parent_wwpn(String adapter_parent_wwpn) {
//			this.adapter_parent_wwpn = adapter_parent_wwpn;
//		}
//
//		public String getAdapter_parent_fabric_wwn() {
//			return adapter_parent_fabric_wwn;
//		}
//
//		public void setAdapter_parent_fabric_wwn(String adapter_parent_fabric_wwn) {
//			this.adapter_parent_fabric_wwn = adapter_parent_fabric_wwn;
//		}
//
//
//	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class StartPool {
		@ParameterDescriber(required = false, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
        protected String type;
		
		protected Boolean build;
		
		protected Boolean no_overwrite;
		
		protected Boolean overwrite;

		public Boolean getBuild() {
			return build;
		}

		public void setBuild(Boolean build) {
			this.build = build;
		}

		public Boolean getNo_overwrite() {
			return no_overwrite;
		}

		public void setNo_overwrite(Boolean no_overwrite) {
			this.no_overwrite = no_overwrite;
		}

		public Boolean getOverwrite() {
			return overwrite;
		}

		public void setOverwrite(Boolean overwrite) {
			this.overwrite = overwrite;
		}

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }
    }
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class StopPool {
		@ParameterDescriber(required = false, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，nfs，glusterfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_NOT_SUPPORT_UUS)
        protected String type;

        public String getType() {
            return type;
        }

        public void setType(String type) {
            this.type = type;
        }
    }
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeletePool {
		@ParameterDescriber(required = false, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，uus，nfs，glusterfs, vdiskfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_PATTERN)
		protected String type;

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ShowPool {
		@ParameterDescriber(required = false, description = "存储池的类型", constraint = "只能是localfs，vdiskfs，uus，nfs，glusterfs, vdiskfs之一", example = "localfs")
		@Pattern(regexp = RegExpUtils.POOL_TYPE_PATTERN)
		protected String type;

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}
	}
	
//	@JsonInclude(JsonInclude.Include.NON_NULL)
//	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
//	public static class UnregisterPool {
//
//	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RestoreVMBackup {

		@ParameterDescriber(required = true, description = "备份时使用云主机", constraint = "备份时使用云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "备份主机使用的存储池", constraint = "备份主机使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		@ParameterDescriber(required = false, description = "备份虚拟机所有的盘，否则只备份系统盘，需要注意的是恢复带有数据云盘的记录时，数据云盘必须还挂载在该虚拟机上",
				constraint = "备份虚拟机所有的盘，否则只备份系统盘，需要注意的是恢复带有数据云盘的记录时，数据云盘必须还挂载在该虚拟机上", example = "true")
		protected boolean all;

		@ParameterDescriber(required = false, description = "新建虚拟机的名字", constraint = "新建虚拟机的名字", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String newname;

		@ParameterDescriber(required = false, description = "新建虚拟机时所使用的存储池", constraint = "新建虚拟机所使用的存储池", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String target;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public boolean getAll() {
			return all;
		}

		public void setAll(boolean all) {
			this.all = all;
		}

		public String getNewname() {
			return newname;
		}

		public void setNewname(String newname) {
			this.newname = newname;
		}

		public String getTarget() {
			return target;
		}

		public void setTarget(String target) {
			this.target = target;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteVMBackup {

		@ParameterDescriber(required = true, description = "要删除备份记录所在的云主机", constraint = "要删除备份记录所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "备份主机使用的存储池", constraint = "备份主机使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteRemoteBackup {

		@ParameterDescriber(required = true, description = "要清理云主机或云盘的远程备份所在的云主机", constraint = "要清理云主机或云盘的远程备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = false, description = "仅删除该云主机的云盘备份", constraint = "仅删除该云主机的云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		@ParameterDescriber(required = false, description = "远程备份的ftp主机ip", constraint = "远程备份的ftp主机ip", example = "172.16.1.214")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String remote;

		@ParameterDescriber(required = false, description = "远程备份的ftp主机端口", constraint = "远程备份的ftp主机端口", example = "21")
		@Pattern(regexp = RegExpUtils.PORT_PATTERN)
		protected String port;

		@ParameterDescriber(required = false, description = "远程备份的ftp用户名", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String username;

		@ParameterDescriber(required = false, description = "远程备份的ftp密码", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public String getRemote() {
			return remote;
		}

		public void setRemote(String remote) {
			this.remote = remote;
		}

		public String getPort() {
			return port;
		}

		public void setPort(String port) {
			this.port = port;
		}

		public String getUsername() {
			return username;
		}

		public void setUsername(String username) {
			this.username = username;
		}

		public String getPassword() {
			return password;
		}

		public void setPassword(String password) {
			this.password = password;
		}
	}


	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class PullRemoteBackup {

		@ParameterDescriber(required = true, description = "要拉取云盘或云主机的远程备份所在的云主机", constraint = "要拉取云盘或云主机的远程备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "拉取备份后使用的存储池", constraint = "拉取备份后使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = false, description = "仅拉取该云主机的云盘备份", constraint = "仅拉取云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机ip", constraint = "远程备份的ftp主机ip", example = "172.16.1.214")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String remote;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机端口", constraint = "远程备份的ftp主机端口", example = "21")
		@Pattern(regexp = RegExpUtils.PORT_PATTERN)
		protected String port;

		@ParameterDescriber(required = true, description = "远程备份的ftp用户名", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String username;

		@ParameterDescriber(required = true, description = "远程备份的ftp密码", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
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

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public String getRemote() {
			return remote;
		}

		public void setRemote(String remote) {
			this.remote = remote;
		}

		public String getPort() {
			return port;
		}

		public void setPort(String port) {
			this.port = port;
		}

		public String getUsername() {
			return username;
		}

		public void setUsername(String username) {
			this.username = username;
		}

		public String getPassword() {
			return password;
		}

		public void setPassword(String password) {
			this.password = password;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class PushRemoteBackup {

		@ParameterDescriber(required = true, description = "要推送的云主机或云盘备份所在的云主机", constraint = "要推送的云主机或云盘备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "备份使用的存储池", constraint = "备份使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = false, description = "仅上传该云主机的云盘备份", constraint = "仅上传该云主机的云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机ip", constraint = "远程备份的ftp主机ip", example = "172.16.1.214")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String remote;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机端口", constraint = "远程备份的ftp主机端口", example = "21")
		@Pattern(regexp = RegExpUtils.PORT_PATTERN)
		protected String port;

		@ParameterDescriber(required = true, description = "远程备份的ftp用户名", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String username;

		@ParameterDescriber(required = true, description = "远程备份的ftp密码", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
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

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public String getRemote() {
			return remote;
		}

		public void setRemote(String remote) {
			this.remote = remote;
		}

		public String getPort() {
			return port;
		}

		public void setPort(String port) {
			this.port = port;
		}

		public String getUsername() {
			return username;
		}

		public void setUsername(String username) {
			this.username = username;
		}

		public String getPassword() {
			return password;
		}

		public void setPassword(String password) {
			this.password = password;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CleanVMBackup {

		@ParameterDescriber(required = true, description = "要清理云盘或云主机备份所在的云主机", constraint = "要清理云盘或云主机备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "云主机备份时使用的存储池", constraint = "云主机备份时使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = false, description = "仅清除该云主机的云盘备份", constraint = "仅清除该云主机的云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = false, description = "备份记录的版本号，多个版本号以逗号隔开", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		protected String version;

		@ParameterDescriber(required = false, description = "清除云主机或云盘所有备份", constraint = "清除云主机或云盘所有备份", example = "13024b305b5c463b80bceee066077079")
		protected boolean all;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public boolean getAll() {
			return all;
		}

		public void setAll(boolean all) {
			this.all = all;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
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
	public static class CleanVMRemoteBackup {

		@ParameterDescriber(required = true, description = "要清理云盘的远程备份所在的云主机", constraint = "要清理云盘的远程备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = false, description = "仅清除该云主机的云盘备份", constraint = "仅清除该云主机的云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = false, description = "备份记录的版本号，多个版本号以逗号隔开", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		protected String version;

		@ParameterDescriber(required = false, description = "清除云主机或云盘所有备份", constraint = "清除云主机或云盘所有备份", example = "13024b305b5c463b80bceee066077079")
		protected boolean all;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机ip", constraint = "远程备份的ftp主机ip", example = "172.16.1.214")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String remote;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机端口", constraint = "远程备份的ftp主机端口", example = "21")
		@Pattern(regexp = RegExpUtils.PORT_PATTERN)
		protected String port;

		@ParameterDescriber(required = true, description = "远程备份的ftp用户名", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String username;

		@ParameterDescriber(required = true, description = "远程备份的ftp密码", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}

		public String getRemote() {
			return remote;
		}

		public void setRemote(String remote) {
			this.remote = remote;
		}

		public String getPort() {
			return port;
		}

		public void setPort(String port) {
			this.port = port;
		}

		public String getUsername() {
			return username;
		}

		public void setUsername(String username) {
			this.username = username;
		}

		public String getPassword() {
			return password;
		}

		public void setPassword(String password) {
			this.password = password;
		}

		public boolean getAll() {
			return all;
		}

		public void setAll(boolean all) {
			this.all = all;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ScanVMBackup {

		@ParameterDescriber(required = true, description = "要扫描云盘的备份所在的云主机", constraint = "要扫描云盘的备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "云主机备份时使用的存储池", constraint = "云主机备份时使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = false, description = "仅扫描该云主机的云盘备份", constraint = "仅扫描该云主机的云盘备份", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

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

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RestoreDisk {
		@ParameterDescriber(required = true, description = "要恢复的云盘备份记录所在的云主机", constraint = "要恢复的云盘备份记录所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		protected String domain;

		@ParameterDescriber(required = true, description = "云盘备份所在的存储池", constraint = "云盘备份所在的存储池", example = "172.16.1.214")
		protected String pool;

		@ParameterDescriber(required = true, description = "云主机的云盘备份所使用的的云盘id", constraint = "云主机的云盘备份所使用的的云盘id", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "172.16.1.214")
		protected String version;

		@ParameterDescriber(required = false, description = "新建云盘的名字", constraint = "新建云盘的名字", example = "a63dd73f92a24a9ab840492f0e538f2b")
		protected String newname;

		@ParameterDescriber(required = false, description = "根据备份记录新建云盘时使用的存储池", constraint = "根据备份记录新建云盘时使用的存储池", example = "pooltest")
		protected String target;

		@ParameterDescriber(required = false, description = "新建云盘要挂载到的虚拟机", constraint = "新建云盘要挂载到的虚拟机", example = "172.16.1.214")
		protected String targetDomain;

		public String getVol() {
			return vol;
		}

		public void setVol(String vol) {
			this.vol = vol;
		}

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getPool() {
			return pool;
		}

		public void setPool(String pool) {
			this.pool = pool;
		}

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}

		public String getNewname() {
			return newname;
		}

		public void setNewname(String newname) {
			this.newname = newname;
		}

		public String getTarget() {
			return target;
		}

		public void setTarget(String target) {
			this.target = target;
		}

		public String getTargetDomain() {
			return targetDomain;
		}

		public void setTargetDomain(String targetDomain) {
			this.targetDomain = targetDomain;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteVMDiskBackup {
		@ParameterDescriber(required = true, description = "要删除云盘的备份所在的云主机", constraint = "要删除云盘的备份所在的云主机", example = "a63dd73f92a24a9ab840492f0e538f2b")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;

		@ParameterDescriber(required = true, description = "备份主机云盘使用的存储池", constraint = "备份主机云盘使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "云盘id", constraint = "云盘id", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String vol;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
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

		public String getVersion() {
			return version;
		}

		public void setVersion(String version) {
			this.version = version;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteRemoteBackupServer {
		@ParameterDescriber(required = true, description = "远程备份的ftp主机ip", constraint = "远程备份的ftp主机ip", example = "172.16.1.214")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String remote;

		@ParameterDescriber(required = true, description = "远程备份的ftp主机端口", constraint = "远程备份的ftp主机端口", example = "21")
		@Pattern(regexp = RegExpUtils.PORT_PATTERN)
		protected String port;

		@ParameterDescriber(required = true, description = "远程备份的ftp用户名", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String username;

		@ParameterDescriber(required = true, description = "远程备份的ftp密码", constraint = "ftpuser", example = "ftpuser")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getRemote() {
			return remote;
		}

		public void setRemote(String remote) {
			this.remote = remote;
		}

		public String getPort() {
			return port;
		}

		public void setPort(String port) {
			this.port = port;
		}

		public String getUsername() {
			return username;
		}

		public void setUsername(String username) {
			this.username = username;
		}

		public String getPassword() {
			return password;
		}

		public void setPassword(String password) {
			this.password = password;
		}

	}
}
