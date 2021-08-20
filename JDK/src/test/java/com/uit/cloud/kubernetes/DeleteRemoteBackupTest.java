package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class DeleteRemoteBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .deleteRemoteBackup("migratepoolnodepool22", "vm.node22", getDeleteRemoteBackup());
        System.out.println(successful);
    }

    public static Lifecycle.DeleteRemoteBackup getDeleteRemoteBackup() {
        Lifecycle.DeleteRemoteBackup deleteRemoteBackup = new Lifecycle.DeleteRemoteBackup();
        deleteRemoteBackup.setDomain("cloudinitbackup4");
//        deleteRemoteBackup.setVol("cloudinit");
        deleteRemoteBackup.setVersion("vmbackup2");
        deleteRemoteBackup.setRemote("133.133.135.30");
        deleteRemoteBackup.setPort("21");
        deleteRemoteBackup.setUsername("ftpuser");
        deleteRemoteBackup.setPassword("ftpuser");
        return deleteRemoteBackup;
    }
}
