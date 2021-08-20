/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinenetwork;

import javax.validation.constraints.Pattern;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.annotations.ClassDescriber;
import com.github.kubesys.kubernetes.annotations.FunctionDescriber;
import com.github.kubesys.kubernetes.annotations.ParameterDescriber;
import com.github.kubesys.kubernetes.utils.AnnotationUtils;
import com.github.kubesys.kubernetes.utils.RegExpUtils;

/**
 * @author  wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since   2019/9/4
 * 
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
@ClassDescriber(value = "VirtualMachineNetwork", desc = "扩展支持OVN插件")
public class Lifecycle {

	/**************************************************************
	 * 
	 *      L2 Network
	 * 
	 ***************************************************************/
	@FunctionDescriber(shortName = "创建二层桥接网络，用于vlan场景", description = "创建二层桥接，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateBridge createBridge;
	
	@FunctionDescriber(shortName = "删除二层桥接网络", description = "删除二层桥接," 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteBridge deleteBridge;
	
	@FunctionDescriber(shortName = "设置二层网桥的vlan ID", description = "适用于OpenvSwitch二层网桥，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected SetBridgeVlan setBridgeVlan;
	
	@FunctionDescriber(shortName = "删除二层网桥的vlan ID", description = "适用于OpenvSwitch二层网桥，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DelBridgeVlan delBridgeVlan;
	
	@FunctionDescriber(shortName = "给虚拟机绑定vlan ID", description = "适用于OpenvSwitch二层网桥，更换虚拟机的vlan" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected BindPortVlan bindPortVlan;
	
	@FunctionDescriber(shortName = "解除虚拟机的vlan ID", description = "适用于OpenvSwitch二层网桥，更换虚拟机的vlan" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	@Deprecated
	protected UnbindPortVlan unbindPortVlan;
	
	
	/**************************************************************
	 * 
	 *      L3 Network
	 * 
	 ***************************************************************/
	@FunctionDescriber(shortName = "创建三层网络交换机", description = "创建三层网络交换机，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateSwitch createSwitch;
	
	@FunctionDescriber(shortName = "删除三层网络交换机", description = "删除三层网络交换机，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteSwitch deleteSwitch;
	
	@FunctionDescriber(shortName = "修改三层网络交换机配置", description = "修改三层网络交换机配置，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ModifySwitch modifySwitch;
	
	@FunctionDescriber(shortName = "创建地址列表", description = "创建地址列表，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected CreateAddress createAddress;
	
	@FunctionDescriber(shortName = "删除地址列表", description = "删除地址列表，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = AnnotationUtils.DESC_FUNCTION_VMN, 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected DeleteAddress deleteAddress;
	
	@FunctionDescriber(shortName = "修改地址列表", description = "修改地址列表，" 
			+ AnnotationUtils.DESC_FUNCTION_DESC, 
		prerequisite = "", 
		exception = AnnotationUtils.DESC_FUNCTION_EXEC)
	protected ModifyAddress modifyAddress;
	
	public ModifySwitch getModifySwitch() {
		return modifySwitch;
	}

	public void setModifySwitch(ModifySwitch modifySwitch) {
		this.modifySwitch = modifySwitch;
	}

	public CreateSwitch getCreateSwitch() {
		return createSwitch;
	}

	public void setCreateSwitch(CreateSwitch createSwitch) {
		this.createSwitch = createSwitch;
	}

	public DeleteSwitch getDeleteSwitch() {
		return deleteSwitch;
	}

	public void setDeleteSwitch(DeleteSwitch deleteSwitch) {
		this.deleteSwitch = deleteSwitch;
	}

	public CreateBridge getCreateBridge() {
		return createBridge;
	}

	public void setCreateBridge(CreateBridge createBridge) {
		this.createBridge = createBridge;
	}

	public DeleteBridge getDeleteBridge() {
		return deleteBridge;
	}

	public void setDeleteBridge(DeleteBridge deleteBridge) {
		this.deleteBridge = deleteBridge;
	}


	public SetBridgeVlan getSetBridgeVlan() {
		return setBridgeVlan;
	}

	public void setSetBridgeVlan(SetBridgeVlan setBridgeVlan) {
		this.setBridgeVlan = setBridgeVlan;
	}

	public DelBridgeVlan getDelBridgeVlan() {
		return delBridgeVlan;
	}

	public void setDelBridgeVlan(DelBridgeVlan delBridgeVlan) {
		this.delBridgeVlan = delBridgeVlan;
	}

	public CreateAddress getCreateAddress() {
		return createAddress;
	}

	public void setCreateAddress(CreateAddress createAddress) {
		this.createAddress = createAddress;
	}

	public DeleteAddress getDeleteAddress() {
		return deleteAddress;
	}

	public void setDeleteAddress(DeleteAddress deleteAddress) {
		this.deleteAddress = deleteAddress;
	}

	public ModifyAddress getModifyAddress() {
		return modifyAddress;
	}

	public void setModifyAddress(ModifyAddress modifyAddress) {
		this.modifyAddress = modifyAddress;
	}

	public BindPortVlan getBindPortVlan() {
		return bindPortVlan;
	}

	public void setBindPortVlan(BindPortVlan bindPortVlan) {
		this.bindPortVlan = bindPortVlan;
	}

	public UnbindPortVlan getUnbindPortVlan() {
		return unbindPortVlan;
	}

	public void setUnbindPortVlan(UnbindPortVlan unbindPortVlan) {
		this.unbindPortVlan = unbindPortVlan;
	}


	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateSwitch {

		@ParameterDescriber(required = true, description = "网段，这里后台只会做形式，不会做逻辑判断，只要符合xx.xx.xx.xx/y形式即可，请确保传入正确的数值, y的取值必须是8,16,24之一", constraint = "网段和掩码", example = "192.168.5.1/24")
//		@Pattern(regexp = RegExpUtils.SUBNET_PATTERN)
		protected String subnet;

		@ParameterDescriber(required = false, description = "DHCP地址", constraint = "IP", example = "192.168.5.5")
//		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String dhcp;
		
		@ParameterDescriber(required = true, description = "网关地址", constraint = "IP", example = "192.168.5.5")
//		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String gateway;
		
		@ParameterDescriber(required = false, description = "mtu", constraint = "10-1000", example = "1500")
		@Pattern(regexp = RegExpUtils.MTU_PATTERN)
		protected String mtu;
		
		@ParameterDescriber(required = false, description = "网桥名", constraint = "网桥", example = "br-ex")
		@Pattern(regexp = RegExpUtils.BRIDGE_PATTERN)
		protected String bridge;
		
		@ParameterDescriber(required = false, description = "vlanID", constraint = "0-4094", example = "br-ex")
		@Pattern(regexp = RegExpUtils.VLAN_PATTERN)
		protected String vlanId;
		
		@ParameterDescriber(required = false, description = "IP列表黑名单", constraint = "单个IP之间通过空格分开，IP范围使用..分开", example = "192.168.5.2 192.168.5.10..192.168.5.100")
		@Pattern(regexp = RegExpUtils.EXCLUDEIPS_PATTERN)
		protected String excludeIPs;
		
		@ParameterDescriber(required = false, description = "域名服务器", constraint = "IP地址，允许多个，以,号分开", example = "192.168.5.5")
		@Pattern(regexp = RegExpUtils.DNS_PATTERN)
		protected String dnsServer;
		
		@ParameterDescriber(required = false, description = "是否ipv6", constraint = "true或者false", example = "true")
		@Pattern(regexp = RegExpUtils.BOOL_STRING_TYPE_PATTERN)
		protected String ipv6;
		
		public String getVlanId() {
			return vlanId;
		}

		public void setVlanId(String vlanId) {
			this.vlanId = vlanId;
		}

		public String getBridge() {
			return bridge;
		}

		public void setBridge(String bridge) {
			this.bridge = bridge;
		}

		public String getExcludeIPs() {
			return excludeIPs;
		}

		public void setExcludeIPs(String excludeIPs) {
			this.excludeIPs = excludeIPs;
		}

		public String getSubnet() {
			return subnet;
		}

		public void setSubnet(String subnet) {
			this.subnet = subnet;
		}

		public String getGateway() {
			return gateway;
		}

		public void setGateway(String gateway) {
			this.gateway = gateway;
		}

		public String getMtu() {
			return mtu;
		}

		public void setMtu(String mtu) {
			this.mtu = mtu;
		}

		public String getDnsServer() {
			return dnsServer;
		}

		public void setDnsServer(String dnsServer) {
			this.dnsServer = dnsServer;
		}

		public String getDhcp() {
			return dhcp;
		}

		public void setDhcp(String dhcp) {
			this.dhcp = dhcp;
		}

		public String getIpv6() {
			return ipv6;
		}

		public void setIpv6(String ipv6) {
			this.ipv6 = ipv6;
		}

		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ModifySwitch {

		@ParameterDescriber(required = false, description = "网关地址", constraint = "IP", example = "192.168.5.5")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String gateway;
		
		@ParameterDescriber(required = false, description = "mtu", constraint = "10-1000", example = "1500")
		@Pattern(regexp = RegExpUtils.MTU_PATTERN)
		protected String mtu;
		
		@ParameterDescriber(required = false, description = "域名服务器", constraint = "IP地址", example = "192.168.5.5")
//		@Pattern(regexp = RegExpUtils.DNS_PATTERN)
		protected String dnsServer;
		
		@ParameterDescriber(required = false, description = "DHCP地址", constraint = "IP", example = "192.168.5.5")
		@Pattern(regexp = RegExpUtils.IP_PATTERN)
		protected String dhcp;
		
		@ParameterDescriber(required = false, description = "vlanID", constraint = "0-4094", example = "br-ex")
		@Pattern(regexp = RegExpUtils.VLAN_PATTERN)
		protected String vlanId;
		
		@ParameterDescriber(required = false, description = "是否ipv6", constraint = "true或者false", example = "true")
		@Pattern(regexp = RegExpUtils.BOOL_TYPE_PATTERN)
		protected String ipv6;
		
		public String getGateway() {
			return gateway;
		}

		public void setGateway(String gateway) {
			this.gateway = gateway;
		}

		public String getMtu() {
			return mtu;
		}

		public void setMtu(String mtu) {
			this.mtu = mtu;
		}

		public String getDnsServer() {
			return dnsServer;
		}

		public void setDnsServer(String dnsServer) {
			this.dnsServer = dnsServer;
		}

		public String getDhcp() {
			return dhcp;
		}

		public void setDhcp(String dhcp) {
			this.dhcp = dhcp;
		}

		public String getVlanId() {
			return vlanId;
		}

		public void setVlanId(String vlanId) {
			this.vlanId = vlanId;
		}

		public String getIpv6() {
			return ipv6;
		}

		public void setIpv6(String ipv6) {
			this.ipv6 = ipv6;
		}
		
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteSwitch {
		
		@ParameterDescriber(required = false, description = "网桥名", constraint = "网桥", example = "br-ex")
		@Pattern(regexp = RegExpUtils.BRIDGE_PATTERN)
		protected String bridge;
		
		@ParameterDescriber(required = false, description = "是否ipv6", constraint = "true或者false", example = "true")
		@Pattern(regexp = RegExpUtils.BOOL_TYPE_PATTERN)
		protected String ipv6;

		public String getIpv6() {
			return ipv6;
		}

		public void setIpv6(String ipv6) {
			this.ipv6 = ipv6;
		}

		public String getBridge() {
			return bridge;
		}

		public void setBridge(String bridge) {
			this.bridge = bridge;
		}

	}
	
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class SetBridgeVlan {

		@ParameterDescriber(required = true, description = "vlan ID", constraint = "0~4094", example = "1")
		@Pattern(regexp = RegExpUtils.VLAN_PATTERN)
		protected String vlan;
		
		@ParameterDescriber(required = true, description = "桥接的名字", constraint = "桥接名，3到12位，只允许数字、小写字母、中划线", example = "l2bridge")
		@Pattern(regexp = RegExpUtils.BRIDGE_PATTERN)
		protected String name;

		public String getVlan() {
			return vlan;
		}

		public void setVlan(String vlan) {
			this.vlan = vlan;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DelBridgeVlan extends SetBridgeVlan{

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateBridge {
		
		@ParameterDescriber(required = true, description = "被接管的网卡", constraint = "名称是字符串类型，长度是3到12位，只允许数字、小写字母、中划线、以及圆点", example = "l2bridge")
		@Pattern(regexp = RegExpUtils.NIC_PATTERN)
		protected String nic;
		
		@ParameterDescriber(required = true, description = "桥接的名字", constraint = "桥接名，3到12位，只允许数字、小写字母、中划线", example = "l2bridge")
		@Pattern(regexp = RegExpUtils.BRIDGE_PATTERN)
		protected String name;
		
		@ParameterDescriber(required = false, description = "vlan ID", constraint = "0~4094", example = "1")
		@Pattern(regexp = RegExpUtils.VLAN_PATTERN)
		protected String vlan;

		public String getNic() {
			return nic;
		}

		public void setNic(String nic) {
			this.nic = nic;
		}

		public String getVlan() {
			return vlan;
		}

		public void setVlan(String vlan) {
			this.vlan = vlan;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteBridge {
		
		@ParameterDescriber(required = true, description = "被接管的网卡", constraint = "名称是字符串类型，长度是3到12位，只允许数字、小写字母、中划线、以及圆点", example = "l2bridge")
		@Pattern(regexp = RegExpUtils.NIC_PATTERN)
		protected String nic;
		
		@ParameterDescriber(required = true, description = "桥接的名字", constraint = "桥接名，3到12位，只允许数字、小写字母、中划线", example = "l2bridge")
		@Pattern(regexp = RegExpUtils.BRIDGE_PATTERN)
		protected String name;
		
		public String getNic() {
			return nic;
		}

		public void setNic(String nic) {
			this.nic = nic;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class BindPortVlan {
		
		@ParameterDescriber(required = true, description = "mac地址", constraint = "mac地址不能以fe开头", example = "7e:0c:b0:ef:6a:04")
		@Pattern(regexp = RegExpUtils.MAC_PATTERN)
		protected String mac;
		
		@ParameterDescriber(required = true, description = "虚拟机名称", constraint = "4-100位，包含小写字母，数字0-9，中划线，以及圆点", example = "950646e8c17a49d0b83c1c797811e004")
		@Pattern(regexp = RegExpUtils.NAME_PATTERN)
		protected String domain;
		
		@ParameterDescriber(required = false, description = "vlan ID", constraint = "0~4094", example = "1")
		@Pattern(regexp = RegExpUtils.VLAN_PATTERN)
		protected String vlan;

		public String getDomain() {
			return domain;
		}

		public void setDomain(String domain) {
			this.domain = domain;
		}

		public String getMac() {
			return mac;
		}

		public void setMac(String mac) {
			this.mac = mac;
		}

		public String getVlan() {
			return vlan;
		}

		public void setVlan(String vlan) {
			this.vlan = vlan;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	@Deprecated
	public static class UnbindPortVlan extends BindPortVlan {
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreateAddress {
		
		@ParameterDescriber(required = true, description = "地址列表", constraint = "IP以,分割", example = "192.168.1.1，192.168.1.2")
		@Pattern(regexp = RegExpUtils.ADDRESS_PATTERN)
		protected String address;

		public String getAddress() {
			return address;
		}

		public void setAddress(String address) {
			this.address = address;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class ModifyAddress extends CreateAddress {
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class DeleteAddress {
		
	}
}
