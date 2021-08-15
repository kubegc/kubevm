#!/bin/bash

cd "$(dirname $0)"

kubectl create -f *.yaml

kubectl delete -f *.yaml