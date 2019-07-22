#!/bin/bash
# author: liu he


DEFAULT_PATH=/root/mybackup/ 

if [ ! -d "$DEFAULT_PATH" ]; then
        mkdir $DEFAULT_PATH
fi

# check is exist tje vm, and the vm is running or not
line1=`virsh list --all | grep $1 | wc -l`

if [ $line1 -eq 1 ] 
then
    echo 'vm exist...'
else
    echo 'vm not exist...'
    exit 1
fi


line2=`virsh list --all | grep $1 | grep 'shut' | wc -l`

if [ $line2 -eq 1 ]
then
    echo 'vm has shut down...'
else
    echo 'vm is running..., shutting down...'
    virsh destroy $1
    if [ $? -ne 0 ]; then
        echo "occur error while shutting down vm..."
        exit 1
    else
        echo "shut down vm successfully..."
    fi
fi

# step 1 dump  vm xml
virsh dumpxml $1 > ${DEFAULT_PATH}${1}.xml

if [ $? -ne 0 ]; then
    echo "dump xml file fail..."
    exit 1
else
    echo "dump xml file successfully..."
fi

# step 2 cop the file to default path

IMAGEPATH=`cat ${DEFAULT_PATH}${1}.xml | grep 'source file' | grep 'qcow2'| cut -d "'" -f 2`

echo $IMAGEPATH
cp ${IMAGEPATH} ${DEFAULT_PATH}

if [ $? -ne 0 ]; then
    echo "copy image file fail..."
    # operation fial, roll back
    rm ${DEFAULT_PATH}${1}.xml
    exit 1
else
    echo "copy image file successfully..."
fi

# step 3
virsh undefine $1
if [ $? -ne 0 ]; then
    echo "undefine vm fail..., deleting xml file and vm image copy"
    # operation fial, roll back
    rm -f ${DEFAULT_PATH}${1}.xml ${DEFAULT_PATH}${IMAGEPATH} 
    exit 1
else
    echo "undifine vm successfully..."
fi


