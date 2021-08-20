/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.annotations;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/4
 *
 * <p>
 * <code>ExtendedKubernetesClient<code> extends <code>DefaultKubernetesClient<code>
 * to provide the lifecycle of VirtualMachine, VirtualMachinePool, VirtualMachineDisk,
 * VirtualMachineImage, VirtualMachineSnapshot, VirtualMachineNetwork
 * 
 */
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface ParameterDescriber {

	boolean required();
	
	String description();
	
	String constraint();
	
	String example();
}
