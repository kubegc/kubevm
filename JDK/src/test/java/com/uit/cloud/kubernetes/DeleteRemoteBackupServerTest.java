package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class DeleteRemoteBackupServerTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .deleteRemoteBackupServer("migratenodepool22", "vm.node22", getDeleteRemoteBackupServer());
        System.out.println(successful);
    }

    public static Lifecycle.DeleteRemoteBackupServer getDeleteRemoteBackupServer() {
        Lifecycle.DeleteRemoteBackupServer deleteRemoteBackupServer = new Lifecycle.DeleteRemoteBackupServer();
        deleteRemoteBackupServer.setRemote("133.133.135.30");
        deleteRemoteBackupServer.setPort("21");
        deleteRemoteBackupServer.setUsername("ftpuser");
        deleteRemoteBackupServer.setPassword("ftpuser");
        return deleteRemoteBackupServer;
    }
}
