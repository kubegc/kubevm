package com.uit.cloud.autotest;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.UUID;
import java.util.concurrent.CountDownLatch;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.CreateAndStartVMFromISO;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Lifecycle.DeleteVM;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.CreateDiskFromDiskImage;
import com.github.kubesys.kubernetes.api.model.virtualmachinedisk.Lifecycle.DeleteDisk;
import com.uit.cloud.kubernetes.AbstractTest;

import io.fabric8.kubernetes.api.model.Event;
import io.fabric8.kubernetes.client.KubernetesClientException;
import io.fabric8.kubernetes.client.Watcher;

public class ConcurrentTest {

	final static SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

	public static void main(String[] args) {
		// 模拟10人并发请求
		CountDownLatch latch = new CountDownLatch(1);
		// 模拟10个用户
		System.out.println("Start at " + sdf.format(new Date()));
		for (int i = 0; i < 20; i++) {
			String id = UUID.randomUUID().toString().replaceAll("-", "");
			AnalogUser analogUser = new AnalogUser("test" + i, id, "vm.node22", latch);
			analogUser.start();
		}
		// 计数器減一 所有线程释放 并发访问。
		latch.countDown();

	}

	static class AnalogUser extends Thread {
		// 模拟用户姓名
		String name;
		String id;
		String node;
		CountDownLatch latch;

		public AnalogUser(String name, String id, String node, CountDownLatch latch) {
			super();
			this.name = name;
			this.id = id;
			this.node = node;
			this.latch = latch;
		}

		@Override
		public void run() {
			// TODO Auto-generated method stub
			try {
				latch.await(); // 一直阻塞当前线程，直到计时器的值为0
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
			try {
				jobCreateDisk(); // 先创建云盘，再创建虚拟机，再删除虚拟机，再删除云盘
				jobEventHandler("createDiskFromDiskImage",this.id);
//				jobEventHandler("createAndStartVMFromISO",this.id);
//				jobEventHandler("deleteVM",this.id);
			} catch (Exception e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			
//			try {
//				jobDeleteVM(); // 先删除虚拟机，再删除云盘
//				jobDeleteDisk();
////				jobEventHandler("deleteVM",this.id);
//			} catch (Exception e) {
//				// TODO Auto-generated catch block
//				e.printStackTrace();
//			}

		}

		public void jobCreateDisk() throws Exception {

			ExtendedKubernetesClient client = AbstractTest.getClient();
			boolean successful = client.virtualMachineDisks().createDiskFromDiskImage("disk"+this.name, this.node,
					getCreateDiskFromDiskImage(), this.id);
			System.out.println(successful);

		}

		public void jobCreateVM() throws Exception {

			ExtendedKubernetesClient client = AbstractTest.getClient();
			// name
			boolean successful = client.virtualMachines().createAndStartVMFromISO("vm"+this.name, this.node,
					getCreateAndStartVMFromISO("disk"+this.name), this.id);
			System.out.println(successful);

		}

		public void jobDeleteVM() throws Exception {

			ExtendedKubernetesClient client = AbstractTest.getClient();
			boolean successful = client.virtualMachines().deleteVM("vm"+this.name, new DeleteVM(), this.id);
			System.out.println(successful);
		}
		
		public void jobDeleteDisk() throws Exception {

			ExtendedKubernetesClient client = AbstractTest.getClient();
			boolean successful = client.virtualMachineDisks()
					.deleteDisk("disk"+this.name, getDeleteDisk(), this.id);
			System.out.println(successful);
		}
		
		public void jobEventHandler(String eventType,String eventId) throws Exception {
			ExtendedKubernetesClient client = AbstractTest.getClient();
			client.events().withField("reason", eventType).watch(new Watcher<Event>() {

				@Override
				public void eventReceived(Action action, Event resource) {
					if (resource.getMessage().indexOf("eventId:" + eventId) != -1) {
						System.out.println("event " + action.name() + " " + resource.toString());
						if (resource.getMessage().indexOf("status:Done") != -1 && resource.getType().equals("Normal")) {
							System.out.println(eventType+" success.");
							try {
								Thread.sleep(1000L);
								if (eventType.equals("createDiskFromDiskImage")) {
									jobCreateVM();
								}
								else if (eventType.equals("deleteVM")) {
									jobDeleteDisk();
								}
								else if (eventType.equals("createAndStartVMFromISO")) {
									jobDeleteVM();
								}
							} catch (Exception e) {
								e.printStackTrace();
							}
							onClose(null);
						} 
						else if (resource.getMessage().indexOf("status:Done") != -1 && resource.getType().equals("Warning")) {
							System.out.println(eventType+" failed.");
							onClose(null);
						}
					}
				}

				@Override
				public void onClose(KubernetesClientException cause) {
					System.out.println("Done at " + sdf.format(new Date()));
//					System.out.println("Watcher close due to " + cause);
					client.close();
				}

			});
		}

		protected static CreateDiskFromDiskImage getCreateDiskFromDiskImage() {
			CreateDiskFromDiskImage createDisk = new CreateDiskFromDiskImage();
			createDisk.setType("localfs");
			// create a volume in this pool
			createDisk.setTargetPool("pooldir1");
			// vm disk image name
			createDisk.setSource("/mnt/localfs/pooldir/170zzca5fd174fccafee76b0d7fc2d35/centos7/centos7");
//    		createDisk.setFull_copy(true);
			return createDisk;
		}

		public static DeleteDisk getDeleteDisk() {
			DeleteDisk deleteDisk = new DeleteDisk();
			deleteDisk.setPool("pooldir1");
			deleteDisk.setType("localfs");
			return deleteDisk;
		}

		public static CreateAndStartVMFromISO getCreateAndStartVMFromISO(String id) throws Exception {

			CreateAndStartVMFromISO createAndStartVMFromISO = new CreateAndStartVMFromISO();
			// default value
//    		createAndStartVMFromISO.setMetadata("uuid=950646e8-c17a-49d0-b83c-1c797811vm001");
			createAndStartVMFromISO.setVirt_type("kvm");
			// @see
			// https://github.com/uit-plus/api/blob/master/src/main/java/com/github/uitplus/utils/OSDistroUtils.java
			createAndStartVMFromISO.setOs_variant("centos7.0");
			createAndStartVMFromISO.setNoautoconsole(true);

			// calculationSpecification
			calculationSpecification(createAndStartVMFromISO);

			// Disk and QoS for 1 disk and many disks
			// path /var/lib/libvirt/images/test11 can be get by CreateDiskTest
			// cdrom
//    		createAndStartVMFromISO.setCdrom("/var/lib/libvirt/iso/centos7-minimal-1511.iso"); 
			// Disk and QoS for 1 disk and many disks
			createAndStartVMFromISO.setBoot("hd");
			createAndStartVMFromISO.setDisk("/mnt/localfs/pooldir/170zzca5fd174fccafee76b0d7fc2d35/" + id + "/" + id
					+ ",cache=none,read_bytes_sec=1024000000,write_bytes_sec=1024000000");

			/*
			 * libivrt default bridge Parameters: type type of network support values:
			 * "bridge", "l2bridge" and "l3bridge" source network source name inbound
			 * (optional) inbound bandwidth in KB outbound (optional) outbound bandwidth in
			 * KB mac (optional) if no mac, create a random mac Note! Mac address is unique
			 * and does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3)
			 */
//    		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,ip=192.168.10.14,switch=vxlan");
			createAndStartVMFromISO.setNetwork("type=bridge,source=virbr0,model=virtio");
//          if you want to use l3bridge, please first execute the command on your master node, 'kubeovn-adm create-switch --name switch8888 --subnet 192.168.5.0/24' 		
//    		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,switch=l2l3,inbound=102400,outbound=102400");  

			/*
			 * l2 network example Parameters: type type of network support values: "bridge",
			 * "l2bridge" and "l3bridge" source network source name inbound (optional)
			 * inbound bandwidth in KB outbound (optional) outbound bandwidth in KB mac
			 * (optional) if no mac, create a random mac Note! Mac address is unique and
			 * does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3)
			 */
//    		createAndStartVMFromISO.setNetwork("type=l2bridge,source=br-native,inbound=102400,outbound=102400");

			/*
			 * l3 network example Parameters: type type of network support values: "bridge",
			 * "l2bridge" and "l3bridge" source network source name inbound (optional)
			 * inbound bandwidth limitation in KB, default is no limitation outbound
			 * (optional) outbound bandwidth limitation in KB, default is no limitation mac
			 * (optional) if no mac, create a random mac Note! Mac address is unique and
			 * does not support a value that start with "fe:" (e.g. fe:54:00:05:37:b3) ip
			 * (optional) ip address for l3 network, default is "dynamic" from DHCP switch
			 * switch name
			 */

//    		createAndStartVMFromISO.setNetwork("type=l3bridge,source=br-int,inbound=102400,outbound=102400,ip=192.168.5.9,switch=switch");  

			// consoleMode amd passowrd
			createAndStartVMFromISO.setGraphics("vnc,listen=0.0.0.0");
//    		createAndStartVMFromISO.setGraphics("spice,listen=0.0.0.0" + getconsolePassword("567890")); 

			return createAndStartVMFromISO;
		}

		protected static void calculationSpecification(CreateAndStartVMFromISO createAndStartVMFromISO) {
			createAndStartVMFromISO.setMemory("2048,maxmemory=2048");
			createAndStartVMFromISO.setVcpus("1" + getCPUSet("1-4,6,8"));
		}

		protected static String getCPUSet(String cpuset) {
			return (cpuset == null || cpuset.length() == 0) ? "" : ",cpuset=" + cpuset;
		}

	}

}