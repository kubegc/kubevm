package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class CleanVMBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .cleanVMBackup("migratepoolnodepool22", "vm.node22", getCleanVMBackup());
        System.out.println(successful);
    }

    public static Lifecycle.CleanVMBackup getCleanVMBackup() {
        Lifecycle.CleanVMBackup cleanVMBackup = new Lifecycle.CleanVMBackup();
        cleanVMBackup.setDomain("cloudinitbackup4");
        cleanVMBackup.setPool("migratepoolnodepool22");
//        cleanVMBackup.setVol("vmbackupdisk1");
        cleanVMBackup.setAll(true);
        return cleanVMBackup;
    }
}
