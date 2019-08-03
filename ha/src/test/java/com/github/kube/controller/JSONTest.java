package com.github.kube.controller;

import com.alibaba.fastjson.JSON;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.github.kubesys.kubernetes.api.model.VirtualMachine;
import com.github.kubesys.kubernetes.api.model.VirtualMachineSpec;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle;

/**
 * Unit test for simple App.
 */
public class JSONTest 
{
	
	public final static String CONFIG    = "/etc/kubernetes/admin.conf";
	
	public final static String NAME      = "virtualmachines.cloudplus.io";
	
    public static void main(String[] args) throws Exception {
    	
    	VirtualMachine vm =new VirtualMachine();
    	VirtualMachineSpec spec = new VirtualMachineSpec();
//    	Lifecycle lifecycle = new Lifecycle();
//    	Install install = new Install();
//    	install.set__vcpus("4");
//    	install.set__memory("1024");
//		lifecycle.setInstall(install );
//		spec.setLifecycle(lifecycle );
//		vm.setSpec(spec );
		
		System.out.println(JSON.toJSONString(vm));
    }  
}
