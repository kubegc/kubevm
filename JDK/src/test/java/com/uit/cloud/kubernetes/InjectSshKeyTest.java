/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.InjectSshKey;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.UnplugNIC;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class InjectSshKeyTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachines()
				.injectSshKey("wywtest", injectSshKey());
		System.out.println(successful);
	}
	
	public static InjectSshKey injectSshKey() {
		InjectSshKey injectSshKey = new InjectSshKey();
		injectSshKey.setOs_type("linux");
		injectSshKey.setUser("root");
		injectSshKey.setSsh_key("ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC9kyC1EUvxppNqYSr8mh8GIC9VBk0IdL7t+Y4dp5vcyKO+Qtx4W9mRdQ8aPuEVAxSfjDsbpfyW1O/cPUbCJJZR9Gg9FYL63V8Q97UN3V4i/ILUMTazF+MfN82ln80PQhCv0SQwfx9qsAmhmVvukPDESr2i2TO93SiY15dh1niX8AeptfXfAZWg+zJA5gIdov1u88IE1xIPjhytUCnGPJNW0kvqJzRsCSzDY7puYXO7mWRuDYpHV7VZp0qYX9urrQB+YPzIP3UBC6VbhpapRLtir8whzFCu0MKTXjzzE7h++DiTaqLMtQIfuXHKgMTA39wnQPuqnf7Q/hbm9qYMCauf root@node22");
		return injectSshKey;
	}
}
