package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class DeleteVMDiskBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .deleteVMDiskBackup("migratepoolnodepool22", "vm.node22", getDeleteVMDiskBackup());
        System.out.println(successful);
    }

    public static Lifecycle.DeleteVMDiskBackup getDeleteVMDiskBackup() {
        Lifecycle.DeleteVMDiskBackup deleteVMBackup = new Lifecycle.DeleteVMDiskBackup();
        deleteVMBackup.setDomain("cloudinitbackup4");
        deleteVMBackup.setPool("migratepoolnodepool22");
        deleteVMBackup.setVersion("diskbackup1");
        return deleteVMBackup;
    }
}
