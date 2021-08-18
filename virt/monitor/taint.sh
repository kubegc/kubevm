#!/usr/bin/env bash

kubectl taint nodes $1 node-role.kubernetes.io/master-