package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class CleanVMRemoteBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .cleanVMRemoteBackup("migratepoolnodepool22", "vm.node22", getCleanVMBackup());
        System.out.println(successful);
    }

    public static Lifecycle.CleanVMRemoteBackup getCleanVMBackup() {
        Lifecycle.CleanVMRemoteBackup cleanVMBackup = new Lifecycle.CleanVMRemoteBackup();
        cleanVMBackup.setDomain("cloudinitbackup4");
//        cleanVMBackup.setVol("");
        cleanVMBackup.setVersion("backup2");
//        cleanVMBackup.setAll(true);
        cleanVMBackup.setRemote("133.133.135.30");
        cleanVMBackup.setPort("21");
        cleanVMBackup.setUsername("ftpuser");
        cleanVMBackup.setPassword("ftpuser");
        return cleanVMBackup;
    }
}
