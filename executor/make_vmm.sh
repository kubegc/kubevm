#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER
pyinstaller -F vmm.py -p ./
chmod +x dist/vmm
cp -f scripts/convert-image-to-vm.sh scripts/convert-vm-to-image.sh /usr/bin
cp -f dist/vmm /usr/bin
