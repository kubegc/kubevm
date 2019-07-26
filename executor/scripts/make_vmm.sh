#!/usr/bin/env bash

cd /root/kubevmm/executor/scripts/
pyinstaller -F executor/vmm.py -p ./executor/