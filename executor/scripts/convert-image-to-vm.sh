#!/bin/bash
# author: liu he

# need args: VM-name

DEFAULT_IMAGE_PATH=/var/lib/libvirt/template/
DEFAULT_VM_PATH=/var/lib/libvirt/images/

# check the name is exist the vm or not
line1=`virsh list --all | awk '{ print $2 }' | grep -w $1 | wc -l`

if [ $line1 -eq 1 ]
then
    echo 'log error: vm name exist, create vm from image fail...\n'
    exit 1
else
    echo 'log error: vm name not exist, begin to create vm from image...\n'
fi

# check is exist the image or not
if [ ! -f ${DEFAULT_IMAGE_PATH}${1}'.xml' ]
then
  echo "log error: image not exist, create vm from image fail...\n"
  exit 1
else
  echo "log info: image has exist, continue...\n"
fi


# check the image OLD_PATH disk space support to create VM or not
OLD_PATH=`cat ${DEFAULT_IMAGE_PATH}${1}'.path'`
echo $OLD_PATH
echo ${DEFAULT_IMAGE_PATH}${OLD_PATH##*/}
NEED_SPACE=`du -m ${DEFAULT_IMAGE_PATH}${OLD_PATH##*/} | awk '{print $1}'`

DISK_SPACE=`df -m ${OLD_PATH%/*} | awk '{ print $4 }' | tail -n +2 |awk '{sum+=$1} END {print sum}'`
if [ $DISK_SPACE -gt $NEED_SPACE ]
then
    echo $NEED_SPACE
    echo $DISK_SPACE
    echo "log info: space is enough, continue convert image to vm..."
else
    echo $NEED_SPACE
    echo $DISK_SPACE
    echo "log error: space is not enough, stop convert image to vm..."
    exit 1
fi

cp ${DEFAULT_IMAGE_PATH}${OLD_PATH##*/} ${OLD_PATH%/*}

if [ $? -ne 0 ]; then
    echo "log error: copy image disk to old path fail...\n"
    exit 1
else
    echo "log info: copy image disk to old path successfully...\n"
    sed -i 's#'${DEFAULT_IMAGE_PATH}${OLD_PATH##*/}'#'${OLD_PATH}'#g' ${DEFAULT_IMAGE_PATH}${1}.xml
    if [ $? -ne 0 ]; then
        echo "log error: change the vm file path in xml file failed\n"
        # operation fial, roll back
        rm -f ${OLD_PATH}
        exit 1
    else
        echo "log info: change the vm file path in xml file successfully...\n"
        virsh define ${DEFAULT_IMAGE_PATH}${1}.xml
        if [ $? -ne 0 ]; then
            echo "log error: virsh define failed\n"
            # operation fial, roll back
            rm -f ${OLD_PATH}
            exit 1
        else
            echo "log info: virsh define successfully...\n"
            rm -f ${DEFAULT_IMAGE_PATH}${1}.xml ${DEFAULT_IMAGE_PATH}${OLD_PATH##*/} ${DEFAULT_IMAGE_PATH}${1}.path
        fi
    fi
fi



#virsh start $1




