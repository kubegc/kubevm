package com.uit.cloud.kubernetes;

import com.github.kubesys.kubernetes.ExtendedKubernetesClient;
import com.github.kubesys.kubernetes.api.model.virtualmachinepool.Lifecycle;

public class PushRemoteBackupTest {
    public static void main(String[] args) throws Exception {

        ExtendedKubernetesClient client = AbstractTest.getClient();
        boolean successful = client.virtualMachinePools()
                .pushRemoteBackup("migratepoolnodepool22", "vm.node22", getPushRemoteBackup());
        System.out.println(successful);
    }

    public static Lifecycle.PushRemoteBackup getPushRemoteBackup() {
        Lifecycle.PushRemoteBackup pushRemoteBackup = new Lifecycle.PushRemoteBackup();
        pushRemoteBackup.setDomain("cloudinitbackup4");
//        pushRemoteBackup.setVol("vmbackupdisktest1");
        pushRemoteBackup.setPool("migratepoolnodepool22");
        pushRemoteBackup.setVersion("vmbackup2");
        pushRemoteBackup.setRemote("133.133.135.30");
        pushRemoteBackup.setPort("21");
        pushRemoteBackup.setUsername("ftpuser");
        pushRemoteBackup.setPassword("ftpuser");
        return pushRemoteBackup;
    }
}
