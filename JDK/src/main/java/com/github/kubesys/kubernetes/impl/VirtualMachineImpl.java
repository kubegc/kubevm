/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.impl;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.regex.Pattern;

import com.github.kubesys.kubernetes.ExtendedKubernetesConstants;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineList;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSpec;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.AddACL;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.AutoStartVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.BackupVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.BatchDeprecatedACL;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.BindFloatingIP;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ChangeNumberOfCPU;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CloneVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ConvertVMToImage;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromImage;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeleteVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeprecatedACL;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.EjectISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ExportVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.InjectSshKey;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.InsertISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ManageISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.MigrateVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.MigrateVMDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ModifyACL;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ModifyQoS;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.PassthroughDevice;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.PlugDevice;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.PlugDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.PlugNIC;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.RebootVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.RedirectUsb;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResetVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResizeMaxRAM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResizeRAM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResizeVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.ResumeVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.SetBootOrder;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.SetGuestPassword;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.SetQoS;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.SetVncPassword;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StartVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StopVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.StopVMForce;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.SuspendVM;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.TuneDiskQoS;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.TuneNICQoS;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnbindFloatingIP;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnplugDevice;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnplugDisk;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnplugNIC;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnsetQoS;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnsetVncPassword;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UpdateGraphic;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UpdateOS;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/1
 **/
@SuppressWarnings("deprecation")
public class VirtualMachineImpl extends AbstractImpl<VirtualMachine, VirtualMachineList, VirtualMachineSpec> {


	@Override
	public VirtualMachine getModel() {
		return new VirtualMachine();
	}

	@Override
	public VirtualMachineSpec getSpec() {
		return new VirtualMachineSpec();
	}

	@Override
	public Object getLifecycle() {
		return new Lifecycle();
	}

	@Override
	public VirtualMachineSpec getSpec(VirtualMachine r) {
		return r.getSpec();
	}

	/**
	 * @param name  name
	 * @throws Exception exception
	 */
	public boolean setHA(String name) throws Exception {
		return this.addTag(name, ExtendedKubernetesConstants.LABEL_VM_HA, String.valueOf(true));
	}
	
	/**
	 * @param name  name
	 * @param labels  map <now just support zone and cluster>
	 * @throws Exception exception
	 */
	public boolean setHA(String name, Map<String, String>  labels) throws Exception {
		Map<String, String> tags = new HashMap<String, String>();
		tags.put(ExtendedKubernetesConstants.LABEL_VM_HA, "true");
		tags.putAll(labels);
		return this.addTags(name, labels);
	}
	
	/**
	 * @param name  name
	 * @throws Exception exception
	 */
	public boolean unsetHA(String name) throws Exception {
		return deleteTag(name, ExtendedKubernetesConstants.LABEL_VM_HA);
	}
	
	/**
	 * @param name  name
	 * @param keys  list   
	 * @throws Exception exception
	 */
	public boolean unsetHA(String name, List<String>  keys) throws Exception {
		List<String> tags = new ArrayList<String>();
		tags.add(ExtendedKubernetesConstants.LABEL_VM_HA);
		tags.addAll(keys);
		return deleteTags(name, tags);
	}
	
	public boolean startVMWithPower(String name, String nodeName, StartVM startVM, String power) throws Exception {
		updateHostAndPower(name, nodeName, power);
		return startVM(name, startVM, null);
	}
	
	/*************************************************
	 * 
	 * Generated by <code>MethodGenerator<code>
	 * 
	 **************************************************/
	public boolean createAndStartVMFromISO(String name, CreateAndStartVMFromISO createAndStartVMFromISO) throws Exception {
		return createAndStartVMFromISO(name, null, createAndStartVMFromISO, null);
	}

	public boolean createAndStartVMFromISO(String name, String nodeName, CreateAndStartVMFromISO createAndStartVMFromISO) throws Exception {
		return createAndStartVMFromISO(name, nodeName, createAndStartVMFromISO, null);
	}

	public boolean createAndStartVMFromISO(String name, CreateAndStartVMFromISO createAndStartVMFromISO, String eventId) throws Exception {
		return createAndStartVMFromISO(name, null, createAndStartVMFromISO, eventId);
	}

	public boolean createAndStartVMFromISO(String name, String nodeName,CreateAndStartVMFromISO createAndStartVMFromISO, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return create(getModel(), createMetadata(name, nodeName, eventId), 
				createSpec(nodeName, createLifecycle(createAndStartVMFromISO)));
	}

	public boolean createAndStartVMFromImage(String name, CreateAndStartVMFromImage createAndStartVMFromImage) throws Exception {
		return createAndStartVMFromImage(name, null, createAndStartVMFromImage, null);
	}

	public boolean createAndStartVMFromImage(String name, String nodeName, CreateAndStartVMFromImage createAndStartVMFromImage) throws Exception {
		return createAndStartVMFromImage(name, nodeName, createAndStartVMFromImage, null);
	}

	public boolean createAndStartVMFromImage(String name, CreateAndStartVMFromImage createAndStartVMFromImage, String eventId) throws Exception {
		return createAndStartVMFromImage(name, null, createAndStartVMFromImage, eventId);
	}

	public boolean createAndStartVMFromImage(String name, String nodeName,CreateAndStartVMFromImage createAndStartVMFromImage, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return create(getModel(), createMetadata(name, nodeName, eventId), 
				createSpec(nodeName, createLifecycle(createAndStartVMFromImage)));
	}

	public boolean suspendVM(String name, SuspendVM suspendVM) throws Exception {
		return suspendVM(name, suspendVM, null);
	}

	public boolean suspendVM(String name, SuspendVM suspendVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), suspendVM);
	}

	public boolean suspendVM(String name, String nodeName, SuspendVM suspendVM) throws Exception {
		updateHost(name, nodeName);
		return suspendVM(name, suspendVM, null);
	}

	public boolean suspendVM(String name, String nodeName, SuspendVM suspendVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return suspendVM(name, suspendVM, eventId);
	}

	public boolean stopVMForce(String name, StopVMForce stopVMForce) throws Exception {
		return stopVMForce(name, stopVMForce, null);
	}

	public boolean stopVMForce(String name, StopVMForce stopVMForce, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), stopVMForce);
	}

	public boolean stopVMForce(String name, String nodeName, StopVMForce stopVMForce) throws Exception {
		updateHost(name, nodeName);
		return stopVMForce(name, stopVMForce, null);
	}

	public boolean stopVMForce(String name, String nodeName, StopVMForce stopVMForce, String eventId) throws Exception {
		updateHost(name, nodeName);
		return stopVMForce(name, stopVMForce, eventId);
	}

	public boolean unplugDevice(String name, UnplugDevice unplugDevice) throws Exception {
		return unplugDevice(name, unplugDevice, null);
	}

	public boolean unplugDevice(String name, UnplugDevice unplugDevice, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unplugDevice);
	}

	public boolean unplugDevice(String name, String nodeName, UnplugDevice unplugDevice) throws Exception {
		updateHost(name, nodeName);
		return unplugDevice(name, unplugDevice, null);
	}

	public boolean unplugDevice(String name, String nodeName, UnplugDevice unplugDevice, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unplugDevice(name, unplugDevice, eventId);
	}

	public boolean unplugNIC(String name, UnplugNIC unplugNIC) throws Exception {
		return unplugNIC(name, unplugNIC, null);
	}

	public boolean unplugNIC(String name, UnplugNIC unplugNIC, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unplugNIC);
	}

	public boolean unplugNIC(String name, String nodeName, UnplugNIC unplugNIC) throws Exception {
		updateHost(name, nodeName);
		return unplugNIC(name, unplugNIC, null);
	}

	public boolean unplugNIC(String name, String nodeName, UnplugNIC unplugNIC, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unplugNIC(name, unplugNIC, eventId);
	}

	public boolean migrateVM(String name, MigrateVM migrateVM) throws Exception {
		return migrateVM(name, migrateVM, null);
	}

	public boolean migrateVM(String name, MigrateVM migrateVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), migrateVM);
	}

	public boolean migrateVM(String name, String nodeName, MigrateVM migrateVM) throws Exception {
		updateHost(name, nodeName);
		return migrateVM(name, migrateVM, null);
	}

	public boolean migrateVM(String name, String nodeName, MigrateVM migrateVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return migrateVM(name, migrateVM, eventId);
	}

	public boolean migrateVMDisk(String name, MigrateVMDisk migrateVMDisk) throws Exception {
		return migrateVMDisk(name, migrateVMDisk, null);
	}

	public boolean migrateVMDisk(String name, MigrateVMDisk migrateVMDisk, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), migrateVMDisk);
	}

	public boolean migrateVMDisk(String name, String nodeName, MigrateVMDisk migrateVMDisk) throws Exception {
		updateHost(name, nodeName);
		return migrateVMDisk(name, migrateVMDisk, null);
	}

	public boolean migrateVMDisk(String name, String nodeName, MigrateVMDisk migrateVMDisk, String eventId) throws Exception {
		updateHost(name, nodeName);
		return migrateVMDisk(name, migrateVMDisk, eventId);
	}

	public boolean changeNumberOfCPU(String name, ChangeNumberOfCPU changeNumberOfCPU) throws Exception {
		return changeNumberOfCPU(name, changeNumberOfCPU, null);
	}

	public boolean changeNumberOfCPU(String name, ChangeNumberOfCPU changeNumberOfCPU, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), changeNumberOfCPU);
	}

	public boolean changeNumberOfCPU(String name, String nodeName, ChangeNumberOfCPU changeNumberOfCPU) throws Exception {
		updateHost(name, nodeName);
		return changeNumberOfCPU(name, changeNumberOfCPU, null);
	}

	public boolean changeNumberOfCPU(String name, String nodeName, ChangeNumberOfCPU changeNumberOfCPU, String eventId) throws Exception {
		updateHost(name, nodeName);
		return changeNumberOfCPU(name, changeNumberOfCPU, eventId);
	}

	public boolean resumeVM(String name, ResumeVM resumeVM) throws Exception {
		return resumeVM(name, resumeVM, null);
	}

	public boolean resumeVM(String name, ResumeVM resumeVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), resumeVM);
	}

	public boolean resumeVM(String name, String nodeName, ResumeVM resumeVM) throws Exception {
		updateHost(name, nodeName);
		return resumeVM(name, resumeVM, null);
	}

	public boolean resumeVM(String name, String nodeName, ResumeVM resumeVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return resumeVM(name, resumeVM, eventId);
	}

	public boolean plugDisk(String name, PlugDisk plugDisk) throws Exception {
		return plugDisk(name, plugDisk, null);
	}

	public boolean plugDisk(String name, PlugDisk plugDisk, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), plugDisk);
	}

	public boolean plugDisk(String name, String nodeName, PlugDisk plugDisk) throws Exception {
		updateHost(name, nodeName);
		return plugDisk(name, plugDisk, null);
	}

	public boolean plugDisk(String name, String nodeName, PlugDisk plugDisk, String eventId) throws Exception {
		updateHost(name, nodeName);
		return plugDisk(name, plugDisk, eventId);
	}

	public boolean plugDevice(String name, PlugDevice plugDevice) throws Exception {
		return plugDevice(name, plugDevice, null);
	}

	public boolean plugDevice(String name, PlugDevice plugDevice, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), plugDevice);
	}

	public boolean plugDevice(String name, String nodeName, PlugDevice plugDevice) throws Exception {
		updateHost(name, nodeName);
		return plugDevice(name, plugDevice, null);
	}

	public boolean plugDevice(String name, String nodeName, PlugDevice plugDevice, String eventId) throws Exception {
		updateHost(name, nodeName);
		return plugDevice(name, plugDevice, eventId);
	}

	public boolean resetVM(String name, ResetVM resetVM) throws Exception {
		return resetVM(name, resetVM, null);
	}

	public boolean resetVM(String name, ResetVM resetVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), resetVM);
	}

	public boolean resetVM(String name, String nodeName, ResetVM resetVM) throws Exception {
		updateHost(name, nodeName);
		return resetVM(name, resetVM, null);
	}

	public boolean resetVM(String name, String nodeName, ResetVM resetVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return resetVM(name, resetVM, eventId);
	}

	public boolean unplugDisk(String name, UnplugDisk unplugDisk) throws Exception {
		return unplugDisk(name, unplugDisk, null);
	}

	public boolean unplugDisk(String name, UnplugDisk unplugDisk, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unplugDisk);
	}

	public boolean unplugDisk(String name, String nodeName, UnplugDisk unplugDisk) throws Exception {
		updateHost(name, nodeName);
		return unplugDisk(name, unplugDisk, null);
	}

	public boolean unplugDisk(String name, String nodeName, UnplugDisk unplugDisk, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unplugDisk(name, unplugDisk, eventId);
	}

	public boolean stopVM(String name, StopVM stopVM) throws Exception {
		return stopVM(name, stopVM, null);
	}

	public boolean stopVM(String name, StopVM stopVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), stopVM);
	}

	public boolean stopVM(String name, String nodeName, StopVM stopVM) throws Exception {
		updateHost(name, nodeName);
		return stopVM(name, stopVM, null);
	}

	public boolean stopVM(String name, String nodeName, StopVM stopVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return stopVM(name, stopVM, eventId);
	}

	public boolean startVM(String name, StartVM startVM) throws Exception {
		return startVM(name, startVM, null);
	}

	public boolean startVM(String name, StartVM startVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), startVM);
	}

	public boolean startVM(String name, String nodeName, StartVM startVM) throws Exception {
		updateHost(name, nodeName);
		return startVM(name, startVM, null);
	}

	public boolean startVM(String name, String nodeName, StartVM startVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return startVM(name, startVM, eventId);
	}

	public boolean deleteVM(String name, DeleteVM deleteVM) throws Exception {
		return deleteVM(name, deleteVM, null);
	}

	public boolean deleteVM(String name, DeleteVM deleteVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), deleteVM);
	}

	public boolean deleteVM(String name, String nodeName, DeleteVM deleteVM) throws Exception {
		updateHost(name, nodeName);
		return deleteVM(name, deleteVM, null);
	}

	public boolean deleteVM(String name, String nodeName, DeleteVM deleteVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return deleteVM(name, deleteVM, eventId);
	}

	public boolean rebootVM(String name, RebootVM rebootVM) throws Exception {
		return rebootVM(name, rebootVM, null);
	}

	public boolean rebootVM(String name, RebootVM rebootVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), rebootVM);
	}

	public boolean rebootVM(String name, String nodeName, RebootVM rebootVM) throws Exception {
		updateHost(name, nodeName);
		return rebootVM(name, rebootVM, null);
	}

	public boolean rebootVM(String name, String nodeName, RebootVM rebootVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return rebootVM(name, rebootVM, eventId);
	}

	public boolean plugNIC(String name, PlugNIC plugNIC) throws Exception {
		return plugNIC(name, plugNIC, null);
	}

	public boolean plugNIC(String name, PlugNIC plugNIC, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), plugNIC);
	}

	public boolean plugNIC(String name, String nodeName, PlugNIC plugNIC) throws Exception {
		updateHost(name, nodeName);
		return plugNIC(name, plugNIC, null);
	}

	public boolean plugNIC(String name, String nodeName, PlugNIC plugNIC, String eventId) throws Exception {
		updateHost(name, nodeName);
		return plugNIC(name, plugNIC, eventId);
	}

	public boolean manageISO(String name, ManageISO manageISO) throws Exception {
		return manageISO(name, manageISO, null);
	}

	public boolean manageISO(String name, ManageISO manageISO, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), manageISO);
	}

	public boolean manageISO(String name, String nodeName, ManageISO manageISO) throws Exception {
		updateHost(name, nodeName);
		return manageISO(name, manageISO, null);
	}

	public boolean manageISO(String name, String nodeName, ManageISO manageISO, String eventId) throws Exception {
		updateHost(name, nodeName);
		return manageISO(name, manageISO, eventId);
	}

	public boolean updateOS(String name, UpdateOS updateOS) throws Exception {
		return updateOS(name, updateOS, null);
	}

	public boolean updateOS(String name, UpdateOS updateOS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), updateOS);
	}

	public boolean updateOS(String name, String nodeName, UpdateOS updateOS) throws Exception {
		updateHost(name, nodeName);
		return updateOS(name, updateOS, null);
	}

	public boolean updateOS(String name, String nodeName, UpdateOS updateOS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return updateOS(name, updateOS, eventId);
	}

	public boolean convertVMToImage(String name, ConvertVMToImage convertVMToImage) throws Exception {
		return convertVMToImage(name, convertVMToImage, null);
	}

	public boolean convertVMToImage(String name, ConvertVMToImage convertVMToImage, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), convertVMToImage);
	}

	public boolean convertVMToImage(String name, String nodeName, ConvertVMToImage convertVMToImage) throws Exception {
		updateHost(name, nodeName);
		return convertVMToImage(name, convertVMToImage, null);
	}

	public boolean convertVMToImage(String name, String nodeName, ConvertVMToImage convertVMToImage, String eventId) throws Exception {
		updateHost(name, nodeName);
		return convertVMToImage(name, convertVMToImage, eventId);
	}

	public boolean insertISO(String name, InsertISO insertISO) throws Exception {
		return insertISO(name, insertISO, null);
	}

	public boolean insertISO(String name, InsertISO insertISO, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), insertISO);
	}

	public boolean insertISO(String name, String nodeName, InsertISO insertISO) throws Exception {
		updateHost(name, nodeName);
		return insertISO(name, insertISO, null);
	}

	public boolean insertISO(String name, String nodeName, InsertISO insertISO, String eventId) throws Exception {
		updateHost(name, nodeName);
		return insertISO(name, insertISO, eventId);
	}

	public boolean ejectISO(String name, EjectISO ejectISO) throws Exception {
		return ejectISO(name, ejectISO, null);
	}

	public boolean ejectISO(String name, EjectISO ejectISO, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), ejectISO);
	}

	public boolean ejectISO(String name, String nodeName, EjectISO ejectISO) throws Exception {
		updateHost(name, nodeName);
		return ejectISO(name, ejectISO, null);
	}

	public boolean ejectISO(String name, String nodeName, EjectISO ejectISO, String eventId) throws Exception {
		updateHost(name, nodeName);
		return ejectISO(name, ejectISO, eventId);
	}

	public boolean resizeVM(String name, ResizeVM resizeVM) throws Exception {
		return resizeVM(name, resizeVM, null);
	}

	public boolean resizeVM(String name, ResizeVM resizeVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), resizeVM);
	}

	public boolean resizeVM(String name, String nodeName, ResizeVM resizeVM) throws Exception {
		updateHost(name, nodeName);
		return resizeVM(name, resizeVM, null);
	}

	public boolean resizeVM(String name, String nodeName, ResizeVM resizeVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return resizeVM(name, resizeVM, eventId);
	}

	public boolean cloneVM(String name, CloneVM cloneVM) throws Exception {
		return cloneVM(name, cloneVM, null);
	}

	public boolean cloneVM(String name, CloneVM cloneVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), cloneVM);
	}

	public boolean cloneVM(String name, String nodeName, CloneVM cloneVM) throws Exception {
		updateHost(name, nodeName);
		return cloneVM(name, cloneVM, null);
	}

	public boolean cloneVM(String name, String nodeName, CloneVM cloneVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return cloneVM(name, cloneVM, eventId);
	}

	public boolean tuneDiskQoS(String name, TuneDiskQoS tuneDiskQoS) throws Exception {
		return tuneDiskQoS(name, tuneDiskQoS, null);
	}

	public boolean tuneDiskQoS(String name, TuneDiskQoS tuneDiskQoS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), tuneDiskQoS);
	}

	public boolean tuneDiskQoS(String name, String nodeName, TuneDiskQoS tuneDiskQoS) throws Exception {
		updateHost(name, nodeName);
		return tuneDiskQoS(name, tuneDiskQoS, null);
	}

	public boolean tuneDiskQoS(String name, String nodeName, TuneDiskQoS tuneDiskQoS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return tuneDiskQoS(name, tuneDiskQoS, eventId);
	}

	public boolean tuneNICQoS(String name, TuneNICQoS tuneNICQoS) throws Exception {
		return tuneNICQoS(name, tuneNICQoS, null);
	}

	public boolean tuneNICQoS(String name, TuneNICQoS tuneNICQoS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), tuneNICQoS);
	}

	public boolean tuneNICQoS(String name, String nodeName, TuneNICQoS tuneNICQoS) throws Exception {
		updateHost(name, nodeName);
		return tuneNICQoS(name, tuneNICQoS, null);
	}

	public boolean tuneNICQoS(String name, String nodeName, TuneNICQoS tuneNICQoS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return tuneNICQoS(name, tuneNICQoS, eventId);
	}

	public boolean resizeMaxRAM(String name, ResizeMaxRAM resizeMaxRAM) throws Exception {
		return resizeMaxRAM(name, resizeMaxRAM, null);
	}

	public boolean resizeMaxRAM(String name, ResizeMaxRAM resizeMaxRAM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), resizeMaxRAM);
	}

	public boolean resizeMaxRAM(String name, String nodeName, ResizeMaxRAM resizeMaxRAM) throws Exception {
		updateHost(name, nodeName);
		return resizeMaxRAM(name, resizeMaxRAM, null);
	}

	public boolean resizeMaxRAM(String name, String nodeName, ResizeMaxRAM resizeMaxRAM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return resizeMaxRAM(name, resizeMaxRAM, eventId);
	}

	public boolean setBootOrder(String name, SetBootOrder setBootOrder) throws Exception {
		return setBootOrder(name, setBootOrder, null);
	}

	public boolean setBootOrder(String name, SetBootOrder setBootOrder, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), setBootOrder);
	}

	public boolean setBootOrder(String name, String nodeName, SetBootOrder setBootOrder) throws Exception {
		updateHost(name, nodeName);
		return setBootOrder(name, setBootOrder, null);
	}

	public boolean setBootOrder(String name, String nodeName, SetBootOrder setBootOrder, String eventId) throws Exception {
		updateHost(name, nodeName);
		return setBootOrder(name, setBootOrder, eventId);
	}

	public boolean setVncPassword(String name, SetVncPassword setVncPassword) throws Exception {
		return setVncPassword(name, setVncPassword, null);
	}

	public boolean setVncPassword(String name, SetVncPassword setVncPassword, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), setVncPassword);
	}

	public boolean setVncPassword(String name, String nodeName, SetVncPassword setVncPassword) throws Exception {
		updateHost(name, nodeName);
		return setVncPassword(name, setVncPassword, null);
	}

	public boolean setVncPassword(String name, String nodeName, SetVncPassword setVncPassword, String eventId) throws Exception {
		updateHost(name, nodeName);
		return setVncPassword(name, setVncPassword, eventId);
	}

	public boolean unsetVncPassword(String name, UnsetVncPassword unsetVncPassword) throws Exception {
		return unsetVncPassword(name, unsetVncPassword, null);
	}

	public boolean unsetVncPassword(String name, UnsetVncPassword unsetVncPassword, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unsetVncPassword);
	}

	public boolean unsetVncPassword(String name, String nodeName, UnsetVncPassword unsetVncPassword) throws Exception {
		updateHost(name, nodeName);
		return unsetVncPassword(name, unsetVncPassword, null);
	}

	public boolean unsetVncPassword(String name, String nodeName, UnsetVncPassword unsetVncPassword, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unsetVncPassword(name, unsetVncPassword, eventId);
	}

	public boolean setGuestPassword(String name, SetGuestPassword setGuestPassword) throws Exception {
		return setGuestPassword(name, setGuestPassword, null);
	}

	public boolean setGuestPassword(String name, SetGuestPassword setGuestPassword, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), setGuestPassword);
	}

	public boolean setGuestPassword(String name, String nodeName, SetGuestPassword setGuestPassword) throws Exception {
		updateHost(name, nodeName);
		return setGuestPassword(name, setGuestPassword, null);
	}

	public boolean setGuestPassword(String name, String nodeName, SetGuestPassword setGuestPassword, String eventId) throws Exception {
		updateHost(name, nodeName);
		return setGuestPassword(name, setGuestPassword, eventId);
	}

	public boolean injectSshKey(String name, InjectSshKey injectSshKey) throws Exception {
		return injectSshKey(name, injectSshKey, null);
	}

	public boolean injectSshKey(String name, InjectSshKey injectSshKey, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), injectSshKey);
	}

	public boolean injectSshKey(String name, String nodeName, InjectSshKey injectSshKey) throws Exception {
		updateHost(name, nodeName);
		return injectSshKey(name, injectSshKey, null);
	}

	public boolean injectSshKey(String name, String nodeName, InjectSshKey injectSshKey, String eventId) throws Exception {
		updateHost(name, nodeName);
		return injectSshKey(name, injectSshKey, eventId);
	}

	public boolean resizeRAM(String name, ResizeRAM resizeRAM) throws Exception {
		return resizeRAM(name, resizeRAM, null);
	}

	public boolean resizeRAM(String name, ResizeRAM resizeRAM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), resizeRAM);
	}

	public boolean resizeRAM(String name, String nodeName, ResizeRAM resizeRAM) throws Exception {
		updateHost(name, nodeName);
		return resizeRAM(name, resizeRAM, null);
	}

	public boolean resizeRAM(String name, String nodeName, ResizeRAM resizeRAM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return resizeRAM(name, resizeRAM, eventId);
	}

	public boolean bindFloatingIP(String name, BindFloatingIP bindFloatingIP) throws Exception {
		return bindFloatingIP(name, bindFloatingIP, null);
	}

	public boolean bindFloatingIP(String name, BindFloatingIP bindFloatingIP, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), bindFloatingIP);
	}

	public boolean bindFloatingIP(String name, String nodeName, BindFloatingIP bindFloatingIP) throws Exception {
		updateHost(name, nodeName);
		return bindFloatingIP(name, bindFloatingIP, null);
	}

	public boolean bindFloatingIP(String name, String nodeName, BindFloatingIP bindFloatingIP, String eventId) throws Exception {
		updateHost(name, nodeName);
		return bindFloatingIP(name, bindFloatingIP, eventId);
	}

	public boolean unbindFloatingIP(String name, UnbindFloatingIP unbindFloatingIP) throws Exception {
		return unbindFloatingIP(name, unbindFloatingIP, null);
	}

	public boolean unbindFloatingIP(String name, UnbindFloatingIP unbindFloatingIP, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unbindFloatingIP);
	}

	public boolean unbindFloatingIP(String name, String nodeName, UnbindFloatingIP unbindFloatingIP) throws Exception {
		updateHost(name, nodeName);
		return unbindFloatingIP(name, unbindFloatingIP, null);
	}

	public boolean unbindFloatingIP(String name, String nodeName, UnbindFloatingIP unbindFloatingIP, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unbindFloatingIP(name, unbindFloatingIP, eventId);
	}

	public boolean addACL(String name, AddACL addACL) throws Exception {
		return addACL(name, addACL, null);
	}

	public boolean addACL(String name, AddACL addACL, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), addACL);
	}

	public boolean addACL(String name, String nodeName, AddACL addACL) throws Exception {
		updateHost(name, nodeName);
		return addACL(name, addACL, null);
	}

	public boolean addACL(String name, String nodeName, AddACL addACL, String eventId) throws Exception {
		updateHost(name, nodeName);
		return addACL(name, addACL, eventId);
	}

	public boolean modifyACL(String name, ModifyACL modifyACL) throws Exception {
		return modifyACL(name, modifyACL, null);
	}

	public boolean modifyACL(String name, ModifyACL modifyACL, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), modifyACL);
	}

	public boolean modifyACL(String name, String nodeName, ModifyACL modifyACL) throws Exception {
		updateHost(name, nodeName);
		return modifyACL(name, modifyACL, null);
	}

	public boolean modifyACL(String name, String nodeName, ModifyACL modifyACL, String eventId) throws Exception {
		updateHost(name, nodeName);
		return modifyACL(name, modifyACL, eventId);
	}

	public boolean deprecatedACL(String name, DeprecatedACL deprecatedACL) throws Exception {
		return deprecatedACL(name, deprecatedACL, null);
	}

	public boolean deprecatedACL(String name, DeprecatedACL deprecatedACL, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), deprecatedACL);
	}

	public boolean deprecatedACL(String name, String nodeName, DeprecatedACL deprecatedACL) throws Exception {
		updateHost(name, nodeName);
		return deprecatedACL(name, deprecatedACL, null);
	}

	public boolean deprecatedACL(String name, String nodeName, DeprecatedACL deprecatedACL, String eventId) throws Exception {
		updateHost(name, nodeName);
		return deprecatedACL(name, deprecatedACL, eventId);
	}

	public boolean batchDeprecatedACL(String name, BatchDeprecatedACL batchDeprecatedACL) throws Exception {
		return batchDeprecatedACL(name, batchDeprecatedACL, null);
	}

	public boolean batchDeprecatedACL(String name, BatchDeprecatedACL batchDeprecatedACL, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), batchDeprecatedACL);
	}

	public boolean batchDeprecatedACL(String name, String nodeName, BatchDeprecatedACL batchDeprecatedACL) throws Exception {
		updateHost(name, nodeName);
		return batchDeprecatedACL(name, batchDeprecatedACL, null);
	}

	public boolean batchDeprecatedACL(String name, String nodeName, BatchDeprecatedACL batchDeprecatedACL, String eventId) throws Exception {
		updateHost(name, nodeName);
		return batchDeprecatedACL(name, batchDeprecatedACL, eventId);
	}

	public boolean setQoS(String name, SetQoS setQoS) throws Exception {
		return setQoS(name, setQoS, null);
	}

	public boolean setQoS(String name, SetQoS setQoS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), setQoS);
	}

	public boolean setQoS(String name, String nodeName, SetQoS setQoS) throws Exception {
		updateHost(name, nodeName);
		return setQoS(name, setQoS, null);
	}

	public boolean setQoS(String name, String nodeName, SetQoS setQoS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return setQoS(name, setQoS, eventId);
	}

	public boolean modifyQoS(String name, ModifyQoS modifyQoS) throws Exception {
		return modifyQoS(name, modifyQoS, null);
	}

	public boolean modifyQoS(String name, ModifyQoS modifyQoS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), modifyQoS);
	}

	public boolean modifyQoS(String name, String nodeName, ModifyQoS modifyQoS) throws Exception {
		updateHost(name, nodeName);
		return modifyQoS(name, modifyQoS, null);
	}

	public boolean modifyQoS(String name, String nodeName, ModifyQoS modifyQoS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return modifyQoS(name, modifyQoS, eventId);
	}

	public boolean unsetQoS(String name, UnsetQoS unsetQoS) throws Exception {
		return unsetQoS(name, unsetQoS, null);
	}

	public boolean unsetQoS(String name, UnsetQoS unsetQoS, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), unsetQoS);
	}

	public boolean unsetQoS(String name, String nodeName, UnsetQoS unsetQoS) throws Exception {
		updateHost(name, nodeName);
		return unsetQoS(name, unsetQoS, null);
	}

	public boolean unsetQoS(String name, String nodeName, UnsetQoS unsetQoS, String eventId) throws Exception {
		updateHost(name, nodeName);
		return unsetQoS(name, unsetQoS, eventId);
	}

	public boolean exportVM(String name, ExportVM exportVM) throws Exception {
		return exportVM(name, exportVM, null);
	}

	public boolean exportVM(String name, ExportVM exportVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), exportVM);
	}

	public boolean exportVM(String name, String nodeName, ExportVM exportVM) throws Exception {
		updateHost(name, nodeName);
		return exportVM(name, exportVM, null);
	}

	public boolean exportVM(String name, String nodeName, ExportVM exportVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return exportVM(name, exportVM, eventId);
	}

	public boolean backupVM(String name, BackupVM backupVM) throws Exception {
		return backupVM(name, backupVM, null);
	}

	public boolean backupVM(String name, BackupVM backupVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), backupVM);
	}

	public boolean backupVM(String name, String nodeName, BackupVM backupVM) throws Exception {
		updateHost(name, nodeName);
		return backupVM(name, backupVM, null);
	}

	public boolean backupVM(String name, String nodeName, BackupVM backupVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return backupVM(name, backupVM, eventId);
	}

	public boolean passthroughDevice(String name, PassthroughDevice passthroughDevice) throws Exception {
		return passthroughDevice(name, passthroughDevice, null);
	}

	public boolean passthroughDevice(String name, PassthroughDevice passthroughDevice, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), passthroughDevice);
	}

	public boolean passthroughDevice(String name, String nodeName, PassthroughDevice passthroughDevice) throws Exception {
		updateHost(name, nodeName);
		return passthroughDevice(name, passthroughDevice, null);
	}

	public boolean passthroughDevice(String name, String nodeName, PassthroughDevice passthroughDevice, String eventId) throws Exception {
		updateHost(name, nodeName);
		return passthroughDevice(name, passthroughDevice, eventId);
	}

	public boolean redirectUsb(String name, RedirectUsb redirectUsb) throws Exception {
		return redirectUsb(name, redirectUsb, null);
	}

	public boolean redirectUsb(String name, RedirectUsb redirectUsb, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), redirectUsb);
	}

	public boolean redirectUsb(String name, String nodeName, RedirectUsb redirectUsb) throws Exception {
		updateHost(name, nodeName);
		return redirectUsb(name, redirectUsb, null);
	}

	public boolean redirectUsb(String name, String nodeName, RedirectUsb redirectUsb, String eventId) throws Exception {
		updateHost(name, nodeName);
		return redirectUsb(name, redirectUsb, eventId);
	}

	public boolean updateGraphic(String name, UpdateGraphic updateGraphic) throws Exception {
		return updateGraphic(name, updateGraphic, null);
	}

	public boolean updateGraphic(String name, UpdateGraphic updateGraphic, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), updateGraphic);
	}

	public boolean updateGraphic(String name, String nodeName, UpdateGraphic updateGraphic) throws Exception {
		updateHost(name, nodeName);
		return updateGraphic(name, updateGraphic, null);
	}

	public boolean updateGraphic(String name, String nodeName, UpdateGraphic updateGraphic, String eventId) throws Exception {
		updateHost(name, nodeName);
		return updateGraphic(name, updateGraphic, eventId);
	}

	public boolean autoStartVM(String name, AutoStartVM autoStartVM) throws Exception {
		return autoStartVM(name, autoStartVM, null);
	}

	public boolean autoStartVM(String name, AutoStartVM autoStartVM, String eventId) throws Exception {
		Pattern pattern = Pattern.compile(RegExpUtils.NAME_PATTERN);
		if (!pattern.matcher(name).matches()) {
			throw new IllegalArgumentException("the length must be between 4 and 100, and it can only includes a-z, 0-9 and -.");
		}
		return update(name, updateMetadata(name, eventId), autoStartVM);
	}

	public boolean autoStartVM(String name, String nodeName, AutoStartVM autoStartVM) throws Exception {
		updateHost(name, nodeName);
		return autoStartVM(name, autoStartVM, null);
	}

	public boolean autoStartVM(String name, String nodeName, AutoStartVM autoStartVM, String eventId) throws Exception {
		updateHost(name, nodeName);
		return autoStartVM(name, autoStartVM, eventId);
	}

}