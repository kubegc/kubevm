/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinenetwork;

import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @since Thu Aug 20 21:36:39 CST 2019
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
public class Data {

	protected SwitchInfo switchInfo;

	protected RouterInfo routerInfo;

	protected GatewayInfo gatewayInfo;

	protected BridgeInfo bridgeInfo;

	protected AddressInfo addressInfo;

	public BridgeInfo getBridgeInfo() {
		return bridgeInfo;
	}

	public void setBridgeInfo(BridgeInfo bridgeInfo) {
		this.bridgeInfo = bridgeInfo;
	}

	public SwitchInfo getSwitchInfo() {
		return switchInfo;
	}

	public void setSwitchInfo(SwitchInfo switchInfo) {
		this.switchInfo = switchInfo;
	}

	public RouterInfo getRouterInfo() {
		return routerInfo;
	}

	public void setRouterInfo(RouterInfo routerInfo) {
		this.routerInfo = routerInfo;
	}

	public GatewayInfo getGatewayInfo() {
		return gatewayInfo;
	}

	public void setGatewayInfo(GatewayInfo gatewayInfo) {
		this.gatewayInfo = gatewayInfo;
	}

	public AddressInfo getAddressInfo() {
		return addressInfo;
	}

	public void setAddressInfo(AddressInfo addressInfo) {
		this.addressInfo = addressInfo;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class SwitchInfo {

		protected String id;

		protected String name;

		protected List<Ports> ports;

		public List<Ports> getPorts() {
			return ports;
		}

		public void setPorts(List<Ports> ports) {
			this.ports = ports;
		}

		public SwitchInfo() {
			super();
		}

		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Ports {

			protected String name;

			protected String tag;

			protected String type;

			protected Object addresses;

			protected String router_port;

			public String getTag() {
				return tag;
			}

			public void setTag(String tag) {
				this.tag = tag;
			}

			public Object getAddresses() {
				return addresses;
			}

			public void setAddresses(Object addresses) {
				this.addresses = addresses;
			}

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getType() {
				return type;
			}

			public void setType(String type) {
				this.type = type;
			}

			public String getRouter_port() {
				return router_port;
			}

			public void setRouter_port(String router_port) {
				this.router_port = router_port;
			}

		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class RouterInfo {

		protected String id;

		protected String name;

		protected List<Ports> ports;

		protected List<Nat> nat;

		public List<Ports> getPorts() {
			return ports;
		}

		public void setPorts(List<Ports> ports) {
			this.ports = ports;
		}

		public RouterInfo() {
			super();
		}

		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public List<Nat> getNat() {
			return nat;
		}

		public void setNat(List<Nat> nat) {
			this.nat = nat;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Ports {

			protected String name;

			protected String mac;

			protected String networks;

			protected String gateway;

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getMac() {
				return mac;
			}

			public void setMac(String mac) {
				this.mac = mac;
			}

			public String getNetworks() {
				return networks;
			}

			public void setNetworks(String networks) {
				this.networks = networks;
			}

			public String getGateway() {
				return gateway;
			}

			public void setGateway(String gateway) {
				this.gateway = gateway;
			}

		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Nat {

			protected String name;

			protected String externalIP;

			protected String logicalIP;

			protected String type;

			protected String gateway;

			public Nat() {
				super();
			}

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getExternalIP() {
				return externalIP;
			}

			public void setExternalIP(String externalIP) {
				this.externalIP = externalIP;
			}

			public String getLogicalIP() {
				return logicalIP;
			}

			public void setLogicalIP(String logicalIP) {
				this.logicalIP = logicalIP;
			}

			public String getType() {
				return type;
			}

			public void setType(String type) {
				this.type = type;
			}

			public String getGateway() {
				return gateway;
			}

			public void setGateway(String gateway) {
				this.gateway = gateway;
			}

		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class GatewayInfo {

		protected String id;

		protected String server_mac;

		protected String server_id;

		protected String router;

		protected String lease_time;

		public String getId() {
			return id;
		}

		public void setId(String id) {
			this.id = id;
		}

		public String getServer_mac() {
			return server_mac;
		}

		public void setServer_mac(String server_mac) {
			this.server_mac = server_mac;
		}

		public String getServer_id() {
			return server_id;
		}

		public void setServer_id(String server_id) {
			this.server_id = server_id;
		}

		public String getRouter() {
			return router;
		}

		public void setRouter(String router) {
			this.router = router;
		}

		public String getLease_time() {
			return lease_time;
		}

		public void setLease_time(String lease_time) {
			this.lease_time = lease_time;
		}

	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class BridgeInfo {
		protected String name;

		protected List<Ports> ports;

		protected String uuid;

		public List<Ports> getPorts() {
			return ports;
		}

		public void setPorts(List<Ports> ports) {
			this.ports = ports;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public String getUuid() {
			return uuid;
		}

		public void setUuid(String uuid) {
			this.uuid = uuid;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Ports {
			protected String name;

			protected String uuid;

			protected String vlan;

			protected List<Interfaces> interfaces;

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getUuid() {
				return uuid;
			}

			public void setUuid(String uuid) {
				this.uuid = uuid;
			}

			public String getVlan() {
				return vlan;
			}

			public void setVlan(String vlan) {
				this.vlan = vlan;
			}

			public List<Interfaces> getInterfaces() {
				return interfaces;
			}

			public void setInterfaces(List<Interfaces> interfaces) {
				this.interfaces = interfaces;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Interfaces {

				protected String name;

				protected String uuid;

				protected String mac;

				public String getName() {
					return name;
				}

				public void setName(String name) {
					this.name = name;
				}

				public String getUuid() {
					return uuid;
				}

				public void setUuid(String uuid) {
					this.uuid = uuid;
				}

				public String getMac() {
					return mac;
				}

				public void setMac(String mac) {
					this.mac = mac;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class AddressInfo {

		protected String _uuid;

		protected String addresses;

		protected String external_ids;

		protected String name;

		public String getAddresses() {
			return addresses;
		}

		public void setAddresses(String addresses) {
			this.addresses = addresses;
		}

		public String get_uuid() {
			return _uuid;
		}

		public void set_uuid(String _uuid) {
			this._uuid = _uuid;
		}

		public String getExternal_ids() {
			return external_ids;
		}

		public void setExternal_ids(String external_ids) {
			this.external_ids = external_ids;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

	}
}
