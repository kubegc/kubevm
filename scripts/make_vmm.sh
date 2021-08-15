#!/usr/bin/env bash

SHELL_FOLDER=$(cd "$(dirname "$0")";pwd)
cd $SHELL_FOLDER
rm -rf dist/ build/ vmm.spec
pyinstaller -F vmm.py -p ./
chmod +x dist/vmm
cp -f dist/vmm /usr/bin

rm -rf dist/ build/ cstor-cli.spec
pyinstaller -F cstor-cli.py -p ./
chmod +x dist/cstor-cli
cp -f dist/cstor-cli /usr/bin
rm -rf dist/ build/ cstor-cli.spec