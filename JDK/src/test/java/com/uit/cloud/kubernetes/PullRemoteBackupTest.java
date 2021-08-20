package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class PullRemoteBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .pullRemoteBackup("migratepoolnodepool22", "vm.node22", getPullRemoteBackup());
        System.out.println(successful);
    }

    public static Lifecycle.PullRemoteBackup getPullRemoteBackup() {
        Lifecycle.PullRemoteBackup pullRemoteBackup = new Lifecycle.PullRemoteBackup();
        pullRemoteBackup.setDomain("cloudinitbackup4");
//        pullRemoteBackup.setVol("vmbackupdisktest1");
        pullRemoteBackup.setPool("migratepoolnodepool22");
        pullRemoteBackup.setVersion("vmbackup2");
        pullRemoteBackup.setRemote("133.133.135.30");
        pullRemoteBackup.setPort("21");
        pullRemoteBackup.setUsername("ftpuser");
        pullRemoteBackup.setPassword("ftpuser");
        return pullRemoteBackup;
    }
}
