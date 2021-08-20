#!/usr/bin/env bash

/root/pyinstaller -F kubesds-adm.py
/root/pyinstaller -F kubesds-rpc-service.py

chmod +x ./dist/kubesds-rpc-service kubesds-ctl.sh

cp -f ./dist/kubesds-rpc-service kubesds-ctl.sh /usr/bin

chmod 777 kubesds.service

cp -f kubesds.service /lib/systemd/system
systemctl daemon-reload

cp -f ./dist/kubesds-adm /usr/bin

