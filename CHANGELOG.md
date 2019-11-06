# 变更日志
## 版本 v1.4.4-rc1
### 接口变更
```
1、变更createDiskFromDiskImage，参数sourceImage改为source，传路径
### Commits
```
009140efdd337bc9525830e930339197dc454439
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
### Commits
```
8c9180336bc0f5ce53cbdd00e5ad4bcfcc5d28b4
c2dd3fb354c26887bd52647ef7d18721b6cf60b8
04d2cff6b5ad19628b9b4311ce61557f10c4bac0
453f9b8bee1a9d1c028a5570e314278a23f569cd
45269150735d090563404b8089f9de60e953505c
```
