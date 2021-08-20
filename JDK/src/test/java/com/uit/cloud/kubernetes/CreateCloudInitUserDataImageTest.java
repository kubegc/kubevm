/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateCloudInitUserDataImage;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author wuyuewen@otcaix.iscas.ac.cn
 * @author liuhe@otcaix.iscas.ac.cn
 * 
 * @version 1.3.0
 * @since   2019/9/3
 *
 */
public class CreateCloudInitUserDataImageTest {
	
	
	public static void main(String[] args) throws Exception {

		ExtendedKubernetesClient client = AbstractTest.getClient();
		boolean successful = client.virtualMachineDisks()
				.createCloudInitUserDataImage("userdata1", "vm.node22", get(), "abc");
		System.out.println(successful);
	}

	protected static CreateCloudInitUserDataImage get() {
		CreateCloudInitUserDataImage createCloudInitUserDataImage = new CreateCloudInitUserDataImage();
		createCloudInitUserDataImage.setPool("migratepoolnodepool22");
		createCloudInitUserDataImage.setUserData("#cloud-config\r\n" +
				"hostname: ctest1\r\n" + 
				"fqdn: ctest1.example.com\r\n" + 
				"manage_etc_hosts: true\r\n" + 
				"users:\r\n" + 
				"  - name: centos\r\n" + 
				"    sudo: ALL=(ALL) NOPASSWD:ALL\r\n" + 
				"    groups: adm,sys\r\n" + 
				"    home: /home/centos\r\n" + 
				"    shell: /bin/bash\r\n" + 
				"    lock_passwd: false\r\n" + 
				"    ssh-authorized-keys:\r\n" + 
				"      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDB1nN/0qK/oh5RG2VunkOYIeQzKvJ3601gvuILoUbL0ZOGIXICV75fFR6byGwmXCuJiH4+GySJbCECDxaECPKutCU7FYAXNpSx2BWlgoxuQg9jGclyjcstKLiM3UJmRPUW6wQLZRpyJyiWjl9GDYTswCx1Ohj3VjWtZ/bDpM9U1eWKYKKx4qofESoY47J+5uFtmdEbkNkMOzNIUPIyhnuWlCB4YeMWyA2BmnKkmpErvocs/yTGt9j4rV4gU/epCW1311dE7AiDWz1CZCiLk55XkD2nlXJ/lqTk5+ZXRmsyuFex6hp5fq4P/URWcjp0qck9EmZMVY4ohs8/oZe8jyhbMyKr9xtzutZvujlapMhp3THjxv57nT0L5oLbORgFxF8pAXx6rpfgB7ggVkskCSMpRgi8oKQpY4N7EUdrUyxNlxS4EXxeAv/oWqhXNUmVakULvnh39sZcUzqHH1js+H1EV86dqilBpfRysts22AHPBiG82aVerHZyw//x0I/Jpx+4Hd7UZII75dM6+yfjyBAZTLx+p0t1bpwo9AkaW65U823n+qXsAm2mJHqt4cwxUS7JV25uMZ7kpRcmgIBa7xCfP3LbszYqjF5fQSlFd2fCUawlhEpg/7Ay2KGnEPydswbMfVCa5DR0+naCuZdTPs+qiZBYqpXr+Rc1IgdMdLOALQ== test1\r\n" + 
				"# only cert auth via ssh (console access can still login)\r\n" + 
				"ssh_pwauth: false\r\n" + 
				"disable_root: false\r\n" + 
				"chpasswd:\r\n" + 
				"  list: |\r\n" + 
				"     root:123456\r\n" + 
				"     centos:newpass123\r\n" + 
				"  expire: False\r\n" + 
				"packages:\r\n" + 
				"  - qemu-guest-agent\r\n" + 
				"  - bind-utils\r\n" + 
				"  - vim-enhanced\r\n" + 
				"\r\n" + 
				"# manually set BOOTPROTO for static IP\r\n" + 
				"# older cloud-config binary has bug?\r\n" + 
				"runcmd:\r\n" + 
				"    - [ sh, -c, 'sed -i s/BOOTPROTO=dhcp/BOOTPROTO=static/ /etc/sysconfig/network-scripts/ifcfg-eth0' ]\r\n" + 
				"    - [ sh, -c, 'ifdown eth0 && sleep 1 && ifup eth0 && sleep 1 && ip a' ]\r\n" + 
				"# written to /var/log/cloud-init.log, /var/log/messages\r\n" + 
				"final_message: \"The system is finally up, after $UPTIME seconds\"");
		return createCloudInitUserDataImage;
	}
}
