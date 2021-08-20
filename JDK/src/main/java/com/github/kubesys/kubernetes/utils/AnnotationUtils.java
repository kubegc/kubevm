/*
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.utils;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.2.0
 * @since   2019/9/3
 *
 */
public class AnnotationUtils {

	public final static String DESC_BOOLEAN       = "true或者false";
	
	public final static String DESC_FUNCTION_DESC = "只会返回True或者异常"
			+ "返回True意味着提交到Kubernetes成功，并不代表执行成功(异步设计)。开发人员需要通过监听Event和Watcher方法获取更详细信息；"
			+ "如果提交到Kubernetes后执行错误，请查看[接口异常]";
	
	public final static String DESC_BRIDGE_DESC   = "只能取值bridge，l2bridge，l3bridge. brdige表示libvirt自定义交换机，"
			+ "但不支持设置mac和IP等；l2bridge是Ovs交换机，虚拟机或获得与当前物理机网络一样的IP，但不能动态指定；l3bridge是基于gre或vxlan的，可设置mac和IP等";
	
	public final static String DESC_TARGET_DESC   = "windows可适用hdx驱动，Linux可适用vdx驱动，x是指a,b,c,d可增长，但不能重名，disk具体是哪种target，以及适用了哪些target可以通过get方法获取进行分析";
	
	public final static String DESC_FUNCTION_EXEC = "RuntimeException: 出现重名或不存在，或者该资源（如VirtualMachine, VirtualMachinePool等）还在处理中，需等待上一步操作完成才能进行下一步";
	
	public final static String DESC_FUNCTION_VM   = "虚拟机存在，即已调用过CreatePool, CreateSwitch, CreateDisk/CreateDiskImage, CreateAndStartVMFromISO/CreateAndStartVMFromImage";
	
	public final static String DESC_FUNCTION_VMD  = "云盘存在，即已调用过CreateDisk/CreateDiskFromDiskImage";
	
	public final static String DESC_FUNCTION_VMDSN  = "云盘快照存在，即已调用过CreateDiskExternalSnapshot";
	
	public final static String DESC_FUNCTION_VMDI = "云盘镜像存在，即已调用过CreateDiskImage/ConvertDiskToDiskImage";
	
	public final static String DESC_FUNCTION_VMI  = "虚拟机镜像存在，即已调用过CreateImage/ConvertVMToImage";
	
	public final static String DESC_FUNCTION_VMSN = "虚拟机/云盘快照存在，即已调用过CreateSnapshot";
	
	public final static String DESC_FUNCTION_VMN  = "虚拟机网络存在，即已调用过CreateSwitch";
	
	public final static String DESC_FUNCTION_VMP  = "虚拟机存储池存在，即已调用过CreatePool";

}
