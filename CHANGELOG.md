# 变更日志
## 版本 v1.4.4-rc1
### 接口变更
```
1、变更createDiskFromDiskImage，参数sourceImage改为source，传路径
```

## 版本 v1.4.4
### 接口变更
```
1、变更covertDiskToDiskImage -> createDiskImageFromDisk(metadata_name, sourceVolume, sourcePool, targetPool)
2、删除covertDiskImageToDisk
3、删除云盘快照文件（当删除为current的快照时，实际不删除任何文件，当删除其他快照时，均会删除快照文件）
4、删除云盘（从k8s中删除，云盘目录及文件均不删除）
```
### 异常修复
```
1、修复CreateDiskImage参数个数错误（vmm.py->create_vmdi()）
```
