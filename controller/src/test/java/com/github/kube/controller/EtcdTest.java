package com.github.kube.controller;

import com.github.kube.controller.ha.DistributedLock;
import com.github.kube.controller.ha.DistributedLock.LockResult;

public class EtcdTest 
{
	
    public static void main(String[] args) throws Exception {
    	for (int i = 0; i < 5; i++)
        {
            new MyThread().start();
        }
    }
    
    public static class MyThread extends Thread
    {
        @Override
        public void run()
        {
            String lockName = "/lock/mylock";
            // 1. 加锁
            LockResult lockResult = DistributedLock.getInstance().lock(lockName, 30);

            // 2. 执行业务
            if (lockResult.getIsLockSuccess())
            {
                // 获得锁后，执行业务，用sleep方法模拟.
                try
                {
                    Thread.sleep(10000);
                }
                catch (InterruptedException e)
                {
                    System.out.println("[error]:" + e);
                }
            }

            // 3. 解锁
            DistributedLock.getInstance().unLock(lockName, lockResult);
        }
    }

}
