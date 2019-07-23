#!/bin/bash
# author: liu he


DEFAULT_PATH=/root/mybackup/ 

if [ ! -d "$DEFAULT_PATH" ]; then
    mkdir $DEFAULT_PATH
fi

# check is exist the vm, and the vm is running or not
line1=`virsh list --all | grep $1 | wc -l`

if [ $line1 -eq 1 ] 
then
    echo 'log info: vm exist...\n'
else
    echo 'log error: vm not exist...\n'
    exit 1
fi


line2=`virsh list --all | grep $1 | grep 'shut' | wc -l`

if [ $line2 -eq 1 ]
then
    echo 'log info: vm has shut down...'
else
    echo 'log error: vm is running..., please shut down firstly...\n'
    exit 1
#    virsh destroy $1
#    if [ $? -ne 0 ]; then
#        echo "occur error while shutting down vm..."
#        exit 1
#    else
#        echo "shut down vm successfully..."
#    fi
fi

# step 1 dump  vm xml
virsh dumpxml $1 > ${DEFAULT_PATH}${1}.xml

if [ $? -ne 0 ]; then
    echo "log error: dump xml file fail...\n"
    exit 1
else
    echo "log info: dump xml file successfully...\n"
fi

# step 2 cop the file to default path

IMAGEPATH=`cat ${DEFAULT_PATH}${1}.xml | grep 'source file' | grep 'qcow2'| cut -d "'" -f 2`

echo $IMAGEPATH
cp ${IMAGEPATH} ${DEFAULT_PATH}

if [ $? -ne 0 ]; then
    echo "log error: copy image file fail...\n"
    # operation fial, roll back
    rm ${DEFAULT_PATH}${1}.xml
    exit 1
else
    echo "log info: copy image file successfully...\n"
fi

# step 3
virsh undefine $1
if [ $? -ne 0 ]; then
    echo "log error: undefine vm fail..., deleting xml file and vm image copy\n"
    # operation fial, roll back
    rm -f ${DEFAULT_PATH}${1}.xml ${DEFAULT_PATH}${IMAGEPATH} 
    exit 1
else
    echo "log info: undifine vm successfully...\n"
fi


