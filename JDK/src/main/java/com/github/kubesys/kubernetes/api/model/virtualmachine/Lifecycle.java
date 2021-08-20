/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachine;

import java.util.List;

import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.annotations.ClassDescriber;
import com.github.kubesys.kubernetes.annotations.FunctionDescriber;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;
import com.github.kubesys.kubernetes.utils.AnnotationUtils;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since 2019/9/4
 * 
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
@ClassDescriber(value = "VirtualMachine", desc = "虚拟机是指安装了OS的磁盘")
public class Lifecycle {

	@FunctionDescriber(shortName = "通过ISO装虚拟机", description = "通过光驱安装云OS，光驱必须存在"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = "", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateAndStartVMFromISO createAndStartVMFromISO;

	@FunctionDescriber(shortName = "通过镜像复制虚拟机", description = "通过虚拟机镜像VirtualMachineImage创建云OS"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = "", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateAndStartVMFromImage createAndStartVMFromImage;

	@FunctionDescriber(shortName = "暂停虚机", description = "对运行的虚拟机进行暂停操作，已经暂停虚拟机执行暂停会报错"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected SuspendVM suspendVM;

	@FunctionDescriber(shortName = "强制关机", description = "强制关闭虚拟机，虚拟机在某些情况下无法关闭，本质相当于拔掉电源"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected StopVMForce stopVMForce;

	@FunctionDescriber(shortName = "卸载设备", description = "卸载GPU、云盘、网卡等资源，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UnplugDevice unplugDevice;

	@FunctionDescriber(shortName = "卸载网卡", description = "卸载网卡，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UnplugNIC unplugNIC;

	@FunctionDescriber(shortName = "虚机迁移", description = "虚拟机迁移，必须依赖共享存储，且所有物理机之间免密登陆"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected MigrateVM migrateVM;

	@FunctionDescriber(shortName = "虚机存储迁移", description = "虚拟机存储迁移，只支持冷迁，迁移之前虚拟机需要关机"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected MigrateVMDisk migrateVMDisk;

	@FunctionDescriber(shortName = "CPU设置", description = "修改虚拟机CPU个数"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ChangeNumberOfCPU changeNumberOfCPU;

	@FunctionDescriber(shortName = "恢复虚机", description = "恢复暂停的虚拟机，对运行的虚拟机执行恢复会报错"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ResumeVM resumeVM;

	@FunctionDescriber(shortName = "添加云盘", description = "添加云盘，云盘必须通过CreateVirtualMachineDisk预先创建好"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ ",或CreateVirtualMachineDisk", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PlugDisk plugDisk;

	@FunctionDescriber(shortName = "添加设备", description = "添加GPU、云盘、网卡等，这种方法相对于pluginDisk等可设置高级选项，如QoS"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PlugDevice plugDevice;

	@FunctionDescriber(shortName = "强制重启", description = "强制重置虚拟机，即强制重启虚拟机"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ResetVM resetVM;

	@FunctionDescriber(shortName = "卸载云盘", description = "卸载虚拟机云盘"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ ",或CreateVirtualMachineDisk", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UnplugDisk unplugDisk;

	@FunctionDescriber(shortName = "虚机关机", description = "关闭虚拟机，但不一定能关闭，如虚拟机中OS受损，对关闭虚拟机再执行关闭会报错"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected StopVM stopVM;

	@FunctionDescriber(shortName = "启动虚机", description = "启动虚拟机，能否正常启动取决于虚拟机OS是否受损，对运行虚拟机执行启动会报错"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected StartVM startVM;

	@FunctionDescriber(shortName = "删除虚机", description = "删除虚拟机，需要先关闭虚拟机"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ "或StopVM，或StopVMForce", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteVM deleteVM;

	@FunctionDescriber(shortName = "虚机重启", description = "重启虚拟机，能否正常重新启动取决于虚拟机OS是否受损"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected RebootVM rebootVM;

	@FunctionDescriber(shortName = "添加网卡", description = "给虚拟机添加网卡"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PlugNIC plugNIC;

	@FunctionDescriber(shortName = "插拔光驱", description = "插入或者拔出光驱"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ "或plugDevice", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ManageISO manageISO;

	@FunctionDescriber(shortName = "更换OS", description = "更换云主机的OS，云主机必须关机"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UpdateOS updateOS;

	@FunctionDescriber(shortName = "转化模板", description = "转化为虚拟机镜像"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected ConvertVMToImage convertVMToImage;

	@FunctionDescriber(shortName = "插入光驱", description = "插入"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ "或plugDevice", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected InsertISO insertISO;

	@FunctionDescriber(shortName = "拔出光驱", description = "拔出光驱"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM
					+ "或plugDevice", exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected EjectISO ejectISO;

	@FunctionDescriber(shortName = "调整磁盘", description = "调整虚拟机大小，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ResizeVM resizeVM;

	@FunctionDescriber(shortName = "克隆虚机", description = "克隆虚拟机，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CloneVM cloneVM;

	@FunctionDescriber(shortName = "磁盘QoS", description = "设置虚拟机磁盘QoS，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected TuneDiskQoS tuneDiskQoS;

	@FunctionDescriber(shortName = "网卡QoS", description = "设置虚拟机网卡QoS，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected TuneNICQoS tuneNICQoS;

	@FunctionDescriber(shortName = "设置虚拟机最大内存", description = "设置虚拟机最大内存，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ResizeMaxRAM resizeMaxRAM;

	@FunctionDescriber(shortName = "启动顺序", description = "设置虚拟机启动顺序，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected SetBootOrder setBootOrder;

	@FunctionDescriber(shortName = "设置VNC密码", description = "设置虚拟机VNC密码，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected SetVncPassword setVncPassword;

	@FunctionDescriber(shortName = "取消VNC密码", description = "取消虚拟机VNC密码，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected UnsetVncPassword unsetVncPassword;

	@FunctionDescriber(shortName = "虚机密码", description = "设置虚拟机密码，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected SetGuestPassword setGuestPassword;

	@FunctionDescriber(shortName = "虚机ssh key", description = "注入虚拟机ssh key，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected InjectSshKey injectSshKey;

	@FunctionDescriber(shortName = "内存扩容", description = "对虚拟机内存扩容，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ResizeRAM resizeRAM;

	@FunctionDescriber(shortName = "绑定浮动IP", description = "适用浮动和虚拟IP场景，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected BindFloatingIP bindFloatingIP;

	@FunctionDescriber(shortName = "解绑浮动IP", description = "适用浮动和虚拟IP场景，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UnbindFloatingIP unbindFloatingIP;

	@FunctionDescriber(shortName = "创建安全组", description = "创建安全规则，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected AddACL addACL;

	@FunctionDescriber(shortName = "修改安全组", description = "修改安全规则，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ModifyACL modifyACL;

	@FunctionDescriber(shortName = "删除安全组", description = "删除安全规则，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeprecatedACL deprecatedACL;
	
	@FunctionDescriber(shortName = "批量删除安全组", description = "删除安全规则，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected BatchDeprecatedACL batchDeprecatedACL;

	@FunctionDescriber(shortName = "设置QoS", description = "设置QoS，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected SetQoS setQoS;

	@FunctionDescriber(shortName = "修改QoS", description = "修改QoS，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ModifyQoS modifyQoS;

	@FunctionDescriber(shortName = "删除QoS", description = "删除QoS，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UnsetQoS unsetQoS;

	@FunctionDescriber(shortName = "导出虚拟机", description = "导出虚拟机，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ExportVM exportVM;

	@FunctionDescriber(shortName = "备份虚拟机", description = "备份虚拟机，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected BackupVM backupVM;


	@FunctionDescriber(shortName = "恢复虚拟机", description = "恢复虚拟机，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected RestoreVM restoreVM;

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
	
	@FunctionDescriber(shortName = "设备透传", description = "设备透传，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected PassthroughDevice passthroughDevice;
	
	@FunctionDescriber(shortName = "usb重定向，需搭配SPICE终端使用", description = "usb重定向，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected RedirectUsb redirectUsb;
	
	@FunctionDescriber(shortName = "更新虚拟机远程终端", description = "更新虚拟机远程终端，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected UpdateGraphic updateGraphic;
	
	@FunctionDescriber(shortName = "设置虚拟机高可用，对于正在运行的虚拟机重启后生效", description = "设置虚拟机高可用，"
			+ AnnotationUtils.DESC_FUNCTION_DESC, prerequisite = AnnotationUtils.DESC_FUNCTION_VM, exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected AutoStartVM autoStartVM;

	public BatchDeprecatedACL getBatchDeprecatedACL() {
		return batchDeprecatedACL;
	}

	public void setBatchDeprecatedACL(BatchDeprecatedACL batchDeprecatedACL) {
		this.batchDeprecatedACL = batchDeprecatedACL;
	}

	public UnplugDisk getUnplugDisk() {
		return unplugDisk;
	}

	public void setUnplugDisk(UnplugDisk unplugDisk) {
		this.unplugDisk = unplugDisk;
	}

	public PushRemoteBackup getPushRemoteBackup() {
		return pushRemoteBackup;
	}

	public void setPushRemoteBackup(PushRemoteBackup pushRemoteBackup) {
		this.pushRemoteBackup = pushRemoteBackup;
	}

	public AutoStartVM getAutoStartVM() {
		return autoStartVM;
	}

	public void setAutoStartVM(AutoStartVM autoStartVM) {
		this.autoStartVM = autoStartVM;
	}

	public RedirectUsb getRedirectUsb() {
		return redirectUsb;
	}

	public void setRedirectUsb(RedirectUsb redirectUsb) {
		this.redirectUsb = redirectUsb;
	}

	public PassthroughDevice getPassthroughDevice() {
		return passthroughDevice;
	}

	public void setPassthroughDevice(PassthroughDevice passthroughDevice) {
		this.passthroughDevice = passthroughDevice;
	}

	public UpdateGraphic getUpdateGraphic() {
		return updateGraphic;
	}

	public void setUpdateGraphic(UpdateGraphic updateGraphic) {
		this.updateGraphic = updateGraphic;
	}

	public ExportVM getExportVM() {
		return exportVM;
	}

	public void setExportVM(ExportVM exportVM) {
		this.exportVM = exportVM;
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

	public DeleteVMBackup getDeleteVMBackup() {
		return deleteVMBackup;
	}

	public void setDeleteVMBackup(DeleteVMBackup deleteVMBackup) {
		this.deleteVMBackup = deleteVMBackup;
	}

	public BackupVM getBackupVM() {
		return backupVM;
	}

	public void setBackupVM(BackupVM backupVM) {
		this.backupVM = backupVM;
	}

	public RestoreVM getRestoreVM() {
		return restoreVM;
	}

	public void setRestoreVM(RestoreVM restoreVM) {
		this.restoreVM = restoreVM;
	}

	public MigrateVMDisk getMigrateVMDisk() {
		return migrateVMDisk;
	}

	public void setMigrateVMDisk(MigrateVMDisk migrateVMDisk) {
		this.migrateVMDisk = migrateVMDisk;
	}

	public SetQoS getSetQoS() {
		return setQoS;
	}

	public void setSetQoS(SetQoS setQoS) {
		this.setQoS = setQoS;
	}

	public UnsetQoS getUnsetQoS() {
		return unsetQoS;
	}

	public void setUnsetQoS(UnsetQoS unsetQoS) {
		this.unsetQoS = unsetQoS;
	}

	public ModifyQoS getModifyQoS() {
		return modifyQoS;
	}

	public void setModifyQoS(ModifyQoS modifyQoS) {
		this.modifyQoS = modifyQoS;
	}

	public BindFloatingIP getBindFloatingIP() {
		return bindFloatingIP;
	}

	public void setBindFloatingIP(BindFloatingIP bindFloatingIP) {
		this.bindFloatingIP = bindFloatingIP;
	}

	public UnbindFloatingIP getUnbindFloatingIP() {
		return unbindFloatingIP;
	}

	public void setUnbindFloatingIP(UnbindFloatingIP unbindFloatingIP) {
		this.unbindFloatingIP = unbindFloatingIP;
	}

	public AddACL getAddACL() {
		return addACL;
	}

	public void setAddACL(AddACL addACL) {
		this.addACL = addACL;
	}

	public ModifyACL getModifyACL() {
		return modifyACL;
	}

	public void setModifyACL(ModifyACL modifyACL) {
		this.modifyACL = modifyACL;
	}

	public DeprecatedACL getDeprecatedACL() {
		return deprecatedACL;
	}

	public void setDeprecatedACL(DeprecatedACL deprecatedACL) {
		this.deprecatedACL = deprecatedACL;
	}

	public SetGuestPassword getSetGuestPassword() {
		return setGuestPassword;
	}

	public void setSetGuestPassword(SetGuestPassword setGuestPassword) {
		this.setGuestPassword = setGuestPassword;
	}

	public UnsetVncPassword getUnsetVncPassword() {
		return unsetVncPassword;
	}

	public void setUnsetVncPassword(UnsetVncPassword unsetVncPassword) {
		this.unsetVncPassword = unsetVncPassword;
	}

	public TuneNICQoS getTuneNICQoS() {
		return tuneNICQoS;
	}

	public void setTuneNICQoS(TuneNICQoS tuneNICQoS) {
		this.tuneNICQoS = tuneNICQoS;
	}

	public SetBootOrder getSetBootOrder() {
		return setBootOrder;
	}

	public void setSetBootOrder(SetBootOrder setBootOrder) {
		this.setBootOrder = setBootOrder;
	}

	public SetVncPassword getSetVncPassword() {
		return setVncPassword;
	}

	public void setSetVncPassword(SetVncPassword setVncPassword) {
		this.setVncPassword = setVncPassword;
	}

	public InjectSshKey getInjectSshKey() {
		return injectSshKey;
	}

	public void setInjectSshKey(InjectSshKey injectSshKey) {
		this.injectSshKey = injectSshKey;
	}

	public ResizeMaxRAM getResizeMaxRAM() {
		return resizeMaxRAM;
	}

	public void setResizeMaxRAM(ResizeMaxRAM resizeMaxRAM) {
		this.resizeMaxRAM = resizeMaxRAM;
	}

	public TuneDiskQoS getTuneDiskQoS() {
		return tuneDiskQoS;
	}

	public void setTuneDiskQoS(TuneDiskQoS tuneDiskQoS) {
		this.tuneDiskQoS = tuneDiskQoS;
	}

	public ManageISO getManageISO() {
		return manageISO;
	}

	public void setManageISO(ManageISO manageISO) {
		this.manageISO = manageISO;
	}

	public UpdateOS getUpdateOS() {
		return updateOS;
	}

	public void setUpdateOS(UpdateOS updateOS) {
		this.updateOS = updateOS;
	}

	public void setResizeRAM(ResizeRAM resizeRAM) {
		this.resizeRAM = resizeRAM;
	}

	public ResizeRAM getResizeRAM() {
		return this.resizeRAM;
	}

	public void setSuspendVM(SuspendVM suspendVM) {
		this.suspendVM = suspendVM;
	}

	public SuspendVM getSuspendVM() {
		return this.suspendVM;
	}

	public void setStopVMForce(StopVMForce stopVMForce) {
		this.stopVMForce = stopVMForce;
	}

	public StopVMForce getStopVMForce() {
		return this.stopVMForce;
	}

	public void setUnplugDevice(UnplugDevice unplugDevice) {
		this.unplugDevice = unplugDevice;
	}

	public UnplugDevice getUnplugDevice() {
		return this.unplugDevice;
	}

	public void setUnplugNIC(UnplugNIC unplugNIC) {
		this.unplugNIC = unplugNIC;
	}

	public UnplugNIC getUnplugNIC() {
		return this.unplugNIC;
	}

	public void setMigrateVM(MigrateVM migrateVM) {
		this.migrateVM = migrateVM;
	}

	public MigrateVM getMigrateVM() {
		return this.migrateVM;
	}

	public void setChangeNumberOfCPU(ChangeNumberOfCPU changeNumberOfCPU) {
		this.changeNumberOfCPU = changeNumberOfCPU;
	}

	public ChangeNumberOfCPU getChangeNumberOfCPU() {
		return this.changeNumberOfCPU;
	}

	public void setResumeVM(ResumeVM resumeVM) {
		this.resumeVM = resumeVM;
	}

	public ResumeVM getResumeVM() {
		return this.resumeVM;
	}

	public CreateAndStartVMFromISO getCreateAndStartVMFromISO() {
		return createAndStartVMFromISO;
	}

	public void setCreateAndStartVMFromISO(CreateAndStartVMFromISO createAndStartVMFromISO) {
		this.createAndStartVMFromISO = createAndStartVMFromISO;
	}

	public CreateAndStartVMFromImage getCreateAndStartVMFromImage() {
		return createAndStartVMFromImage;
	}

	public void setCreateAndStartVMFromImage(CreateAndStartVMFromImage createAndStartVMFromImage) {
		this.createAndStartVMFromImage = createAndStartVMFromImage;
	}

	public void setPlugDisk(PlugDisk plugDisk) {
		this.plugDisk = plugDisk;
	}

	public PlugDisk getPlugDisk() {
		return this.plugDisk;
	}

	public void setPlugDevice(PlugDevice plugDevice) {
		this.plugDevice = plugDevice;
	}

	public PlugDevice getPlugDevice() {
		return this.plugDevice;
	}

	public void setResetVM(ResetVM resetVM) {
		this.resetVM = resetVM;
	}

	public ResetVM getResetVM() {
		return this.resetVM;
	}

	public void setStopVM(StopVM stopVM) {
		this.stopVM = stopVM;
	}

	public StopVM getStopVM() {
		return this.stopVM;
	}

	public void setStartVM(StartVM startVM) {
		this.startVM = startVM;
	}

	public StartVM getStartVM() {
		return this.startVM;
	}

	public void setDeleteVM(DeleteVM deleteVM) {
		this.deleteVM = deleteVM;
	}

	public DeleteVM getDeleteVM() {
		return this.deleteVM;
	}

	public void setRebootVM(RebootVM rebootVM) {
		this.rebootVM = rebootVM;
	}

	public RebootVM getRebootVM() {
		return this.rebootVM;
	}

	public void setPlugNIC(PlugNIC plugNIC) {
		this.plugNIC = plugNIC;
	}

	public PlugNIC getPlugNIC() {
		return this.plugNIC;
	}

	public ConvertVMToImage getConvertVMToImage() {
		return convertVMToImage;
	}

	public void setConvertVMToImage(ConvertVMToImage convertVMToImage) {
		this.convertVMToImage = convertVMToImage;
	}

	public InsertISO getInsertISO() {
		return insertISO;
	}

	public void setInsertISO(InsertISO insertISO) {
		this.insertISO = insertISO;
	}

	public EjectISO getEjectISO() {
		return ejectISO;
	}

	public void setEjectISO(EjectISO ejectISO) {
		this.ejectISO = ejectISO;
	}

	public ResizeVM getResizeVM() {
		return resizeVM;
	}

	public void setResizeVM(ResizeVM resizeVM) {
		this.resizeVM = resizeVM;
	}

	public CloneVM getCloneVM() {
		return cloneVM;
	}

	public void setCloneVM(CloneVM cloneVM) {
		this.cloneVM = cloneVM;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ResizeRAM {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = true, description = "内存大小，单位为KiB", constraint = "100MiB到100GiB", example = "1GiB: 1048576")
		@Pattern(regexp = RegExpUtils.RAM_KiB_PATTERN)
		protected String size;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "本次生效，如果虚拟机开机状态使用", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public String getSize() {
			return size;
		}

		public void setSize(String size) {
			this.size = size;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
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
	public static class SuspendVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class StopVMForce {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class UnplugDevice {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "设备xml文件，可以是GPU、硬盘、网卡、光驱等", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/unplug.xml")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String file;

		public UnplugDevice() {

		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setFile(String file) {
			this.file = file;
		}

		public String getFile() {
			return this.file;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
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
	public static class UnplugNIC {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "虚拟机网络类型", constraint = AnnotationUtils.DESC_BRIDGE_DESC, example = "true")
		@Pattern(regexp = RegExpUtils.SWITCH_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = true, description = "mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String mac;

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getType() {
			return this.type;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getLive() {
			return this.live;
		}

		public void setMac(String mac) {
			this.mac = mac;
		}

		public String getMac() {
			return this.mac;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class MigrateVM {

		protected Boolean suspend;

		protected Boolean direct;

		protected Boolean change_protection;

		protected Boolean rdma_pin_all;

		protected Boolean undefinesource;

		protected Boolean copy_storage_all;

		protected Boolean unsafe;

		protected Boolean copy_storage_inc;

		protected Boolean p2p;

		protected Boolean auto_converge;

		protected Boolean postcopy;

		@ParameterDescriber(required = false, description = "虚拟机关机迁移，关机时时必填", constraint = "虚拟机关机迁移，关机时时必填", example = "true")
		protected Boolean offline;

		protected Boolean tunnelled;

		protected String domain;

		@ParameterDescriber(required = true, description = "目标主机服务地址，主机之间需要提前免密登录", constraint = "目标主机的服务url，主机之间需要提前配置免密登录", example = "133.133.135.31")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String ip;

		protected Boolean abort_on_error;

		protected Boolean compressed;

		protected Boolean persistent;

		protected Boolean live;

		protected String desturi;

		public String getDesturi() {
			return desturi;
		}

		public void setDesturi(String desturi) {
			this.desturi = desturi;
		}

		public void setSuspend(Boolean suspend) {
			this.suspend = suspend;
		}

		public Boolean getSuspend() {
			return this.suspend;
		}

		public void setDirect(Boolean direct) {
			this.direct = direct;
		}

		public Boolean getDirect() {
			return this.direct;
		}

		public void setChange_protection(Boolean change_protection) {
			this.change_protection = change_protection;
		}

		public Boolean getChange_protection() {
			return this.change_protection;
		}

		public void setRdma_pin_all(Boolean rdma_pin_all) {
			this.rdma_pin_all = rdma_pin_all;
		}

		public Boolean getRdma_pin_all() {
			return this.rdma_pin_all;
		}

		public void setUndefinesource(Boolean undefinesource) {
			this.undefinesource = undefinesource;
		}

		public Boolean getUndefinesource() {
			return this.undefinesource;
		}

		public void setCopy_storage_all(Boolean copy_storage_all) {
			this.copy_storage_all = copy_storage_all;
		}

		public Boolean getCopy_storage_all() {
			return this.copy_storage_all;
		}

		public void setUnsafe(Boolean unsafe) {
			this.unsafe = unsafe;
		}

		public Boolean getUnsafe() {
			return this.unsafe;
		}

		public void setCopy_storage_inc(Boolean copy_storage_inc) {
			this.copy_storage_inc = copy_storage_inc;
		}

		public Boolean getCopy_storage_inc() {
			return this.copy_storage_inc;
		}

		public void setP2p(Boolean p2p) {
			this.p2p = p2p;
		}

		public Boolean getP2p() {
			return this.p2p;
		}

		public void setAuto_converge(Boolean auto_converge) {
			this.auto_converge = auto_converge;
		}

		public Boolean getAuto_converge() {
			return this.auto_converge;
		}

		public void setPostcopy(Boolean postcopy) {
			this.postcopy = postcopy;
		}

		public Boolean getPostcopy() {
			return this.postcopy;
		}

		public void setOffline(Boolean offline) {
			this.offline = offline;
		}

		public Boolean getOffline() {
			return this.offline;
		}

		public void setTunnelled(Boolean tunnelled) {
			this.tunnelled = tunnelled;
		}

		public Boolean getTunnelled() {
			return this.tunnelled;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getDomain() {
			return this.domain;
		}

		public void setIp(String ip) {
			this.ip = ip;
		}

		public String getIp() {
			return this.ip;
		}

		public void setAbort_on_error(Boolean abort_on_error) {
			this.abort_on_error = abort_on_error;
		}

		public Boolean getAbort_on_error() {
			return this.abort_on_error;
		}

		public void setCompressed(Boolean compressed) {
			this.compressed = compressed;
		}

		public Boolean getCompressed() {
			return this.compressed;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
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
	public static class MigrateVMDisk {

		protected String domain;

		@ParameterDescriber(required = true, description = "目标主机服务地址，主机之间需要提前免密登录", constraint = "目标主机的服务url，主机之间需要提前配置免密登录", example = "133.133.135.31")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String ip;

		@ParameterDescriber(required = true, description = "需要迁移的云盘和云盘要迁移到的存储池，必须遵守vol=disk1,pool=poolnfs1的格式，有多个要迁移的云盘需要用分号分割开，如vol=/var/lib/libvirt/cstor/pool1/pool1/disk1,pool=poolnfs1;vol=/var/lib/libvirt/cstor/pool2/pool2/disk2,pool=poolnfs2，目标存储池要在要迁移的目标节点。支持其他类型的存储到的文件类型存储的迁移，支持块设备到相同存储池uuid之间的迁移，不支持文件类型到块设备类型的迁移和块设备类型到其他uuid块设备存储的迁移。", constraint = "云主机存储迁移", example = "disk=/var/lib/libvirt/cstor/pool1/pool1/disk1,pool=poolnfs1;disk=/var/lib/libvirt/cstor/pool2/pool2/disk2,pool=poolnfs2")
		protected String migratedisks;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getIp() {
			return ip;
		}

		public void setIp(String ip) {
			this.ip = ip;
		}

		public String getMigratedisks() {
			return migratedisks;
		}

		public void setMigratedisks(String migratedisks) {
			this.migratedisks = migratedisks;
		}
	}


	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ChangeNumberOfCPU {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = false, description = "对于开机虚拟机进行运行时插拔，与--live等价", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean hotpluggable;

		@ParameterDescriber(required = true, description = "vcpu数量", constraint = "1-100个", example = "16")
		@Pattern(regexp = RegExpUtils.VCPU_PATTERN)
		protected String count;

		@ParameterDescriber(required = false, description = "修改虚拟机CPU状态", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean guest;
		
		@ParameterDescriber(required = false, description = "最大vcpu数量，重启后生效", constraint = "1-100个", example = "16")
		@Pattern(regexp = RegExpUtils.BOOL_TYPE_PATTERN)
		protected Boolean maximum;
		
		@ParameterDescriber(required = false, description = "当设置最大vcpu数量时为必填参数，设置cpu核数", constraint = "约束条件：最大vcpu数量=cpu核数×cpu插槽数×cpu线程数", example = "16")
		@Pattern(regexp = RegExpUtils.VCPU_PATTERN)
		protected String cores;
		
		@ParameterDescriber(required = false, description = "当设置最大vcpu数量时为必填参数，设置cpu插槽数", constraint = "约束条件：最大vcpu数量=cpu核数×cpu插槽数×cpu线程数", example = "1")
		@Pattern(regexp = RegExpUtils.VCPU_PATTERN)
		protected String sockets;
		
		@ParameterDescriber(required = false, description = "当设置最大vcpu数量时为必填参数，设置cpu线程数", constraint = "约束条件：最大vcpu数量=cpu核数×cpu插槽数×cpu线程数", example = "1")
		@Pattern(regexp = RegExpUtils.VCPU_PATTERN)
		protected String threads;

		public String getCores() {
			return cores;
		}

		public void setCores(String cores) {
			this.cores = cores;
		}

		public String getSockets() {
			return sockets;
		}

		public void setSockets(String sockets) {
			this.sockets = sockets;
		}

		public String getThreads() {
			return threads;
		}

		public void setThreads(String threads) {
			this.threads = threads;
		}

		public Boolean getMaximum() {
			return maximum;
		}

		public void setMaximum(Boolean maximum) {
			this.maximum = maximum;
		}

		public ChangeNumberOfCPU() {

		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setHotpluggable(Boolean hotpluggable) {
			this.hotpluggable = hotpluggable;
		}

		public Boolean getHotpluggable() {
			return this.hotpluggable;
		}

		public String getCount() {
			return count;
		}

		public void setCount(String count) {
			this.count = count;
		}

		public void setGuest(Boolean guest) {
			this.guest = guest;
		}

		public Boolean getGuest() {
			return this.guest;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
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
	public static class ResumeVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class PlugDisk {

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		protected String iothread;

		@ParameterDescriber(required = false, description = "云盘缓存类型", constraint = "取值范围：none, writethrough, directsync, unsafe, writeback", example = "none")
		@Pattern(regexp = RegExpUtils.DISK_CACHE_PATTERN)
		protected String cache;

		protected String address;

		protected String io;
		
		@ParameterDescriber(required = false, description = "云盘SCSI设备IO模式，默认值unfiltered", constraint = "取值范围：unfiltered, filtered", example = "unfiltered")
		@Pattern(regexp = RegExpUtils.DISK_SGIO_PATTERN)
		protected String sgio;

		@ParameterDescriber(required = true, description = "云盘源路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/images/test1.qcow2")
//		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String source;

		@ParameterDescriber(required = false, description = "虚拟的云盘总线类型，如果不填将根据target的取值自动匹配，例如vdX匹配为virtio类型的总线、sdX匹配为scsi类型的总线", constraint = "取值范围：ide, scsi, virtio, xen, usb, sata, sd", example = "virtio")
		@Pattern(regexp = RegExpUtils.DISK_BUS_PATTERN)
		protected String targetbus;

		@ParameterDescriber(required = false, description = "云盘类型", constraint = "取值范围：disk, lun, cdrom, floppy", example = "disk")
		@Pattern(regexp = RegExpUtils.DISK_TYPE_PATTERN)
		protected String type;
		
		@ParameterDescriber(required = false, description = "云盘子驱动类型", constraint = "取值范围：qcow2, raw", example = "qcow2")
		@Pattern(regexp = RegExpUtils.DISK_SUBDRIVER_PATTERN)
		protected String subdriver;

		protected Boolean multifunction;

		@ParameterDescriber(required = true, description = "目标盘符，对应虚拟机内看到的盘符号，其中vdX对应virtio支持的文件存储，hdX对应ide存储（如cdrom），sdX对应iscsi块存储", constraint = "取值范围：vdX, hdX, sdX", example = "vdc")
		@Pattern(regexp = RegExpUtils.FDISK_TYPE_PATTERN)
		protected String target;

		protected String wwn;

		@ParameterDescriber(required = false, description = "读写类型", constraint = "取值范围：readonly, shareable", example = "shareable")
		@Pattern(regexp = RegExpUtils.DISK_MODE_PATTERN)
		protected String mode;

		@ParameterDescriber(required = false, description = "云盘驱动类型", constraint = "取值范围：qemu", example = "qemu")
		@Pattern(regexp = RegExpUtils.DISK_DRIVER_PATTERN)
		protected String driver;

		protected String serial;

		protected Boolean rawio;

		@ParameterDescriber(required = false, description = "云盘源类型", constraint = "取值范围：file, block", example = "file")
		@Pattern(regexp = RegExpUtils.DISK_SOURCE_TYPE_PATTERN)
		protected String sourcetype;

		@ParameterDescriber(required = false, description = "云盘总bps的QoS设置，单位为bytes，与read,write互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String total_bytes_sec;

		@ParameterDescriber(required = false, description = "云盘读bps的QoS设置，单位为bytes，与total互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String read_bytes_sec;

		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘写bps的QoS设置，单位为bytes，与total互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		protected String write_bytes_sec;

		@ParameterDescriber(required = false, description = "云盘总iops的QoS设置，单位为bytes，与read,write互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String total_iops_sec;

		@Pattern(regexp = RegExpUtils.DISK_IOPS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘读iops的QoS设置，与total互斥", constraint = "0~99999", example = "40000")
		protected String read_iops_sec;

		@Pattern(regexp = RegExpUtils.DISK_IOPS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘写iops的QoS设置，与total互斥", constraint = "0~99999", example = "40000")
		protected String write_iops_sec;

		public String getSgio() {
			return sgio;
		}

		public void setSgio(String sgio) {
			this.sgio = sgio;
		}

		public String getTotal_bytes_sec() {
			return total_bytes_sec;
		}

		public void setTotal_bytes_sec(String total_bytes_sec) {
			this.total_bytes_sec = total_bytes_sec;
		}

		public String getTotal_iops_sec() {
			return total_iops_sec;
		}

		public void setTotal_iops_sec(String total_iops_sec) {
			this.total_iops_sec = total_iops_sec;
		}

		public PlugDisk() {

		}

		public String getRead_bytes_sec() {
			return read_bytes_sec;
		}

		public void setRead_bytes_sec(String read_bytes_sec) {
			this.read_bytes_sec = read_bytes_sec;
		}

		public String getWrite_bytes_sec() {
			return write_bytes_sec;
		}

		public void setWrite_bytes_sec(String write_bytes_sec) {
			this.write_bytes_sec = write_bytes_sec;
		}

		public String getRead_iops_sec() {
			return read_iops_sec;
		}

		public void setRead_iops_sec(String read_iops_sec) {
			this.read_iops_sec = read_iops_sec;
		}

		public String getWrite_iops_sec() {
			return write_iops_sec;
		}

		public void setWrite_iops_sec(String write_iops_sec) {
			this.write_iops_sec = write_iops_sec;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public void setIothread(String iothread) {
			this.iothread = iothread;
		}

		public String getIothread() {
			return this.iothread;
		}

		public void setCache(String cache) {
			this.cache = cache;
		}

		public String getCache() {
			return this.cache;
		}

		public void setAddress(String address) {
			this.address = address;
		}

		public String getAddress() {
			return this.address;
		}

		public void setIo(String io) {
			this.io = io;
		}

		public String getIo() {
			return this.io;
		}

		public void setSource(String source) {
			this.source = source;
		}

		public String getSource() {
			return this.source;
		}

		public void setTargetbus(String targetbus) {
			this.targetbus = targetbus;
		}

		public String getTargetbus() {
			return this.targetbus;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getType() {
			return this.type;
		}

		public void setSubdriver(String subdriver) {
			this.subdriver = subdriver;
		}

		public String getSubdriver() {
			return this.subdriver;
		}

		public void setMultifunction(Boolean multifunction) {
			this.multifunction = multifunction;
		}

		public Boolean getMultifunction() {
			return this.multifunction;
		}

		public void setTarget(String target) {
			this.target = target;
		}

		public String getTarget() {
			return this.target;
		}

		public void setWwn(String wwn) {
			this.wwn = wwn;
		}

		public String getWwn() {
			return this.wwn;
		}

		public void setMode(String mode) {
			this.mode = mode;
		}

		public String getMode() {
			return this.mode;
		}

		public void setDriver(String driver) {
			this.driver = driver;
		}

		public String getDriver() {
			return this.driver;
		}

		public void setSerial(String serial) {
			this.serial = serial;
		}

		public String getSerial() {
			return this.serial;
		}

		public void setRawio(Boolean rawio) {
			this.rawio = rawio;
		}

		public Boolean getRawio() {
			return this.rawio;
		}

		public void setSourcetype(String sourcetype) {
			this.sourcetype = sourcetype;
		}

		public String getSourcetype() {
			return this.sourcetype;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class PlugDevice {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "设备xml文件，可以是GPU、硬盘、网卡、光驱等", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/unplug.xml")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String file;

		public PlugDevice() {

		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setFile(String file) {
			this.file = file;
		}

		public String getFile() {
			return this.file;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
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
	public static class ResetVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class UnplugDisk {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "设备的目标，即在虚拟机中fdisk -l看到的硬盘标记", constraint = AnnotationUtils.DESC_TARGET_DESC, example = "windows: hdb, Linux: vdb")
		@Pattern(regexp = RegExpUtils.FDISK_TYPE_PATTERN)
		protected String target;

		public UnplugDisk() {

		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getLive() {
			return this.live;
		}

		public void setTarget(String target) {
			this.target = target;
		}

		public String getTarget() {
			return this.target;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class StopVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class StartVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteVM {

		@ParameterDescriber(required = false, description = "删除虚拟机所有快照，否则如果虚拟机还存在快照，会导致删除失败", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean snapshots_metadata;

		@ParameterDescriber(required = false, description = "是否删除虚拟机所有快照对应的磁盘存储", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean remove_all_storage;

		@ParameterDescriber(required = false, description = "需要删除的虚拟机磁盘", constraint = "约束：盘符,路径", example = "vda,/var/lib/libvirt/images/disk1")
		protected String storage;

		@ParameterDescriber(required = false, description = "ARM架构机器需要添加此参数", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean nvram;

		public String getStorage() {
			return storage;
		}

		public void setStorage(String storage) {
			this.storage = storage;
		}

		public Boolean getNvram() {
			return nvram;
		}

		public void setNvram(Boolean nvram) {
			this.nvram = nvram;
		}

		public Boolean getSnapshots_metadata() {
			return snapshots_metadata;
		}

		public void setSnapshots_metadata(Boolean snapshots_metadata) {
			this.snapshots_metadata = snapshots_metadata;
		}

		public void setRemove_all_storage(Boolean remove_all_storage) {
			this.remove_all_storage = remove_all_storage;
		}

		public Boolean getRemove_all_storage() {
			return this.remove_all_storage;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateAndStartVMFromISO {

		protected String container;

		@ParameterDescriber(required = false, description = "用户生成虚拟机的元数据", constraint = "uuid=<UUID>，UUID是字符串类型，长度是12到36位，只允许数字、小写字母、中划线、以及圆点", example = "uuid=950646e8-c17a-49d0-b83c-1c797811e001")
		@Pattern(regexp = RegExpUtils.UUID_PATTERN)
		protected String metadata;

		@ParameterDescriber(required = false, description = "安装操作系统时光驱是否属于livecd类型", constraint = "取值范围：true/false", example = "true")
		@Pattern(regexp = RegExpUtils.BOOL_TYPE_PATTERN)
		protected String livecd;

		protected String sound;

		protected String channel;

		@ParameterDescriber(required = true, description = "虚拟机VNC/SPICE及其密码", constraint = "取值范围：<vnc/spice,listen=0.0.0.0>,password=xxx（<必填>，选填），密码为4-16位，是小写字母、数字和中划线组合", example = "vnc,listen=0.0.0.0,password=abcdefg")
		@Pattern(regexp = RegExpUtils.GRAPHICS_PATTERN)
		protected String graphics;

		protected String autostart;

		protected String features;

		protected String hostdev;

		protected String idmap;

		protected String sysinfo;

		protected String numatune;

		protected String events;

		protected String hvm;

		protected String qemu_commandline;

		protected String resource;

		protected String extra_args;

		protected String cpu;

		protected String rng;

		protected String check;

		protected String clock;

		protected String smartcard;

		protected String panic;

		protected String input;

		@ParameterDescriber(required = true, description = "虚拟机磁盘，包括硬盘和光驱", constraint = "硬盘的约束：/var/lib/libvirt/images/test3.qcow2,target=hda,read_bytes_sec=1024000000,write_bytes_sec=1024000000，"
				+ "光驱的约束：/opt/ISO/CentOS-7-x86_64-Minimal-1511.iso,device=cdrom,perms=ro，支持多个硬盘，第一个硬盘无需添加--disk，后续的需要", example = "/var/lib/libvirt/images/test3.qcow2,read_bytes_sec=1024000000,write_bytes_sec=1024000000 --disk /opt/ISO/CentOS-7-x86_64-Minimal-1511.iso,device=cdrom,perms=ro")
//		@Pattern(regexp = RegExpUtils.MUTI_DISKS_PATTERN)
		protected String disk;

		protected String memorybacking;

		protected String dry_run;

		@ParameterDescriber(required = true, description = "虚拟机内存大小，单位为MiB", constraint = "取值范围：100~99999", example = "2048")
		@Pattern(regexp = RegExpUtils.RAM_MiB_PATTERN)
		protected String memory;

		protected String paravirt;

		protected String memballoon;

		@ParameterDescriber(required = true, description = "虚拟机网络", constraint = "type=bridge（libvirt默认网桥virbr0）/ l2bridge（ovs网桥）/ l3bridge（支持ovn的ovs网桥），"
				+ "source=源网桥（必填），inbound=网络输入带宽QoS限制，单位为KiB，outbound=网络输出带宽QoS限制，单位为KiB，"
				+ "ip=IP地址（选填，只有type=l3bridge类型支持该参数），"
				+ "switch=ovn交换机名称（选填，只有type=l3bridge类型支持该参数），"
				+ "model=virtio/e1000/rtl8139（windows虚拟机），"
				+ "inbound=io入带宽，"
				+ "outbound=io出带宽，"
				+ "mac=mac地址（选填），"
				+ "参数顺序必须是type,source,ip,switch,model,inbound,outbound,mac", example = "type=l3bridge,source=br-int,ip=192.168.5.9,switch=switch8888,model=e1000,inbound=102400,outbound=102400")
//		@Pattern(regexp = RegExpUtils.NETWORK_TYPE_PATTERN)
		protected String network;

		protected String security;

		protected String blkiotune;

		@ParameterDescriber(required = false, description = "虚拟化类型", constraint = "取值范围：kvm, xen", example = "kvm")
		@Pattern(regexp = RegExpUtils.VIRT_TYPE_PATTERN)
		protected String virt_type;

		protected String parallel;

		protected String memtune;

		@ParameterDescriber(required = false, description = "设置启动顺序", constraint = "hd|cdrom，分别表示硬盘和光驱启动", example = "hd")
		@Pattern(regexp = RegExpUtils.BOOT_PATTERN)
		protected String boot;

		protected String initrd_inject;

		protected String pxe;

		protected String console;

		protected String controller;

		protected String memdev;

		@ParameterDescriber(required = false, description = "支持USB重定向", constraint = "协议,类型=，服务器=IP：端口", example = "usb,type=tcp,server=192.168.1.1:4000")
//		@Pattern(regexp = RegExpUtils.USB_PATTERN)
		protected String redirdev;

		@ParameterDescriber(required = true, description = "操作系统类型，如果不设置可能发生鼠标偏移等问题", constraint = "参考https://tower.im/teams/616100/repository_documents/3550/", example = "centos7.0")
		@Pattern(regexp = RegExpUtils.OS_PATTERN)
		protected String os_variant;

		@ParameterDescriber(required = true, description = "虚拟机CPU个数，选填参数依次是：cpuset允许绑定具体物理CPU、maxvcpus最大vcpu个数、cores核数、sockets插槽数、threads线程数", constraint = "约束条件：最大vcpu数量=cpu核数×cpu插槽数×cpu线程数", example = "2,cpuset=1-4,maxvcpus=40,cores=40,sockets=1,threads=1")
//		@Pattern(regexp = RegExpUtils.VCPUSET_PATTERN)
		protected String vcpus;

		@ParameterDescriber(required = false, description = "虚拟机挂载的光驱，重启失效", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/ISO/CentOS-7-x86_64-Minimal-1511.iso")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String cdrom;

		@ParameterDescriber(required = false, description = "设置虚拟机CPU参数", constraint = "参考virt-install中的--cputune参数", example = "vcpupin0.vcpu=0")
		protected String cputune;

		protected String filesystem;

		protected String tpm;

		protected String watchdog;

		protected String serial;

		protected String machine;

		protected String location;

		protected String arch;

		protected String noreboot;

		protected String pm;

		@ParameterDescriber(required = true, description = "不自动连接到虚拟机终端，必须设置成true", constraint = "true", example = "true")
		protected Boolean noautoconsole = true;

		protected Boolean _import;

		public CreateAndStartVMFromISO() {

		}

		public Boolean get_import() {
			return _import;
		}

		public void set_import(Boolean _import) {
			this._import = _import;
		}

		public String getDisk() {
			return disk;
		}

		public void setDisk(String disk) {
			this.disk = disk;
		}

		public Boolean getNoautoconsole() {
			return noautoconsole;
		}

		public Boolean isNoautoconsole() {
			return noautoconsole;
		}

		public void setNoautoconsole(Boolean noautoconsole) {
			this.noautoconsole = noautoconsole;
		}

		public void setContainer(String container) {
			this.container = container;
		}

		public String getContainer() {
			return this.container;
		}

		public void setMetadata(String metadata) {
			this.metadata = metadata;
		}

		public String getMetadata() {
			return this.metadata;
		}

		public void setLivecd(String livecd) {
			this.livecd = livecd;
		}

		public String getLivecd() {
			return this.livecd;
		}

		public void setSound(String sound) {
			this.sound = sound;
		}

		public String getSound() {
			return this.sound;
		}

		public void setChannel(String channel) {
			this.channel = channel;
		}

		public String getChannel() {
			return this.channel;
		}

		public void setGraphics(String graphics) {
			this.graphics = graphics;
		}

		public String getGraphics() {
			return this.graphics;
		}

		public void setAutostart(String autostart) {
			this.autostart = autostart;
		}

		public String getAutostart() {
			return this.autostart;
		}

		public void setFeatures(String features) {
			this.features = features;
		}

		public String getFeatures() {
			return this.features;
		}

		public void setHostdev(String hostdev) {
			this.hostdev = hostdev;
		}

		public String getHostdev() {
			return this.hostdev;
		}

		public void setIdmap(String idmap) {
			this.idmap = idmap;
		}

		public String getIdmap() {
			return this.idmap;
		}

		public void setSysinfo(String sysinfo) {
			this.sysinfo = sysinfo;
		}

		public String getSysinfo() {
			return this.sysinfo;
		}

		public void setNumatune(String numatune) {
			this.numatune = numatune;
		}

		public String getNumatune() {
			return this.numatune;
		}

		public void setEvents(String events) {
			this.events = events;
		}

		public String getEvents() {
			return this.events;
		}

		public void setHvm(String hvm) {
			this.hvm = hvm;
		}

		public String getHvm() {
			return this.hvm;
		}

		public void setQemu_commandline(String qemu_commandline) {
			this.qemu_commandline = qemu_commandline;
		}

		public String getQemu_commandline() {
			return this.qemu_commandline;
		}

		public void setResource(String resource) {
			this.resource = resource;
		}

		public String getResource() {
			return this.resource;
		}

		public void setExtra_args(String extra_args) {
			this.extra_args = extra_args;
		}

		public String getExtra_args() {
			return this.extra_args;
		}

		public void setCpu(String cpu) {
			this.cpu = cpu;
		}

		public String getCpu() {
			return this.cpu;
		}

		public void setRng(String rng) {
			this.rng = rng;
		}

		public String getRng() {
			return this.rng;
		}

		public void setCheck(String check) {
			this.check = check;
		}

		public String getCheck() {
			return this.check;
		}

		public void setClock(String clock) {
			this.clock = clock;
		}

		public String getClock() {
			return this.clock;
		}

		public void setSmartcard(String smartcard) {
			this.smartcard = smartcard;
		}

		public String getSmartcard() {
			return this.smartcard;
		}

		public void setPanic(String panic) {
			this.panic = panic;
		}

		public String getPanic() {
			return this.panic;
		}

		public void setInput(String input) {
			this.input = input;
		}

		public String getInput() {
			return this.input;
		}

		public void setMemorybacking(String memorybacking) {
			this.memorybacking = memorybacking;
		}

		public String getMemorybacking() {
			return this.memorybacking;
		}

		public void setDry_run(String dry_run) {
			this.dry_run = dry_run;
		}

		public String getDry_run() {
			return this.dry_run;
		}

		public void setMemory(String memory) {
			this.memory = memory;
		}

		public String getMemory() {
			return this.memory;
		}

		public void setParavirt(String paravirt) {
			this.paravirt = paravirt;
		}

		public String getParavirt() {
			return this.paravirt;
		}

		public void setMemballoon(String memballoon) {
			this.memballoon = memballoon;
		}

		public String getMemballoon() {
			return this.memballoon;
		}

		public void setNetwork(String network) {
			this.network = network;
		}

		public String getNetwork() {
			return this.network;
		}

		public void setSecurity(String security) {
			this.security = security;
		}

		public String getSecurity() {
			return this.security;
		}

		public void setBlkiotune(String blkiotune) {
			this.blkiotune = blkiotune;
		}

		public String getBlkiotune() {
			return this.blkiotune;
		}

		public void setVirt_type(String virt_type) {
			this.virt_type = virt_type;
		}

		public String getVirt_type() {
			return this.virt_type;
		}

		public void setParallel(String parallel) {
			this.parallel = parallel;
		}

		public String getParallel() {
			return this.parallel;
		}

		public void setMemtune(String memtune) {
			this.memtune = memtune;
		}

		public String getMemtune() {
			return this.memtune;
		}

		public void setBoot(String boot) {
			this.boot = boot;
		}

		public String getBoot() {
			return this.boot;
		}

		public void setInitrd_inject(String initrd_inject) {
			this.initrd_inject = initrd_inject;
		}

		public String getInitrd_inject() {
			return this.initrd_inject;
		}

		public void setPxe(String pxe) {
			this.pxe = pxe;
		}

		public String getPxe() {
			return this.pxe;
		}

		public void setConsole(String console) {
			this.console = console;
		}

		public String getConsole() {
			return this.console;
		}

		public void setController(String controller) {
			this.controller = controller;
		}

		public String getController() {
			return this.controller;
		}

		public void setMemdev(String memdev) {
			this.memdev = memdev;
		}

		public String getMemdev() {
			return this.memdev;
		}

		public void setRedirdev(String redirdev) {
			this.redirdev = redirdev;
		}

		public String getRedirdev() {
			return this.redirdev;
		}

		public void setOs_variant(String os_variant) {
			this.os_variant = os_variant;
		}

		public String getOs_variant() {
			return this.os_variant;
		}

		public void setVcpus(String vcpus) {
			this.vcpus = vcpus;
		}

		public String getVcpus() {
			return this.vcpus;
		}

		public void setCdrom(String cdrom) {
			this.cdrom = cdrom;
		}

		public String getCdrom() {
			return this.cdrom;
		}

		public void setCputune(String cputune) {
			this.cputune = cputune;
		}

		public String getCputune() {
			return this.cputune;
		}

		public void setFilesystem(String filesystem) {
			this.filesystem = filesystem;
		}

		public String getFilesystem() {
			return this.filesystem;
		}

		public void setTpm(String tpm) {
			this.tpm = tpm;
		}

		public String getTpm() {
			return this.tpm;
		}

		public void setWatchdog(String watchdog) {
			this.watchdog = watchdog;
		}

		public String getWatchdog() {
			return this.watchdog;
		}

		public void setSerial(String serial) {
			this.serial = serial;
		}

		public String getSerial() {
			return this.serial;
		}

		public void setMachine(String machine) {
			this.machine = machine;
		}

		public String getMachine() {
			return this.machine;
		}

		public void setLocation(String location) {
			this.location = location;
		}

		public String getLocation() {
			return this.location;
		}

		public void setArch(String arch) {
			this.arch = arch;
		}

		public String getArch() {
			return this.arch;
		}

		public void setNoreboot(String noreboot) {
			this.noreboot = noreboot;
		}

		public String getNoreboot() {
			return this.noreboot;
		}

		public void setPm(String pm) {
			this.pm = pm;
		}

		public String getPm() {
			return this.pm;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateAndStartVMFromImage extends CreateAndStartVMFromISO {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RebootVM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class PlugNIC {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = false, description = "网络输入带宽QoS限制，单位为KiB，示例参考https://libvirt.org/formatnetwork.html#elementQoS", constraint = "0~99999999", example = "1000MiB: 1024000")
		@Pattern(regexp = RegExpUtils.NET_QoS_PATTERN)
		protected String inbound;

		@ParameterDescriber(required = true, description = "网络源设置", constraint = "source=源网桥（必填，默认为virbr0, br-native, br-int，以及用户自己创建的任何两层bridge名称），ip=IP地址（选填，只有type=l3bridge类型支持该参数），switch=ovn交换机名称（选填，只有type=l3bridge类型支持该参数）,顺序必须是source,ip,switch", example = "source=br-int,ip=192.168.5.2,switch=switch")
		@Pattern(regexp = RegExpUtils.IP_SWITCH_PATTERN)
		protected String source;

		@ParameterDescriber(required = true, description = "网络源类型设置", constraint = "取值范围：bridge（libvirt默认网桥virbr0）, l2bridge（ovs网桥）, l3bridge（支持ovn的ovs网桥）", example = "bridge")
		@Pattern(regexp = RegExpUtils.SWITCH_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = true, description = "mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String mac;

		protected String script;

		protected String target;

		protected Boolean managed;

		@ParameterDescriber(required = false, description = "网络输出带宽QoS限制，单位为KiB，示例参考https://libvirt.org/formatnetwork.html#elementQoS", constraint = "0~99999999", example = "1000MiB: 1024000")
		@Pattern(regexp = RegExpUtils.NET_QoS_PATTERN)
		protected String outbound;

		protected String model;

		public PlugNIC() {

		}

		public void setInbound(String inbound) {
			this.inbound = inbound;
		}

		public String getInbound() {
			return this.inbound;
		}

		public void setSource(String source) {
			this.source = source;
		}

		public String getSource() {
			return this.source;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getType() {
			return this.type;
		}

		public void setMac(String mac) {
			this.mac = mac;
		}

		public String getMac() {
			return this.mac;
		}

		public void setScript(String script) {
			this.script = script;
		}

		public String getScript() {
			return this.script;
		}

		public void setTarget(String target) {
			this.target = target;
		}

		public String getTarget() {
			return this.target;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getCurrent() {
			return this.current;
		}

		public void setManaged(Boolean managed) {
			this.managed = managed;
		}

		public Boolean getManaged() {
			return this.managed;
		}

		public void setOutbound(String outbound) {
			this.outbound = outbound;
		}

		public String getOutbound() {
			return this.outbound;
		}

		public void setModel(String model) {
			this.model = model;
		}

		public String getModel() {
			return this.model;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getPersistent() {
			return this.persistent;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getConfig() {
			return this.config;
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
	public static class ManageISO {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "目标盘符，对应虚拟机内看到的盘符号", constraint = "取值范围：vdX, hdX, sdX", example = "vdc")
		@Pattern(regexp = RegExpUtils.FDISK_TYPE_PATTERN)
		protected String path;

		@ParameterDescriber(required = true, description = "模板虚拟机的路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/target.iso")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String source;

		@ParameterDescriber(required = true, description = "弹出光驱，与--insert不可同时设置为true", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean eject;

		@ParameterDescriber(required = true, description = "插入光驱", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean insert;

		@ParameterDescriber(required = true, description = "更新操作", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean update;

		@ParameterDescriber(required = true, description = "强制执行", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean force;

		@ParameterDescriber(required = true, description = "如果适用物理机光驱，应该设置为true", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean block;

		public String getSource() {
			return source;
		}

		public void setSource(String source) {
			this.source = source;
		}

		public ManageISO() {
			super();
		}

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}

		public Boolean getEject() {
			return eject;
		}

		public void setEject(Boolean eject) {
			this.eject = eject;
		}

		public Boolean getInsert() {
			return insert;
		}

		public void setInsert(Boolean insert) {
			this.insert = insert;
		}

		public Boolean getUpdate() {
			return update;
		}

		public void setUpdate(Boolean update) {
			this.update = update;
		}

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getForce() {
			return force;
		}

		public void setForce(Boolean force) {
			this.force = force;
		}

		public Boolean getBlock() {
			return block;
		}

		public void setBlock(Boolean block) {
			this.block = block;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class InsertISO {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "模板虚拟机的路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/target.iso")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String path;

		@ParameterDescriber(required = true, description = "插入光驱", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean insert;

		@ParameterDescriber(required = true, description = "强制执行", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean force;

		@ParameterDescriber(required = true, description = "如果适用物理机光驱，应该设置为true", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean block;

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}

		public Boolean getInsert() {
			return insert;
		}

		public void setInsert(Boolean insert) {
			this.insert = insert;
		}

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getForce() {
			return force;
		}

		public void setForce(Boolean force) {
			this.force = force;
		}

		public Boolean getBlock() {
			return block;
		}

		public void setBlock(Boolean block) {
			this.block = block;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class EjectISO {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = true, description = "模板虚拟机的路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/target.iso")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String path;

		@ParameterDescriber(required = true, description = "弹出光驱，与--insert不可同时设置为true", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean eject;

		@ParameterDescriber(required = true, description = "强制执行", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean force;

		@ParameterDescriber(required = true, description = "如果适用物理机光驱，应该设置为true", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean block;

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}

		public Boolean getEject() {
			return eject;
		}

		public void setEject(Boolean eject) {
			this.eject = eject;
		}

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getForce() {
			return force;
		}

		public void setForce(Boolean force) {
			this.force = force;
		}

		public Boolean getBlock() {
			return block;
		}

		public void setBlock(Boolean block) {
			this.block = block;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class UpdateOS {

		@ParameterDescriber(required = true, description = "需要被替换的虚拟机路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/source.xml")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String source;

		@ParameterDescriber(required = true, description = "模板虚拟机的路径", constraint = "路径是字符串类型，长度是2到64位，只允许数字、小写字母、中划线、以及圆点", example = "/var/lib/libvirt/target.xml")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String target;

		public UpdateOS() {
			super();
		}

		public String getSource() {
			return source;
		}

		public void setSource(String source) {
			this.source = source;
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
	@Deprecated
	public static class ConvertVMToImage {

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

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ResizeVM {

		@ParameterDescriber(required = true, description = "虚拟机路径", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/images/test1.qcow2")
		@Pattern(regexp = RegExpUtils.PATH_PATTERN)
		protected String path;

		@ParameterDescriber(required = true, description = "虚拟机大小, 1G到1T", constraint = "1000000-999999999999（单位：KiB）", example = "‭10,737,418,240‬")
		@Pattern(regexp = RegExpUtils.DISK_SIZE_KIB_PATTERN)
		protected String size;

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}

		public String getSize() {
			return size;
		}

		public void setSize(String size) {
			this.size = size;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CloneVM {

		@ParameterDescriber(required = true, description = "克隆虚拟机的名称", constraint = "新虚拟机名长度是4到100位", example = "newvm")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String name;

		@ParameterDescriber(required = false, description = "新磁盘路径，多个路径用多个--file标识", constraint = "路径必须在/var/lib/libvirt下，18-1024位，只允许小写、字母、中划线和圆点", example = "/var/lib/libvirt/images/test1.qcow2 --file /var/lib/libvirt/images/test2.qcow2")
		protected String file;

		@ParameterDescriber(required = false, description = "不克隆存储，通过 --file 参数指定的新磁盘镜像将保留不变", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean preserve_data;

		@ParameterDescriber(required = false, description = "网卡的mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String mac;

		@ParameterDescriber(required = false, description = "不使用稀疏文件作为克隆的磁盘镜像", constraint = AnnotationUtils.DESC_BOOLEAN, example = "false")
		protected Boolean nonsparse;

		@ParameterDescriber(required = false, description = "从原始客户机配置中自动生成克隆名称和存储路径", constraint = AnnotationUtils.DESC_BOOLEAN, example = "false")
		protected Boolean auto_clone;

		public String getFile() {
			return file;
		}

		public void setFile(String file) {
			this.file = file;
		}

		public Boolean getPreserve_data() {
			return preserve_data;
		}

		public void setPreserve_data(Boolean preserve_data) {
			this.preserve_data = preserve_data;
		}

		public String getMac() {
			return mac;
		}

		public void setMac(String mac) {
			this.mac = mac;
		}

		public Boolean getNonsparse() {
			return nonsparse;
		}

		public void setNonsparse(Boolean nonsparse) {
			this.nonsparse = nonsparse;
		}

		public Boolean getAuto_clone() {
			return auto_clone;
		}

		public void setAuto_clone(Boolean auto_clone) {
			this.auto_clone = auto_clone;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class TuneDiskQoS {

		@ParameterDescriber(required = true, description = "虚拟机磁盘的盘符号，对应虚拟机内看到的盘符号", constraint = "取值范围：vdX, hdX, sdX", example = "vdc")
		@Pattern(regexp = RegExpUtils.FDISK_TYPE_PATTERN)
		protected String device;

		@ParameterDescriber(required = false, description = "云盘总bps的QoS设置，单位为bytes，与read,write互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String total_bytes_sec;

		@ParameterDescriber(required = false, description = "云盘读bps的QoS设置，单位为bytes，与total互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String read_bytes_sec;

		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘写bps的QoS设置，单位为bytes，与total互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		protected String write_bytes_sec;

		@ParameterDescriber(required = false, description = "云盘总iops的QoS设置，单位为bytes，与read,write互斥", constraint = "0~9999999999", example = "1GiB: 1073741824")
		@Pattern(regexp = RegExpUtils.DISK_QoS_PATTERN)
		protected String total_iops_sec;

		@Pattern(regexp = RegExpUtils.DISK_IOPS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘读iops的QoS设置，与total互斥", constraint = "0~99999", example = "40000")
		protected String read_iops_sec;

		@Pattern(regexp = RegExpUtils.DISK_IOPS_PATTERN)
		@ParameterDescriber(required = false, description = "云盘写iops的QoS设置，与total互斥", constraint = "0~99999", example = "40000")
		protected String write_iops_sec;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		public String getDevice() {
			return device;
		}

		public void setDevice(String device) {
			this.device = device;
		}

		public String getTotal_bytes_sec() {
			return total_bytes_sec;
		}

		public void setTotal_bytes_sec(String total_bytes_sec) {
			this.total_bytes_sec = total_bytes_sec;
		}

		public String getRead_bytes_sec() {
			return read_bytes_sec;
		}

		public void setRead_bytes_sec(String read_bytes_sec) {
			this.read_bytes_sec = read_bytes_sec;
		}

		public String getWrite_bytes_sec() {
			return write_bytes_sec;
		}

		public void setWrite_bytes_sec(String write_bytes_sec) {
			this.write_bytes_sec = write_bytes_sec;
		}

		public String getTotal_iops_sec() {
			return total_iops_sec;
		}

		public void setTotal_iops_sec(String total_iops_sec) {
			this.total_iops_sec = total_iops_sec;
		}

		public String getRead_iops_sec() {
			return read_iops_sec;
		}

		public void setRead_iops_sec(String read_iops_sec) {
			this.read_iops_sec = read_iops_sec;
		}

		public String getWrite_iops_sec() {
			return write_iops_sec;
		}

		public void setWrite_iops_sec(String write_iops_sec) {
			this.write_iops_sec = write_iops_sec;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class TuneNICQoS {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = false, description = "网络输入带宽QoS限制，单位为KiB，示例参考https://libvirt.org/formatnetwork.html#elementQoS", constraint = "0~99999999", example = "1000MiB: 1024000")
		@Pattern(regexp = RegExpUtils.NET_QoS_PATTERN)
		protected String inbound;

		@ParameterDescriber(required = true, description = "网卡的mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String _interface;

		@ParameterDescriber(required = false, description = "网络输出带宽QoS限制，单位为KiB，示例参考https://libvirt.org/formatnetwork.html#elementQoS", constraint = "0~99999999", example = "1000MiB: 1024000")
		@Pattern(regexp = RegExpUtils.NET_QoS_PATTERN)
		protected String outbound;

		public String get_interface() {
			return _interface;
		}

		public void set_interface(String _interface) {
			this._interface = _interface;
		}

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public String getInbound() {
			return inbound;
		}

		public void setInbound(String inbound) {
			this.inbound = inbound;
		}

		public String getOutbound() {
			return outbound;
		}

		public void setOutbound(String outbound) {
			this.outbound = outbound;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ResizeMaxRAM extends ResizeRAM {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class SetBootOrder {

		@ParameterDescriber(required = true, description = "虚拟机启动顺序，从光盘或者系统盘启动，启动顺序用逗号分隔，对于开机虚拟机重启后生效", constraint = "取值范围：vdX, hdX, sdX", example = "hda,vda")
		protected String order;

		public String getOrder() {
			return order;
		}

		public void setOrder(String order) {
			this.order = order;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class SetVncPassword {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "强制执行", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean force;

		@ParameterDescriber(required = true, description = "虚拟机终端密码", constraint = "取值范围：密码为4-16位，是小写字母、数字和中划线组合", example = "abcdefg")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getPersistent() {
			return persistent;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getForce() {
			return force;
		}

		public void setForce(Boolean force) {
			this.force = force;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
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
	public static class UnsetVncPassword {

		@ParameterDescriber(required = false, description = "对当前虚拟机生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean current;

		@ParameterDescriber(required = false, description = "对配置进行持久化", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean persistent;

		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;

		@ParameterDescriber(required = false, description = "如果不设置，当前配置下次不会生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean config;

		@ParameterDescriber(required = false, description = "强制执行", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean force;

		public Boolean getCurrent() {
			return current;
		}

		public void setCurrent(Boolean current) {
			this.current = current;
		}

		public Boolean getPersistent() {
			return persistent;
		}

		public void setPersistent(Boolean persistent) {
			this.persistent = persistent;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

		public Boolean getConfig() {
			return config;
		}

		public void setConfig(Boolean config) {
			this.config = config;
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
	public static class UpdateGraphic {

		@ParameterDescriber(required = false, description = "修改虚拟机终端密码，运行虚拟机重启后生效", constraint = "取值范围：密码为4-16位，是小写字母、数字和中划线组合", example = "abcdefg")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;
		
		@ParameterDescriber(required = false, description = "取消虚拟机终端密码，运行虚拟机重启后生效", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean no_password;
		
		@ParameterDescriber(required = true, description = "修改虚拟机终端类型，运行虚拟机重启后生效", constraint = "取值范围：vnc/spice", example = "spice")
		@Pattern(regexp = RegExpUtils.GRAPHICS_TYPE)
		protected String type;

		public Boolean getNo_password() {
			return no_password;
		}

		public void setNo_password(Boolean no_password) {
			this.no_password = no_password;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
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
	public static class SetGuestPassword {

		@ParameterDescriber(required = true, description = "虚拟机操作系统类型", constraint = "取值范围：windows/linux", example = "linux")
		@Pattern(regexp = RegExpUtils.VM_AGENT_OS_TYPE_PATTERN)
		protected String os_type;

		@ParameterDescriber(required = true, description = "虚拟机登录用户", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "root")
		protected String user;

		@ParameterDescriber(required = true, description = "虚拟机密码", constraint = "取值范围：密码为4-16位，是小写字母、数字和中划线组合", example = "abcdefg")
		@Pattern(regexp = RegExpUtils.PASSWORD_PATTERN)
		protected String password;

		public String getOs_type() {
			return os_type;
		}

		public void setOs_type(String os_type) {
			this.os_type = os_type;
		}

		public String getUser() {
			return user;
		}

		public void setUser(String user) {
			this.user = user;
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
	public static class InjectSshKey {

		@ParameterDescriber(required = true, description = "虚拟机操作系统类型", constraint = "取值范围：windows/linux", example = "linux")
		@Pattern(regexp = RegExpUtils.VM_AGENT_OS_TYPE_PATTERN)
		protected String os_type;

		@ParameterDescriber(required = true, description = "虚拟机登录用户", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "root")
		protected String user;

		@ParameterDescriber(required = true, description = "ssh登录公钥", constraint = "取值范围：只允许数字、大小写字母、空格、-+/@", example = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9kyC1EUvxppNqYSr8mh8GIC9VBk0IdL7t+Y4dp5vcyKO+Qtx4W9mRdQ8aPuEVAxSfjDsbpfyW1O/cPUbCJJZR9Gg9FYL63V8Q97UN3V4i/ILUMTazF+MfN82ln80PQhCv0SQwfx9qsAmhmVvukPDESr2i2TO93SiY15dh1niX8AeptfXfAZWg+zJA5gIdov1u88IE1xIPjhytUCnGPJNW0kvqJzRsCSzDY7puYXO7mWRuDYpHV7VZp0qYX9urrQB+YPzIP3UBC6VbhpapRLtir8whzFCu0MKTXjzzE7h++DiTaqLMtQIfuXHKgMTA39wnQPuqnf7Q/hbm9qYMCauf root@node22")
		protected String ssh_key;

		public String getSsh_key() {
			return ssh_key;
		}

		public void setSsh_key(String ssh_key) {
			this.ssh_key = ssh_key;
		}

		public String getOs_type() {
			return os_type;
		}

		public void setOs_type(String os_type) {
			this.os_type = os_type;
		}

		public String getUser() {
			return user;
		}

		public void setUser(String user) {
			this.user = user;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class BindFloatingIP {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "switch11")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "外部交换机名", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "switch11")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String outSwName;

		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String vmmac;

		@ParameterDescriber(required = true, description = "外网IP，以及子网掩码", constraint = "x.x.x.x,x取值范围0到255", example = "192.168.5.2/24")
		@Pattern(regexp = RegExpUtils.SUBNET_PATTERN)
		protected String fip;

		public String getVmmac() {
			return vmmac;
		}

		public void setVmmac(String vmmac) {
			this.vmmac = vmmac;
		}

		public String getFip() {
			return fip;
		}

		public void setFip(String fip) {
			this.fip = fip;
		}

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getOutSwName() {
			return outSwName;
		}

		public void setOutSwName(String outSwName) {
			this.outSwName = outSwName;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class UnbindFloatingIP {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "switch11")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "虚拟机mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String vmmac;

		@ParameterDescriber(required = true, description = "外网IP", constraint = "x.x.x.x,x取值范围0到255", example = "192.168.5.2")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String fip;

		@ParameterDescriber(required = true, description = "虚拟机IP", constraint = "x.x.x.x,x取值范围0到255", example = "192.168.5.2")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String vmip;

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getVmmac() {
			return vmmac;
		}

		public void setVmmac(String vmmac) {
			this.vmmac = vmmac;
		}

		public String getFip() {
			return fip;
		}

		public void setFip(String fip) {
			this.fip = fip;
		}

		public String getVmip() {
			return vmip;
		}

		public void setVmip(String vmip) {
			this.vmip = vmip;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class AddACL {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "switch11")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "虚拟机mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String vmmac;

		@ParameterDescriber(required = true, description = "ACL类型", constraint = "from或者to", example = "from")
		@Pattern(regexp = RegExpUtils.ACL_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = true, description = "ACL规则", constraint = "&&连接两个规则，注意src和dst后==前后必须有一个空格", example = "ip4.src == $dmz && tcp.dst == 3306")
		@Pattern(regexp = RegExpUtils.RULE_PATTERN)
		protected String rule;

		@ParameterDescriber(required = true, description = "ACL操作", constraint = "allow或者drop", example = "allow")
		@Pattern(regexp = RegExpUtils.ACL_OPERATOR_PATTERN)
		protected String operator;

		@ParameterDescriber(required = false, description = "优先级", constraint = "1-999", example = "1")
		@Pattern(regexp = RegExpUtils.ACL_PRIORITY_PATTERN)
		protected String priority;

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getVmmac() {
			return vmmac;
		}

		public void setVmmac(String vmmac) {
			this.vmmac = vmmac;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getRule() {
			return rule;
		}

		public void setRule(String rule) {
			this.rule = rule;
		}

		public String getOperator() {
			return operator;
		}

		public void setOperator(String operator) {
			this.operator = operator;
		}

		public String getPriority() {
			return priority;
		}

		public void setPriority(String priority) {
			this.priority = priority;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ModifyACL extends AddACL {

	}

	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class BatchDeprecatedACL {
		
		protected List<DeprecatedACL> deprecatedACLs;

		public List<DeprecatedACL> getDeprecatedACLs() {
			return deprecatedACLs;
		}

		public void setDeprecatedACLs(List<DeprecatedACL> deprecatedACLs) {
			this.deprecatedACLs = deprecatedACLs;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeprecatedACL {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "名称是字符串类型，长度是4到100位，只允许数字、小写字母、中划线、以及圆点", example = "switch11")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "虚拟机mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String vmmac;

		@ParameterDescriber(required = false, description = "ACL类型", constraint = "from或者to", example = "from")
		@Pattern(regexp = RegExpUtils.ACL_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = false, description = "ACL规则", constraint = "&&连接两个规则，注意src和dst后==前后必须有一个空格", example = "ip4.src == $dmz && tcp.dst == 3306")
		@Pattern(regexp = RegExpUtils.RULE_PATTERN)
		protected String rule;

		@ParameterDescriber(required = false, description = "优先级", constraint = "1-999", example = "1")
		@Pattern(regexp = RegExpUtils.ACL_PRIORITY_PATTERN)
		protected String priority;

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getVmmac() {
			return vmmac;
		}

		public void setVmmac(String vmmac) {
			this.vmmac = vmmac;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getRule() {
			return rule;
		}

		public void setRule(String rule) {
			this.rule = rule;
		}

		public String getPriority() {
			return priority;
		}

		public void setPriority(String priority) {
			this.priority = priority;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class SetQoS {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "交换机名", example = "switch1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "QoS类型", constraint = "from或者to", example = "from")
		@Pattern(regexp = RegExpUtils.QOS_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = true, description = "协议类型", constraint = "只能是ip, ip4, icmp之类", example = "ip")
		@Pattern(regexp = RegExpUtils.RULE_PATTERN)
		protected String rule;

		@ParameterDescriber(required = true, description = "带宽速度", constraint = "单位是kbps, 0-1000Mbps", example = "10000")
		@Pattern(regexp = RegExpUtils.RATE_PATTERN)
		protected String rate;

		@ParameterDescriber(required = true, description = "带宽波动", constraint = "单位是kbps, 0-100Mbps", example = "100")
		@Pattern(regexp = RegExpUtils.BURST_PATTERN)
		protected String burst;

		@ParameterDescriber(required = false, description = "优先级", constraint = "0-32767", example = "2")
		@Pattern(regexp = RegExpUtils.QOS_PRIORITY_PATTERN)
		protected String priority;

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getRule() {
			return rule;
		}

		public void setRule(String rule) {
			this.rule = rule;
		}

		public String getRate() {
			return rate;
		}

		public void setRate(String rate) {
			this.rate = rate;
		}

		public String getBurst() {
			return burst;
		}

		public void setBurst(String burst) {
			this.burst = burst;
		}

		public String getPriority() {
			return priority;
		}

		public void setPriority(String priority) {
			this.priority = priority;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ModifyQoS extends SetQoS {

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class UnsetQoS {

		@ParameterDescriber(required = true, description = "交换机名", constraint = "交换机名", example = "switch1")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String swName;

		@ParameterDescriber(required = true, description = "QoS类型", constraint = "from或者to", example = "from")
		@Pattern(regexp = RegExpUtils.QOS_TYPE_PATTERN)
		protected String type;

		@ParameterDescriber(required = true, description = "协议类型", constraint = "只能是ip, ip4, icmp之类", example = "ip")
		@Pattern(regexp = RegExpUtils.RULE_PATTERN)
		protected String rule;

		@ParameterDescriber(required = true, description = "优先级", constraint = "0-32767", example = "2")
		@Pattern(regexp = RegExpUtils.QOS_PRIORITY_PATTERN)
		protected String priority;
		
		@ParameterDescriber(required = true, description = "mac地址", constraint = "虚拟机的mac地址", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String vmmac;

		public String getVmmac() {
			return vmmac;
		}

		public void setVmmac(String vmmac) {
			this.vmmac = vmmac;
		}

		public String getSwName() {
			return swName;
		}

		public void setSwName(String swName) {
			this.swName = swName;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}

		public String getRule() {
			return rule;
		}

		public void setRule(String rule) {
			this.rule = rule;
		}

		public String getPriority() {
			return priority;
		}

		public void setPriority(String priority) {
			this.priority = priority;
		}

	}


	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ExportVM {

		@ParameterDescriber(required = true, description = "导出文件保存的路径", constraint = "/root", example = "from")
		@Pattern(regexp = RegExpUtils.LINUX_PATH_PATTERN)
		protected String path;

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class BackupVM {
		@ParameterDescriber(required = true, description = "备份主机使用的存储池", constraint = "备份主机使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

		@ParameterDescriber(required = false, description = "备份虚拟机所有的盘，否则只备份系统盘，需要注意的是恢复带有数据云盘的记录时，数据云盘必须还挂载在该虚拟机上",
				constraint = "备份虚拟机所有的盘，否则只备份系统盘，需要注意的是恢复带有数据云盘的记录时，数据云盘必须还挂载在该虚拟机上", example = "true")
		protected boolean all;

		@ParameterDescriber(required = false, description = "全量备份",
				constraint = "全量备份", example = "true")
		protected boolean full;

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

		public boolean getFull() {
			return full;
		}

		public void setFull(boolean full) {
			this.full = full;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RestoreVM {
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
		@ParameterDescriber(required = true, description = "备份主机使用的存储池", constraint = "备份主机使用的存储池", example = "61024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String pool;

		@ParameterDescriber(required = true, description = "备份记录的版本号", constraint = "备份记录的版本号", example = "13024b305b5c463b80bceee066077079")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String version;

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
	public static class PassthroughDevice {
		
		@ParameterDescriber(required = true, description = "执行的操作", constraint = "添加或删除：add/remove", example = "add")
		@Pattern(regexp = RegExpUtils.DEVICE_PASSTHROUGH_ACTION)
		protected String action;
		
		@ParameterDescriber(required = true, description = "物理主机上的bus号，例如01:00.0中的01", constraint = "用lsusb/lspci命令查询的bus号", example = "01")
		protected String bus_num;
		
		@ParameterDescriber(required = true, description = "（仅影响PCI设备）物理主机上的副bus号，例如01:00.0中的00", constraint = "用lsusb/lspci命令查询的副bus号", example = "00")
		protected String sub_bus_num;
		
		@ParameterDescriber(required = true, description = "物理主机上的设备号，例如01:00.0中的0", constraint = "用lsusb/lspci命令查询的device号", example = "0")
		protected String dev_num;
		
		@ParameterDescriber(required = false, description = "立即生效，对于开机虚拟机", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean live;
		
		@ParameterDescriber(required = true, description = "设备的类型", constraint = "取值范围：usb/pci", example = "pci")
		@Pattern(regexp = RegExpUtils.DEVICE_PASSTHROUGH_DEV_TYPE)
		protected String dev_type;

		public String getSub_bus_num() {
			return sub_bus_num;
		}

		public void setSub_bus_num(String sub_bus_num) {
			this.sub_bus_num = sub_bus_num;
		}

		public String getDev_type() {
			return dev_type;
		}

		public void setDev_type(String dev_type) {
			this.dev_type = dev_type;
		}

		public String getAction() {
			return action;
		}

		public void setAction(String action) {
			this.action = action;
		}

		public String getBus_num() {
			return bus_num;
		}

		public void setBus_num(String bus_num) {
			this.bus_num = bus_num;
		}

		public String getDev_num() {
			return dev_num;
		}

		public void setDev_num(String dev_num) {
			this.dev_num = dev_num;
		}

		public Boolean getLive() {
			return live;
		}

		public void setLive(Boolean live) {
			this.live = live;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RedirectUsb {
		
		@ParameterDescriber(required = true, description = "执行的操作，对于开机虚拟机重启后生效", constraint = "开启或关闭：on/off", example = "on")
		@Pattern(regexp = RegExpUtils.USB_REDIRECT_ACTION)
		protected String action;
		
		@ParameterDescriber(required = false, description = "开启usb透传时，设置虚拟机可透传的usb个数，默认4个", constraint = "取值范围：0~8", example = "4")
		@Pattern(regexp = RegExpUtils.USB_REDIRECT_NUMBER)
		protected String number;

		public String getAction() {
			return action;
		}

		public void setAction(String action) {
			this.action = action;
		}

		public String getNumber() {
			return number;
		}

		public void setNumber(String number) {
			this.number = number;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class AutoStartVM {
		
		@ParameterDescriber(required = false, description = "取消虚拟机高可用", constraint = AnnotationUtils.DESC_BOOLEAN, example = "true")
		protected Boolean disable;

		public Boolean getDisable() {
			return disable;
		}

		public void setDisable(Boolean disable) {
			this.disable = disable;
		}

	}
	
}
