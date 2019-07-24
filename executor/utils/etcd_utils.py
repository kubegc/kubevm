import etcd3

# conda install protobuf
# pip install -U protobuf

# client = etcd.Client(host='133.133.133.22',
#             port=2379,
#             read_timeout=60,
#             allow_redirect=True,
#             protocol='https',
#             cacert='/etc/kubernetes/pki/etcd/ca.crt',
#             cert='/etc/kubernetes/pki/etcd/server.crt',
#             key='/etc/kubernetes/pki/etcd/server.key',
#             allow_reconnect=False)

client = etcd3.client(host='133.133.135.22',
                     port=2379,
                     ca_cert='../scripts/ca.crt',
                     cert_cert='../scripts/server.crt',
                     cert_key='../scripts/server.key')

# ETCDCTL_API=3 etcdctl --endpoints 133.133.135.22:2379 \
#                       --cacert /etc/kubernetes/pki/etcd/ca.crt \
#                       --cert /etc/kubernetes/pki/etcd/server.crt \
#                       --key /etc/kubernetes/pki/etcd/server.key get / \
#                       --prefix --keys-only

result = client.get('/registry/services/specs/kube-system/kube-dns')
print(result) # bar