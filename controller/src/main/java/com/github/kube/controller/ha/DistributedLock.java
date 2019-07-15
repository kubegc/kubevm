/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kube.controller.ha;

import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

import io.etcd.jetcd.ByteSequence;
import io.etcd.jetcd.Client;
import io.etcd.jetcd.Lease;
import io.etcd.jetcd.Lock;

/**
 * @author shizhonghao17@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @author wuheng@otcaix.iscas.ac.cn
 * @since Wed July 04 17:26:22 CST 2019
 * 
 *        https://www.json2yaml.com/ http://www.bejson.com/xml2json/
 * 
 *        debug at runWatch method of
 *        io.fabric8.kubernetes.client.dsl.internal.WatchConnectionManager
 **/
public class DistributedLock {
	private static DistributedLock lockProvider = null;
	private static Object mutex = new Object();
	private Client client;
	private Lock lockClient;
	private Lease leaseClient;

	private DistributedLock() {
		super();
		// 创建Etcd客户端，本例中Etcd集群只有一个节点
		this.client = Client.builder().endpoints("http://localhost:2379").build();
		this.lockClient = client.getLockClient();
		this.leaseClient = client.getLeaseClient();
	}

	public static DistributedLock getInstance() {
		synchronized (mutex) {
			if (null == lockProvider) {
				lockProvider = new DistributedLock();
			}
		}
		return lockProvider;
	}

	/**
	 * 加锁操作，需要注意的是，本例中没有加入重试机制，加锁失败将直接返回。
	 * 
	 * @param lockName: 针对某一共享资源(数据、文件等)制定的锁名
	 * @param TTL       : Time To Live，租约有效期，一旦客户端崩溃，可在租约到期后自动释放锁
	 * @return LockResult
	 */
	public LockResult lock(String lockName, long TTL) {
		LockResult lockResult = new LockResult();
		/* 1.准备阶段 */
		// 创建一个定时任务作为“心跳”，保证等待锁释放期间，租约不失效；
		// 同时，一旦客户端发生故障，心跳便会停止，锁也会因租约过期而被动释放，避免死锁
		ScheduledExecutorService service = Executors.newSingleThreadScheduledExecutor();

		// 初始化返回值lockResult
		lockResult.setIsLockSuccess(false);
		lockResult.setService(service);

		// 记录租约ID，初始值设为 0L
		Long leaseId = 0L;

		/* 2.创建租约 */
		// 创建一个租约，租约有效期为TTL，实际应用中根据具体业务确定。
		try {
			leaseId = leaseClient.grant(TTL).get().getID();
			lockResult.setLeaseId(leaseId);

			// 启动定时任务续约，心跳周期和初次启动延时计算公式如下，可根据实际业务制定。
			long period = TTL - TTL / 5;
			service.scheduleAtFixedRate(new KeepAliveTask(leaseClient, leaseId), period, period, TimeUnit.SECONDS);
		} catch (InterruptedException | ExecutionException e) {
			System.out.println("[error]: Create lease failed:" + e);
			return lockResult;
		}

		System.out.println("[lock]: start to lock." + Thread.currentThread().getName());

		/* 3.加锁操作 */
		// 执行加锁操作，并为锁对应的key绑定租约
		try {
			lockClient.lock(ByteSequence.from(lockName.getBytes()), leaseId).get();
		} catch (InterruptedException | ExecutionException e1) {
			System.out.println("[error]: lock failed:" + e1);
			return lockResult;
		}
		System.out.println("[lock]: lock successfully." + Thread.currentThread().getName());

		lockResult.setIsLockSuccess(true);

		return lockResult;
	}

	/**
	 * 解锁操作，释放锁、关闭定时任务、解除租约
	 * 
	 * @param lockName:锁名
	 * @param lockResult:加锁操作返回的结果
	 */
	public void unLock(String lockName, LockResult lockResult) {
		System.out.println("[unlock]: start to unlock." + Thread.currentThread().getName());
		try {
			// 释放锁
			lockClient.unlock(ByteSequence.from(lockName.getBytes())).get();
			// 关闭定时任务
			lockResult.getService().shutdown();
			// 删除租约
			if (lockResult.getLeaseId() != 0L) {
				leaseClient.revoke(lockResult.getLeaseId());
			}
		} catch (InterruptedException | ExecutionException e) {
			System.out.println("[error]: unlock failed: " + e);
		}

		System.out.println("[unlock]: unlock successfully." + Thread.currentThread().getName());
	}

	/**
	 * 在等待其它客户端释放锁期间，通过心跳续约，保证自己的锁对应租约不会失效
	 *
	 */
	public static class KeepAliveTask implements Runnable {
		private Lease leaseClient;
		private long leaseId;

		KeepAliveTask(Lease leaseClient, long leaseId) {
			this.leaseClient = leaseClient;
			this.leaseId = leaseId;
		}

		@Override
		public void run() {
			// 续约一次
			leaseClient.keepAliveOnce(leaseId);
		}
	}

	/**
	 * 该class用于描述加锁的结果，同时携带解锁操作所需参数
	 * 
	 */
	public static class LockResult {
		private boolean isLockSuccess;
		private long leaseId;
		private ScheduledExecutorService service;

		LockResult() {
			super();
		}

		public void setIsLockSuccess(boolean isLockSuccess) {
			this.isLockSuccess = isLockSuccess;
		}

		public void setLeaseId(long leaseId) {
			this.leaseId = leaseId;
		}

		public void setService(ScheduledExecutorService service) {
			this.service = service;
		}

		public boolean getIsLockSuccess() {
			return this.isLockSuccess;
		}

		public long getLeaseId() {
			return this.leaseId;
		}

		public ScheduledExecutorService getService() {
			return this.service;
		}
	}

}