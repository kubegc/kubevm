package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class RestoreVMBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .restoreVMBackup("migratenodepool22", "vm.node22", getRestoreVM());
        System.out.println(successful);
    }

    public static Lifecycle.RestoreVMBackup getRestoreVM() {
        Lifecycle.RestoreVMBackup restoreVMBackup = new Lifecycle.RestoreVMBackup();
        restoreVMBackup.setDomain("wintest");
        restoreVMBackup.setPool("migratenodepool22");
        restoreVMBackup.setVersion("backup1");
//        restoreVMBackup.setAll(true);
//        restoreVMBackup.setTarget("migratenodepool22");
//        restoreVMBackup.setNewname("cloudinitbackup5555");
        return restoreVMBackup;
    }
}
