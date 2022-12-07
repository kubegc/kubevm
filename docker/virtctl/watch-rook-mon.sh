#!/bin/bash -e

CEPH_CONFIG="/etc/ceph/ceph.conf"
MON_CONFIG="/etc/rook/mon-endpoints"
MON_SHELL="kubectl get configmap rook-ceph-mon-endpoints -n rook-ceph -o yaml | grep 'data: ' | sed 's/  data: //'"
KEYRING_FILE="/etc/ceph/keyring"

# create dir
if [ ! -d "/etc/rook/" ];then
  mkdir /etc/rook/
fi

# create a ceph config file in its default location so ceph/rados tools can be used
# without specifying any arguments
write_endpoints() {
  endpoints=$(eval $MON_SHELL | sed 's/ //')

  # filter out the mon names
  # external cluster can have numbers or hyphens in mon names, handling them in regex
  # shellcheck disable=SC2001
  mon_endpoints=$(echo "${endpoints}")
cat <<EOF > ${MON_CONFIG}
${mon_endpoints}
EOF
  mon_endpoints=$(echo "${endpoints}"| sed 's/[a-z0-9_-: ]\+=//g')
  DATE=$(date)
  echo "$DATE writing mon endpoints to ${CEPH_CONFIG}: ${mon_endpoints}"
    cat <<EOF > ${CEPH_CONFIG}
[global]
mon_host = ${mon_endpoints}

[client.admin]
keyring = ${KEYRING_FILE}
EOF
}

# watch the endpoints config file and update if the mon endpoints ever change
watch_endpoints() {
  # get the timestamp for the target of the soft link
  real_txt=$(cat ${MON_CONFIG})
  while true; do
    latest_txt=$(eval $MON_SHELL | sed 's/ //')
#    echo $real_txt
#    echo $latest_txt
    if [[ ${real_txt} != ${latest_txt} ]]; then
      write_endpoints
      real_txt=$latest_txt
    fi

    sleep 10
  done
}

ROOK_CEPH_USERNAME=$(kubectl -n rook-ceph get secret rook-ceph-mon -o jsonpath="{['data']['ceph-username']}" | base64 --decode && echo)
ROOK_CEPH_SECRET=$(kubectl -n rook-ceph get secret rook-ceph-mon -o jsonpath="{['data']['ceph-secret']}" | base64 --decode && echo)
# create the keyring file
cat <<EOF > ${KEYRING_FILE}
[${ROOK_CEPH_USERNAME}]
key = ${ROOK_CEPH_SECRET}
EOF

# write the initial config file
write_endpoints

# continuously update the mon endpoints if they fail over
if [ "$1" != "--skip-watch" ]; then
  watch_endpoints
fi