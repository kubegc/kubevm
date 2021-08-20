#!/usr/bin/env bash

pyinstaller -F kubesds-rpc-service.py

chmod +x ./dist/kubesds-rpc-service kubesds-ctl.sh

cp -f ./dist/kubesds-rpc-service kubesds-ctl.sh /usr/bin

chmod 777 kubesds.service

cp -f kubesds.service /lib/systemd/system
systemctl daemon-reload