/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.api.model.virtualmachinebackup.Backup;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Pool;
import io.fabric8.kubernetes.api.model.KubernetesResource;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/4
 **/
@JsonDeserialize(using = JsonDeserializer.None.class)
public class VirtualMachineBackupSpec extends ExtendedCustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 *
	 */
	private static final long serialVersionUID = -5135652468821098029L;


	protected Backup backup;

	protected Lifecycle lifecycle;

	public VirtualMachineBackupSpec() {

	}

	public Backup getBackup() {
		return backup;
	}

	public void setBackup(Backup backup) {
		this.backup = backup;
	}

	public Lifecycle getLifecycle() {
		return lifecycle;
	}

	public void setLifecycle(Lifecycle lifecycle) {
		this.lifecycle = lifecycle;
	}
}
