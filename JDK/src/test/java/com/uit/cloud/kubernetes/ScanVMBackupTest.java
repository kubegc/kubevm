package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class ScanVMBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .scanVmBackup("migratepoolnodepool22", "vm.node22", getCleanVMBackup());
        System.out.println(successful);
    }

    public static Lifecycle.ScanVMBackup getCleanVMBackup() {
        Lifecycle.ScanVMBackup scanVMBackup = new Lifecycle.ScanVMBackup();
        scanVMBackup.setDomain("cloudinitbackup5555");
        scanVMBackup.setPool("migratepoolnodepool22");
        scanVMBackup.setVol("e8c9b41664584253afa43592d5efeafb");
        return scanVMBackup;
    }
}
