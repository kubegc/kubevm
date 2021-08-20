/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachine;

import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @since Thu Jun 22 21:36:39 CST 2019
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
public class Domain {

	protected Metadata metadata;

	protected Memory memory;

	protected Vcpu vcpu;

	protected ArrayList<Seclabel> seclabel;
	
	protected Description description;

	protected Title title;

	protected MaxMemory maxMemory;

	protected Uuid uuid;

	protected Iothreadids iothreadids;

	protected Features features;

	protected On_crash on_crash;

	protected Blkiotune blkiotune;

	protected Bootloader bootloader;

	protected Idmap idmap;

	protected Sysinfo sysinfo;

	protected Memtune memtune;

	protected Numatune numatune;

	protected Keywrap keywrap;

	protected MemoryBacking memoryBacking;

	protected Perf perf;

	protected LaunchSecurity launchSecurity;

	protected On_poweroff on_poweroff;

	protected Bootloader_args bootloader_args;

	protected Os os;

	protected Devices devices;

	protected Resource resource;

	protected On_reboot on_reboot;

	protected String _type;

	protected Cpu cpu;

	protected Clock clock;

	protected Vcpus vcpus;

	protected Cputune cputune;

	protected Genid genid;

	protected Iothreads iothreads;

	protected Name name;

	protected CurrentMemory currentMemory;

	protected String _id;

	protected Pm pm;

	public Domain() {

	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setMetadata(Metadata metadata) {
		this.metadata = metadata;
	}

	public Metadata getMetadata() {
		return this.metadata;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setMemory(Memory memory) {
		this.memory = memory;
	}

	public Memory getMemory() {
		return this.memory;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setVcpu(Vcpu vcpu) {
		this.vcpu = vcpu;
	}

	public Vcpu getVcpu() {
		return this.vcpu;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setDescription(Description description) {
		this.description = description;
	}

	public ArrayList<Seclabel> getSeclabel() {
		return seclabel;
	}

	public void setSeclabel(ArrayList<Seclabel> seclabel) {
		this.seclabel = seclabel;
	}

	public Description getDescription() {
		return this.description;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setTitle(Title title) {
		this.title = title;
	}

	public Title getTitle() {
		return this.title;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setMaxMemory(MaxMemory maxMemory) {
		this.maxMemory = maxMemory;
	}

	public MaxMemory getMaxMemory() {
		return this.maxMemory;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setUuid(Uuid uuid) {
		this.uuid = uuid;
	}

	public Uuid getUuid() {
		return this.uuid;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setIothreadids(Iothreadids iothreadids) {
		this.iothreadids = iothreadids;
	}

	public Iothreadids getIothreadids() {
		return this.iothreadids;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setFeatures(Features features) {
		this.features = features;
	}

	public Features getFeatures() {
		return this.features;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setOn_crash(On_crash on_crash) {
		this.on_crash = on_crash;
	}

	public On_crash getOn_crash() {
		return this.on_crash;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setBlkiotune(Blkiotune blkiotune) {
		this.blkiotune = blkiotune;
	}

	public Blkiotune getBlkiotune() {
		return this.blkiotune;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setBootloader(Bootloader bootloader) {
		this.bootloader = bootloader;
	}

	public Bootloader getBootloader() {
		return this.bootloader;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setIdmap(Idmap idmap) {
		this.idmap = idmap;
	}

	public Idmap getIdmap() {
		return this.idmap;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setSysinfo(Sysinfo sysinfo) {
		this.sysinfo = sysinfo;
	}

	public Sysinfo getSysinfo() {
		return this.sysinfo;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setMemtune(Memtune memtune) {
		this.memtune = memtune;
	}

	public Memtune getMemtune() {
		return this.memtune;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setNumatune(Numatune numatune) {
		this.numatune = numatune;
	}

	public Numatune getNumatune() {
		return this.numatune;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setKeywrap(Keywrap keywrap) {
		this.keywrap = keywrap;
	}

	public Keywrap getKeywrap() {
		return this.keywrap;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setMemoryBacking(MemoryBacking memoryBacking) {
		this.memoryBacking = memoryBacking;
	}

	public MemoryBacking getMemoryBacking() {
		return this.memoryBacking;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setPerf(Perf perf) {
		this.perf = perf;
	}

	public Perf getPerf() {
		return this.perf;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setLaunchSecurity(LaunchSecurity launchSecurity) {
		this.launchSecurity = launchSecurity;
	}

	public LaunchSecurity getLaunchSecurity() {
		return this.launchSecurity;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setOn_poweroff(On_poweroff on_poweroff) {
		this.on_poweroff = on_poweroff;
	}

	public On_poweroff getOn_poweroff() {
		return this.on_poweroff;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setBootloader_args(Bootloader_args bootloader_args) {
		this.bootloader_args = bootloader_args;
	}

	public Bootloader_args getBootloader_args() {
		return this.bootloader_args;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setOs(Os os) {
		this.os = os;
	}

	public Os getOs() {
		return this.os;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setDevices(Devices devices) {
		this.devices = devices;
	}

	public Devices getDevices() {
		return this.devices;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setResource(Resource resource) {
		this.resource = resource;
	}

	public Resource getResource() {
		return this.resource;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setOn_reboot(On_reboot on_reboot) {
		this.on_reboot = on_reboot;
	}

	public On_reboot getOn_reboot() {
		return this.on_reboot;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void set_type(String _type) {
		this._type = _type;
	}

	public String get_type() {
		return this._type;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setCpu(Cpu cpu) {
		this.cpu = cpu;
	}

	public Cpu getCpu() {
		return this.cpu;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setClock(Clock clock) {
		this.clock = clock;
	}

	public Clock getClock() {
		return this.clock;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setVcpus(Vcpus vcpus) {
		this.vcpus = vcpus;
	}

	public Vcpus getVcpus() {
		return this.vcpus;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setCputune(Cputune cputune) {
		this.cputune = cputune;
	}

	public Cputune getCputune() {
		return this.cputune;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setGenid(Genid genid) {
		this.genid = genid;
	}

	public Genid getGenid() {
		return this.genid;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setIothreads(Iothreads iothreads) {
		this.iothreads = iothreads;
	}

	public Iothreads getIothreads() {
		return this.iothreads;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setName(Name name) {
		this.name = name;
	}

	public Name getName() {
		return this.name;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setCurrentMemory(CurrentMemory currentMemory) {
		this.currentMemory = currentMemory;
	}

	public CurrentMemory getCurrentMemory() {
		return this.currentMemory;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void set_id(String _id) {
		this._id = _id;
	}

	public String get_id() {
		return this._id;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setPm(Pm pm) {
		this.pm = pm;
	}

	public Pm getPm() {
		return this.pm;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Metadata {

		public Metadata() {

		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Memory {

		protected String _unit;

		protected String text;

		protected String _dumpCore;

		public Memory() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_unit(String _unit) {
			this._unit = _unit;
		}

		public String get_unit() {
			return this._unit;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_dumpCore(String _dumpCore) {
			this._dumpCore = _dumpCore;
		}

		public String get_dumpCore() {
			return this._dumpCore;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Vcpu {

		protected String _current;

		protected String _cpuset;

		protected String _placement;

		protected String text;

		public Vcpu() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_current(String _current) {
			this._current = _current;
		}

		public String get_current() {
			return this._current;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_cpuset(String _cpuset) {
			this._cpuset = _cpuset;
		}

		public String get_cpuset() {
			return this._cpuset;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_placement(String _placement) {
			this._placement = _placement;
		}

		public String get_placement() {
			return this._placement;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Seclabel {

		protected Imagelabel imagelabel;

		protected String _type;

		protected Baselabel baselabel;

		protected String _model;

		protected Label label;

		protected String _relabel;

		public Seclabel() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setImagelabel(Imagelabel imagelabel) {
			this.imagelabel = imagelabel;
		}

		public Imagelabel getImagelabel() {
			return this.imagelabel;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_type(String _type) {
			this._type = _type;
		}

		public String get_type() {
			return this._type;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setBaselabel(Baselabel baselabel) {
			this.baselabel = baselabel;
		}

		public Baselabel getBaselabel() {
			return this.baselabel;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_model(String _model) {
			this._model = _model;
		}

		public String get_model() {
			return this._model;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setLabel(Label label) {
			this.label = label;
		}

		public Label getLabel() {
			return this.label;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_relabel(String _relabel) {
			this._relabel = _relabel;
		}

		public String get_relabel() {
			return this._relabel;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Imagelabel {

			protected String text;

			public Imagelabel() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Baselabel {

			protected String text;

			public Baselabel() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Label {

			protected String text;

			public Label() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Description {

		protected String text;

		public Description() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Title {

		protected String text;

		public Title() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class MaxMemory {

		protected String _unit;

		protected String _slots;

		protected String text;

		public MaxMemory() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_unit(String _unit) {
			this._unit = _unit;
		}

		public String get_unit() {
			return this._unit;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_slots(String _slots) {
			this._slots = _slots;
		}

		public String get_slots() {
			return this._slots;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Uuid {

		protected String text;

		public Uuid() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Iothreadids {

		protected ArrayList<Iothread> iothread;

		public Iothreadids() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIothread(ArrayList<Iothread> iothread) {
			this.iothread = iothread;
		}

		public ArrayList<Iothread> getIothread() {
			return this.iothread;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iothread {

			protected String _id;

			public Iothread() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_id(String _id) {
				this._id = _id;
			}

			public String get_id() {
				return this._id;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Features {

		protected Gic gic;

		protected Htm htm;

		protected Capabilities capabilities;

		protected Kvm kvm;

		protected Apic apic;

		protected Viridian viridian;

		protected Pvspinlock pvspinlock;

		protected Vmport vmport;

		protected Vmcoreinfo vmcoreinfo;

		protected Hpt hpt;

		protected Nested_hv nested_hv;

		protected Privnet privnet;

		protected Smm smm;

		protected Msrs msrs;

		protected Pae pae;

		protected Acpi acpi;

		protected Hap hap;

		protected Ioapic ioapic;

		protected Pmu pmu;

		protected Hyperv hyperv;

		public Features() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setGic(Gic gic) {
			this.gic = gic;
		}

		public Gic getGic() {
			return this.gic;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHtm(Htm htm) {
			this.htm = htm;
		}

		public Htm getHtm() {
			return this.htm;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setCapabilities(Capabilities capabilities) {
			this.capabilities = capabilities;
		}

		public Capabilities getCapabilities() {
			return this.capabilities;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setKvm(Kvm kvm) {
			this.kvm = kvm;
		}

		public Kvm getKvm() {
			return this.kvm;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setApic(Apic apic) {
			this.apic = apic;
		}

		public Apic getApic() {
			return this.apic;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setViridian(Viridian viridian) {
			this.viridian = viridian;
		}

		public Viridian getViridian() {
			return this.viridian;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPvspinlock(Pvspinlock pvspinlock) {
			this.pvspinlock = pvspinlock;
		}

		public Pvspinlock getPvspinlock() {
			return this.pvspinlock;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVmport(Vmport vmport) {
			this.vmport = vmport;
		}

		public Vmport getVmport() {
			return this.vmport;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVmcoreinfo(Vmcoreinfo vmcoreinfo) {
			this.vmcoreinfo = vmcoreinfo;
		}

		public Vmcoreinfo getVmcoreinfo() {
			return this.vmcoreinfo;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHpt(Hpt hpt) {
			this.hpt = hpt;
		}

		public Hpt getHpt() {
			return this.hpt;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setNested_hv(Nested_hv nested_hv) {
			this.nested_hv = nested_hv;
		}

		public Nested_hv getNested_hv() {
			return this.nested_hv;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPrivnet(Privnet privnet) {
			this.privnet = privnet;
		}

		public Privnet getPrivnet() {
			return this.privnet;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSmm(Smm smm) {
			this.smm = smm;
		}

		public Smm getSmm() {
			return this.smm;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMsrs(Msrs msrs) {
			this.msrs = msrs;
		}

		public Msrs getMsrs() {
			return this.msrs;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPae(Pae pae) {
			this.pae = pae;
		}

		public Pae getPae() {
			return this.pae;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setAcpi(Acpi acpi) {
			this.acpi = acpi;
		}

		public Acpi getAcpi() {
			return this.acpi;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHap(Hap hap) {
			this.hap = hap;
		}

		public Hap getHap() {
			return this.hap;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIoapic(Ioapic ioapic) {
			this.ioapic = ioapic;
		}

		public Ioapic getIoapic() {
			return this.ioapic;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPmu(Pmu pmu) {
			this.pmu = pmu;
		}

		public Pmu getPmu() {
			return this.pmu;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHyperv(Hyperv hyperv) {
			this.hyperv = hyperv;
		}

		public Hyperv getHyperv() {
			return this.hyperv;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Gic {

			protected String _version;

			public Gic() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_version(String _version) {
				this._version = _version;
			}

			public String get_version() {
				return this._version;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Htm {

			protected String _state;

			public Htm() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Capabilities {

			protected Dac_read_Search dac_read_Search;

			protected Fsetid fsetid;

			protected Dac_override dac_override;

			protected Syslog syslog;

			protected String _policy;

			protected Net_raw net_raw;

			protected Mac_override mac_override;

			protected Setfcap setfcap;

			protected Mknod mknod;

			protected Sys_time sys_time;

			protected Sys_tty_config sys_tty_config;

			protected Net_broadcast net_broadcast;

			protected Setpcap setpcap;

			protected Ipc_lock ipc_lock;

			protected Net_bind_service net_bind_service;

			protected Wake_alarm wake_alarm;

			protected Linux_immutable linux_immutable;

			protected Sys_pacct sys_pacct;

			protected Ipc_owner ipc_owner;

			protected Net_admin net_admin;

			protected Setgid setgid;

			protected Sys_ptrace sys_ptrace;

			protected Chown chown;

			protected Sys_admin sys_admin;

			protected Sys_module sys_module;

			protected Sys_nice sys_nice;

			protected Kill kill;

			protected Audit_control audit_control;

			protected Setuid setuid;

			protected Fowner fowner;

			protected Sys_resource sys_resource;

			protected Sys_chroot sys_chroot;

			protected Sys_rawio sys_rawio;

			protected Audit_write audit_write;

			protected Block_suspend block_suspend;

			protected Lease lease;

			protected Sys_boot sys_boot;

			protected Mac_admin mac_admin;

			public Capabilities() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDac_read_Search(Dac_read_Search dac_read_Search) {
				this.dac_read_Search = dac_read_Search;
			}

			public Dac_read_Search getDac_read_Search() {
				return this.dac_read_Search;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setFsetid(Fsetid fsetid) {
				this.fsetid = fsetid;
			}

			public Fsetid getFsetid() {
				return this.fsetid;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDac_override(Dac_override dac_override) {
				this.dac_override = dac_override;
			}

			public Dac_override getDac_override() {
				return this.dac_override;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSyslog(Syslog syslog) {
				this.syslog = syslog;
			}

			public Syslog getSyslog() {
				return this.syslog;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_policy(String _policy) {
				this._policy = _policy;
			}

			public String get_policy() {
				return this._policy;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setNet_raw(Net_raw net_raw) {
				this.net_raw = net_raw;
			}

			public Net_raw getNet_raw() {
				return this.net_raw;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMac_override(Mac_override mac_override) {
				this.mac_override = mac_override;
			}

			public Mac_override getMac_override() {
				return this.mac_override;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSetfcap(Setfcap setfcap) {
				this.setfcap = setfcap;
			}

			public Setfcap getSetfcap() {
				return this.setfcap;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMknod(Mknod mknod) {
				this.mknod = mknod;
			}

			public Mknod getMknod() {
				return this.mknod;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_time(Sys_time sys_time) {
				this.sys_time = sys_time;
			}

			public Sys_time getSys_time() {
				return this.sys_time;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_tty_config(Sys_tty_config sys_tty_config) {
				this.sys_tty_config = sys_tty_config;
			}

			public Sys_tty_config getSys_tty_config() {
				return this.sys_tty_config;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setNet_broadcast(Net_broadcast net_broadcast) {
				this.net_broadcast = net_broadcast;
			}

			public Net_broadcast getNet_broadcast() {
				return this.net_broadcast;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSetpcap(Setpcap setpcap) {
				this.setpcap = setpcap;
			}

			public Setpcap getSetpcap() {
				return this.setpcap;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setIpc_lock(Ipc_lock ipc_lock) {
				this.ipc_lock = ipc_lock;
			}

			public Ipc_lock getIpc_lock() {
				return this.ipc_lock;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setNet_bind_service(Net_bind_service net_bind_service) {
				this.net_bind_service = net_bind_service;
			}

			public Net_bind_service getNet_bind_service() {
				return this.net_bind_service;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setWake_alarm(Wake_alarm wake_alarm) {
				this.wake_alarm = wake_alarm;
			}

			public Wake_alarm getWake_alarm() {
				return this.wake_alarm;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLinux_immutable(Linux_immutable linux_immutable) {
				this.linux_immutable = linux_immutable;
			}

			public Linux_immutable getLinux_immutable() {
				return this.linux_immutable;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_pacct(Sys_pacct sys_pacct) {
				this.sys_pacct = sys_pacct;
			}

			public Sys_pacct getSys_pacct() {
				return this.sys_pacct;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setIpc_owner(Ipc_owner ipc_owner) {
				this.ipc_owner = ipc_owner;
			}

			public Ipc_owner getIpc_owner() {
				return this.ipc_owner;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setNet_admin(Net_admin net_admin) {
				this.net_admin = net_admin;
			}

			public Net_admin getNet_admin() {
				return this.net_admin;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSetgid(Setgid setgid) {
				this.setgid = setgid;
			}

			public Setgid getSetgid() {
				return this.setgid;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_ptrace(Sys_ptrace sys_ptrace) {
				this.sys_ptrace = sys_ptrace;
			}

			public Sys_ptrace getSys_ptrace() {
				return this.sys_ptrace;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setChown(Chown chown) {
				this.chown = chown;
			}

			public Chown getChown() {
				return this.chown;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_admin(Sys_admin sys_admin) {
				this.sys_admin = sys_admin;
			}

			public Sys_admin getSys_admin() {
				return this.sys_admin;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_module(Sys_module sys_module) {
				this.sys_module = sys_module;
			}

			public Sys_module getSys_module() {
				return this.sys_module;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_nice(Sys_nice sys_nice) {
				this.sys_nice = sys_nice;
			}

			public Sys_nice getSys_nice() {
				return this.sys_nice;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setKill(Kill kill) {
				this.kill = kill;
			}

			public Kill getKill() {
				return this.kill;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAudit_control(Audit_control audit_control) {
				this.audit_control = audit_control;
			}

			public Audit_control getAudit_control() {
				return this.audit_control;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSetuid(Setuid setuid) {
				this.setuid = setuid;
			}

			public Setuid getSetuid() {
				return this.setuid;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setFowner(Fowner fowner) {
				this.fowner = fowner;
			}

			public Fowner getFowner() {
				return this.fowner;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_resource(Sys_resource sys_resource) {
				this.sys_resource = sys_resource;
			}

			public Sys_resource getSys_resource() {
				return this.sys_resource;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_chroot(Sys_chroot sys_chroot) {
				this.sys_chroot = sys_chroot;
			}

			public Sys_chroot getSys_chroot() {
				return this.sys_chroot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_rawio(Sys_rawio sys_rawio) {
				this.sys_rawio = sys_rawio;
			}

			public Sys_rawio getSys_rawio() {
				return this.sys_rawio;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAudit_write(Audit_write audit_write) {
				this.audit_write = audit_write;
			}

			public Audit_write getAudit_write() {
				return this.audit_write;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBlock_suspend(Block_suspend block_suspend) {
				this.block_suspend = block_suspend;
			}

			public Block_suspend getBlock_suspend() {
				return this.block_suspend;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLease(Lease lease) {
				this.lease = lease;
			}

			public Lease getLease() {
				return this.lease;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSys_boot(Sys_boot sys_boot) {
				this.sys_boot = sys_boot;
			}

			public Sys_boot getSys_boot() {
				return this.sys_boot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMac_admin(Mac_admin mac_admin) {
				this.mac_admin = mac_admin;
			}

			public Mac_admin getMac_admin() {
				return this.mac_admin;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Dac_read_Search {

				protected String _state;

				public Dac_read_Search() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Fsetid {

				protected String _state;

				public Fsetid() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Dac_override {

				protected String _state;

				public Dac_override() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Syslog {

				protected String _state;

				public Syslog() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Net_raw {

				protected String _state;

				public Net_raw() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mac_override {

				protected String _state;

				public Mac_override() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Setfcap {

				protected String _state;

				public Setfcap() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mknod {

				protected String _state;

				public Mknod() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_time {

				protected String _state;

				public Sys_time() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_tty_config {

				protected String _state;

				public Sys_tty_config() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Net_broadcast {

				protected String _state;

				public Net_broadcast() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Setpcap {

				protected String _state;

				public Setpcap() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Ipc_lock {

				protected String _state;

				public Ipc_lock() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Net_bind_service {

				protected String _state;

				public Net_bind_service() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Wake_alarm {

				protected String _state;

				public Wake_alarm() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Linux_immutable {

				protected String _state;

				public Linux_immutable() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_pacct {

				protected String _state;

				public Sys_pacct() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Ipc_owner {

				protected String _state;

				public Ipc_owner() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Net_admin {

				protected String _state;

				public Net_admin() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Setgid {

				protected String _state;

				public Setgid() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_ptrace {

				protected String _state;

				public Sys_ptrace() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Chown {

				protected String _state;

				public Chown() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_admin {

				protected String _state;

				public Sys_admin() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_module {

				protected String _state;

				public Sys_module() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_nice {

				protected String _state;

				public Sys_nice() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Kill {

				protected String _state;

				public Kill() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Audit_control {

				protected String _state;

				public Audit_control() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Setuid {

				protected String _state;

				public Setuid() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Fowner {

				protected String _state;

				public Fowner() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_resource {

				protected String _state;

				public Sys_resource() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_chroot {

				protected String _state;

				public Sys_chroot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_rawio {

				protected String _state;

				public Sys_rawio() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Audit_write {

				protected String _state;

				public Audit_write() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Block_suspend {

				protected String _state;

				public Block_suspend() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Lease {

				protected String _state;

				public Lease() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Sys_boot {

				protected String _state;

				public Sys_boot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mac_admin {

				protected String _state;

				public Mac_admin() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Kvm {

			protected Hidden hidden;

			public Kvm() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setHidden(Hidden hidden) {
				this.hidden = hidden;
			}

			public Hidden getHidden() {
				return this.hidden;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Hidden {

				protected String _state;

				public Hidden() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Apic {

			protected String _eoi;

			public Apic() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_eoi(String _eoi) {
				this._eoi = _eoi;
			}

			public String get_eoi() {
				return this._eoi;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Viridian {

			public Viridian() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Pvspinlock {

			protected String _state;

			public Pvspinlock() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vmport {

			protected String _state;

			public Vmport() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vmcoreinfo {

			protected String _state;

			public Vmcoreinfo() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hpt {

			protected Maxpagesize maxpagesize;

			protected String _resizing;

			public Hpt() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMaxpagesize(Maxpagesize maxpagesize) {
				this.maxpagesize = maxpagesize;
			}

			public Maxpagesize getMaxpagesize() {
				return this.maxpagesize;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_resizing(String _resizing) {
				this._resizing = _resizing;
			}

			public String get_resizing() {
				return this._resizing;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Maxpagesize {

				protected String _unit;

				protected String text;

				public Maxpagesize() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Nested_hv {

			protected String _state;

			public Nested_hv() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Privnet {

			public Privnet() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Smm {

			protected String _state;

			protected Tseg tseg;

			public Smm() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTseg(Tseg tseg) {
				this.tseg = tseg;
			}

			public Tseg getTseg() {
				return this.tseg;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Tseg {

				protected String _unit;

				protected String text;

				public Tseg() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Msrs {

			protected String _unknown;

			public Msrs() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_unknown(String _unknown) {
				this._unknown = _unknown;
			}

			public String get_unknown() {
				return this._unknown;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Pae {

			public Pae() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Acpi {

			public Acpi() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hap {

			protected String _state;

			public Hap() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Ioapic {

			protected String _driver;

			public Ioapic() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_driver(String _driver) {
				this._driver = _driver;
			}

			public String get_driver() {
				return this._driver;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Pmu {

			protected String _state;

			public Pmu() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hyperv {

			protected Vpindex vpindex;

			protected Ipi ipi;

			protected Stimer stimer;

			protected Reenlightenment reenlightenment;

			protected Runtime runtime;

			protected Evmcs evmcs;

			protected Spinlocks spinlocks;

			protected Tlbflush tlbflush;

			protected Synic synic;

			protected Relaxed relaxed;

			protected Vapic vapic;

			protected Vendor_id vendor_id;

			protected Reset reset;

			protected Frequencies frequencies;

			public Hyperv() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVpindex(Vpindex vpindex) {
				this.vpindex = vpindex;
			}

			public Vpindex getVpindex() {
				return this.vpindex;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setIpi(Ipi ipi) {
				this.ipi = ipi;
			}

			public Ipi getIpi() {
				return this.ipi;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setStimer(Stimer stimer) {
				this.stimer = stimer;
			}

			public Stimer getStimer() {
				return this.stimer;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setReenlightenment(Reenlightenment reenlightenment) {
				this.reenlightenment = reenlightenment;
			}

			public Reenlightenment getReenlightenment() {
				return this.reenlightenment;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRuntime(Runtime runtime) {
				this.runtime = runtime;
			}

			public Runtime getRuntime() {
				return this.runtime;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEvmcs(Evmcs evmcs) {
				this.evmcs = evmcs;
			}

			public Evmcs getEvmcs() {
				return this.evmcs;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSpinlocks(Spinlocks spinlocks) {
				this.spinlocks = spinlocks;
			}

			public Spinlocks getSpinlocks() {
				return this.spinlocks;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTlbflush(Tlbflush tlbflush) {
				this.tlbflush = tlbflush;
			}

			public Tlbflush getTlbflush() {
				return this.tlbflush;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSynic(Synic synic) {
				this.synic = synic;
			}

			public Synic getSynic() {
				return this.synic;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRelaxed(Relaxed relaxed) {
				this.relaxed = relaxed;
			}

			public Relaxed getRelaxed() {
				return this.relaxed;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVapic(Vapic vapic) {
				this.vapic = vapic;
			}

			public Vapic getVapic() {
				return this.vapic;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVendor_id(Vendor_id vendor_id) {
				this.vendor_id = vendor_id;
			}

			public Vendor_id getVendor_id() {
				return this.vendor_id;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setReset(Reset reset) {
				this.reset = reset;
			}

			public Reset getReset() {
				return this.reset;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setFrequencies(Frequencies frequencies) {
				this.frequencies = frequencies;
			}

			public Frequencies getFrequencies() {
				return this.frequencies;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Vpindex {

				protected String _state;

				public Vpindex() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Ipi {

				protected String _state;

				public Ipi() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Stimer {

				protected String _state;

				public Stimer() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Reenlightenment {

				protected String _state;

				public Reenlightenment() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Runtime {

				protected String _state;

				public Runtime() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Evmcs {

				protected String _state;

				public Evmcs() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Spinlocks {

				protected String _retries;
				
				protected String _state;

				public Spinlocks() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_retries(String _retries) {
					this._retries = _retries;
				}

				public String get_retries() {
					return this._retries;
				}

				public String get_state() {
					return _state;
				}

				public void set_state(String _state) {
					this._state = _state;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Tlbflush {

				protected String _state;

				public Tlbflush() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Synic {

				protected String _state;

				public Synic() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Relaxed {

				protected String _state;

				public Relaxed() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Vapic {

				protected String _state;

				public Vapic() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Vendor_id {

				protected String _value;

				public Vendor_id() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_value(String _value) {
					this._value = _value;
				}

				public String get_value() {
					return this._value;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Reset {

				protected String _state;

				public Reset() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Frequencies {

				protected String _state;

				public Frequencies() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class On_crash {

		protected String text;

		public On_crash() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Blkiotune {

		protected Weight weight;

		protected ArrayList<Device> device;

		public Blkiotune() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setWeight(Weight weight) {
			this.weight = weight;
		}

		public Weight getWeight() {
			return this.weight;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setDevice(ArrayList<Device> device) {
			this.device = device;
		}

		public ArrayList<Device> getDevice() {
			return this.device;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Weight {

			protected String text;

			public Weight() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Device {

			protected Path path;

			protected Write_bytes_sec write_bytes_sec;

			protected Write_iops_sec write_iops_sec;

			protected Weight weight;

			protected Read_bytes_sec read_bytes_sec;

			protected Read_iops_sec read_iops_sec;

			public Device() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setPath(Path path) {
				this.path = path;
			}

			public Path getPath() {
				return this.path;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setWrite_bytes_sec(Write_bytes_sec write_bytes_sec) {
				this.write_bytes_sec = write_bytes_sec;
			}

			public Write_bytes_sec getWrite_bytes_sec() {
				return this.write_bytes_sec;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setWrite_iops_sec(Write_iops_sec write_iops_sec) {
				this.write_iops_sec = write_iops_sec;
			}

			public Write_iops_sec getWrite_iops_sec() {
				return this.write_iops_sec;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setWeight(Weight weight) {
				this.weight = weight;
			}

			public Weight getWeight() {
				return this.weight;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRead_bytes_sec(Read_bytes_sec read_bytes_sec) {
				this.read_bytes_sec = read_bytes_sec;
			}

			public Read_bytes_sec getRead_bytes_sec() {
				return this.read_bytes_sec;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRead_iops_sec(Read_iops_sec read_iops_sec) {
				this.read_iops_sec = read_iops_sec;
			}

			public Read_iops_sec getRead_iops_sec() {
				return this.read_iops_sec;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Path {

				protected String text;

				public Path() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Write_bytes_sec {

				protected String text;

				public Write_bytes_sec() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Write_iops_sec {

				protected String text;

				public Write_iops_sec() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Weight {

				protected String text;

				public Weight() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Read_bytes_sec {

				protected String text;

				public Read_bytes_sec() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Read_iops_sec {

				protected String text;

				public Read_iops_sec() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Bootloader {

		protected String text;

		public Bootloader() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Idmap {

		protected ArrayList<Uid> uid;

		protected ArrayList<Gid> gid;

		public Idmap() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setUid(ArrayList<Uid> uid) {
			this.uid = uid;
		}

		public ArrayList<Uid> getUid() {
			return this.uid;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setGid(ArrayList<Gid> gid) {
			this.gid = gid;
		}

		public ArrayList<Gid> getGid() {
			return this.gid;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Uid {

			protected String _count;

			protected String _start;

			protected String _target;

			public Uid() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_count(String _count) {
				this._count = _count;
			}

			public String get_count() {
				return this._count;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_start(String _start) {
				this._start = _start;
			}

			public String get_start() {
				return this._start;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_target(String _target) {
				this._target = _target;
			}

			public String get_target() {
				return this._target;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Gid {

			protected String _count;

			protected String _start;

			protected String _target;

			public Gid() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_count(String _count) {
				this._count = _count;
			}

			public String get_count() {
				return this._count;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_start(String _start) {
				this._start = _start;
			}

			public String get_start() {
				return this._start;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_target(String _target) {
				this._target = _target;
			}

			public String get_target() {
				return this._target;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Sysinfo {

		protected ArrayList<Memory> memory;

		protected System system;

		protected ArrayList<BaseBoard> baseBoard;

		protected Bios bios;

		protected String _type;

		protected Chassis chassis;

		protected OemStrings oemStrings;

		protected ArrayList<Processor> processor;

		public Sysinfo() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemory(ArrayList<Memory> memory) {
			this.memory = memory;
		}

		public ArrayList<Memory> getMemory() {
			return this.memory;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSystem(System system) {
			this.system = system;
		}

		public System getSystem() {
			return this.system;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setBaseBoard(ArrayList<BaseBoard> baseBoard) {
			this.baseBoard = baseBoard;
		}

		public ArrayList<BaseBoard> getBaseBoard() {
			return this.baseBoard;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setBios(Bios bios) {
			this.bios = bios;
		}

		public Bios getBios() {
			return this.bios;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_type(String _type) {
			this._type = _type;
		}

		public String get_type() {
			return this._type;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setChassis(Chassis chassis) {
			this.chassis = chassis;
		}

		public Chassis getChassis() {
			return this.chassis;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setOemStrings(OemStrings oemStrings) {
			this.oemStrings = oemStrings;
		}

		public OemStrings getOemStrings() {
			return this.oemStrings;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setProcessor(ArrayList<Processor> processor) {
			this.processor = processor;
		}

		public ArrayList<Processor> getProcessor() {
			return this.processor;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memory {

			protected ArrayList<Entry> entry;

			public Memory() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class System {

			protected ArrayList<Entry> entry;

			public System() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class BaseBoard {

			protected ArrayList<Entry> entry;

			public BaseBoard() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Bios {

			protected ArrayList<Entry> entry;

			public Bios() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Chassis {

			protected ArrayList<Entry> entry;

			public Chassis() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class OemStrings {

			protected Entry entry;

			public OemStrings() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(Entry entry) {
				this.entry = entry;
			}

			public Entry getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Processor {

			protected ArrayList<Entry> entry;

			public Processor() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEntry(ArrayList<Entry> entry) {
				this.entry = entry;
			}

			public ArrayList<Entry> getEntry() {
				return this.entry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Entry {

				protected String _name;

				protected String text;

				public Entry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Memtune {

		protected Soft_limit soft_limit;

		protected Min_guarantee min_guarantee;

		protected Swap_hard_limit swap_hard_limit;

		protected Hard_limit hard_limit;

		public Memtune() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSoft_limit(Soft_limit soft_limit) {
			this.soft_limit = soft_limit;
		}

		public Soft_limit getSoft_limit() {
			return this.soft_limit;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMin_guarantee(Min_guarantee min_guarantee) {
			this.min_guarantee = min_guarantee;
		}

		public Min_guarantee getMin_guarantee() {
			return this.min_guarantee;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSwap_hard_limit(Swap_hard_limit swap_hard_limit) {
			this.swap_hard_limit = swap_hard_limit;
		}

		public Swap_hard_limit getSwap_hard_limit() {
			return this.swap_hard_limit;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHard_limit(Hard_limit hard_limit) {
			this.hard_limit = hard_limit;
		}

		public Hard_limit getHard_limit() {
			return this.hard_limit;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Soft_limit {

			protected String _unit;

			protected String text;

			public Soft_limit() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_unit(String _unit) {
				this._unit = _unit;
			}

			public String get_unit() {
				return this._unit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Min_guarantee {

			protected String _unit;

			protected String text;

			public Min_guarantee() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_unit(String _unit) {
				this._unit = _unit;
			}

			public String get_unit() {
				return this._unit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Swap_hard_limit {

			protected String _unit;

			protected String text;

			public Swap_hard_limit() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_unit(String _unit) {
				this._unit = _unit;
			}

			public String get_unit() {
				return this._unit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hard_limit {

			protected String _unit;

			protected String text;

			public Hard_limit() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_unit(String _unit) {
				this._unit = _unit;
			}

			public String get_unit() {
				return this._unit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Numatune {

		protected ArrayList<Memnode> memnode;

		protected Memory memory;

		public Numatune() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemnode(ArrayList<Memnode> memnode) {
			this.memnode = memnode;
		}

		public ArrayList<Memnode> getMemnode() {
			return this.memnode;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemory(Memory memory) {
			this.memory = memory;
		}

		public Memory getMemory() {
			return this.memory;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memnode {

			protected String _nodeset;

			protected String _cellid;

			protected String _mode;

			public Memnode() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_nodeset(String _nodeset) {
				this._nodeset = _nodeset;
			}

			public String get_nodeset() {
				return this._nodeset;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_cellid(String _cellid) {
				this._cellid = _cellid;
			}

			public String get_cellid() {
				return this._cellid;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memory {

			protected String _nodeset;

			protected String _placement;

			protected String _mode;

			public Memory() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_nodeset(String _nodeset) {
				this._nodeset = _nodeset;
			}

			public String get_nodeset() {
				return this._nodeset;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_placement(String _placement) {
				this._placement = _placement;
			}

			public String get_placement() {
				return this._placement;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Keywrap {

		protected ArrayList<Cipher> cipher;

		public Keywrap() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setCipher(ArrayList<Cipher> cipher) {
			this.cipher = cipher;
		}

		public ArrayList<Cipher> getCipher() {
			return this.cipher;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Cipher {

			protected String _name;

			protected String _state;

			public Cipher() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_state(String _state) {
				this._state = _state;
			}

			public String get_state() {
				return this._state;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class MemoryBacking {

		protected Hugepages hugepages;

		protected Discard discard;

		protected Allocation allocation;

		protected Access access;

		protected Nosharepages nosharepages;

		protected Source source;

		protected Locked locked;

		public MemoryBacking() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHugepages(Hugepages hugepages) {
			this.hugepages = hugepages;
		}

		public Hugepages getHugepages() {
			return this.hugepages;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setDiscard(Discard discard) {
			this.discard = discard;
		}

		public Discard getDiscard() {
			return this.discard;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setAllocation(Allocation allocation) {
			this.allocation = allocation;
		}

		public Allocation getAllocation() {
			return this.allocation;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setAccess(Access access) {
			this.access = access;
		}

		public Access getAccess() {
			return this.access;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setNosharepages(Nosharepages nosharepages) {
			this.nosharepages = nosharepages;
		}

		public Nosharepages getNosharepages() {
			return this.nosharepages;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSource(Source source) {
			this.source = source;
		}

		public Source getSource() {
			return this.source;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setLocked(Locked locked) {
			this.locked = locked;
		}

		public Locked getLocked() {
			return this.locked;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hugepages {

			protected ArrayList<Page> page;

			public Hugepages() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setPage(ArrayList<Page> page) {
				this.page = page;
			}

			public ArrayList<Page> getPage() {
				return this.page;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Page {

				protected String _size;

				protected String _unit;

				protected String _nodeset;

				public Page() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_size(String _size) {
					this._size = _size;
				}

				public String get_size() {
					return this._size;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_nodeset(String _nodeset) {
					this._nodeset = _nodeset;
				}

				public String get_nodeset() {
					return this._nodeset;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Discard {

			public Discard() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Allocation {

			protected String _mode;

			public Allocation() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Access {

			protected String _mode;

			public Access() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Nosharepages {

			public Nosharepages() {

			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Source {

			protected String _type;

			public Source() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_type() {
				return this._type;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Locked {

			public Locked() {

			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Perf {

		protected ArrayList<Event> event;

		public Perf() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setEvent(ArrayList<Event> event) {
			this.event = event;
		}

		public ArrayList<Event> getEvent() {
			return this.event;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Event {

			protected String _name;

			protected String _enabled;

			public Event() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_enabled(String _enabled) {
				this._enabled = _enabled;
			}

			public String get_enabled() {
				return this._enabled;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class LaunchSecurity {

		public LaunchSecurity() {

		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class On_poweroff {

		protected String text;

		public On_poweroff() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Bootloader_args {

		protected String text;

		public Bootloader_args() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Os {

		protected Init init;

		protected Bios bios;

		protected Kernel kernel;

		protected Loader loader;

		protected Initarg initarg;

		protected Type type;

		protected Initrd initrd;

		protected Smbios smbios;

		protected Cmdline cmdline;

		protected Dtb dtb;

		protected Nvram nvram;

		protected Inituser inituser;

		protected Acpi acpi;

		protected Bootmenu bootmenu;

		protected Initgroup initgroup;

		protected ArrayList<Boot> boot;
		
		protected Initdir initdir;

		protected ArrayList<Initenv> initenv;

		public Os() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInit(Init init) {
			this.init = init;
		}

		public Init getInit() {
			return this.init;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setBios(Bios bios) {
			this.bios = bios;
		}

		public Bios getBios() {
			return this.bios;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setKernel(Kernel kernel) {
			this.kernel = kernel;
		}

		public Kernel getKernel() {
			return this.kernel;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setLoader(Loader loader) {
			this.loader = loader;
		}

		public Loader getLoader() {
			return this.loader;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInitarg(Initarg initarg) {
			this.initarg = initarg;
		}

		public Initarg getInitarg() {
			return this.initarg;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setType(Type type) {
			this.type = type;
		}

		public Type getType() {
			return this.type;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInitrd(Initrd initrd) {
			this.initrd = initrd;
		}

		public Initrd getInitrd() {
			return this.initrd;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSmbios(Smbios smbios) {
			this.smbios = smbios;
		}

		public Smbios getSmbios() {
			return this.smbios;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setCmdline(Cmdline cmdline) {
			this.cmdline = cmdline;
		}

		public Cmdline getCmdline() {
			return this.cmdline;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setDtb(Dtb dtb) {
			this.dtb = dtb;
		}

		public Dtb getDtb() {
			return this.dtb;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setNvram(Nvram nvram) {
			this.nvram = nvram;
		}

		public Nvram getNvram() {
			return this.nvram;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInituser(Inituser inituser) {
			this.inituser = inituser;
		}

		public Inituser getInituser() {
			return this.inituser;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setAcpi(Acpi acpi) {
			this.acpi = acpi;
		}

		public Acpi getAcpi() {
			return this.acpi;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setBootmenu(Bootmenu bootmenu) {
			this.bootmenu = bootmenu;
		}

		public Bootmenu getBootmenu() {
			return this.bootmenu;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInitgroup(Initgroup initgroup) {
			this.initgroup = initgroup;
		}

		public Initgroup getInitgroup() {
			return this.initgroup;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInitdir(Initdir initdir) {
			this.initdir = initdir;
		}

		public ArrayList<Boot> getBoot() {
			return boot;
		}

		public void setBoot(ArrayList<Boot> boot) {
			this.boot = boot;
		}

		public Initdir getInitdir() {
			return this.initdir;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInitenv(ArrayList<Initenv> initenv) {
			this.initenv = initenv;
		}

		public ArrayList<Initenv> getInitenv() {
			return this.initenv;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Init {

			protected String text;

			public Init() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Bios {

			protected String _rebootTimeout;

			protected String _useserial;

			public Bios() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_rebootTimeout(String _rebootTimeout) {
				this._rebootTimeout = _rebootTimeout;
			}

			public String get_rebootTimeout() {
				return this._rebootTimeout;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_useserial(String _useserial) {
				this._useserial = _useserial;
			}

			public String get_useserial() {
				return this._useserial;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Kernel {

			protected String text;

			public Kernel() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Loader {

			protected String text;

			protected String _type;

			protected String _readonly;


			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_readonly() {
				return _readonly;
			}

			public void set_readonly(String _readonly) {
				this._readonly = _readonly;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Initarg {

			protected String text;

			public Initarg() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Type {

			protected String _machine;

			protected String text;

			protected String _arch;

			public Type() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_machine(String _machine) {
				this._machine = _machine;
			}

			public String get_machine() {
				return this._machine;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_arch(String _arch) {
				this._arch = _arch;
			}

			public String get_arch() {
				return this._arch;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Initrd {

			protected String text;

			public Initrd() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Smbios {

			protected String _mode;

			public Smbios() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Cmdline {

			protected String text;

			public Cmdline() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Dtb {

			protected String text;

			public Dtb() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Nvram {

			protected String text;

			public Nvram() {
				this.text = "strin template='string'>";

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Inituser {

			protected String text;

			public Inituser() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Acpi {

			protected ArrayList<Table> table;

			public Acpi() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTable(ArrayList<Table> table) {
				this.table = table;
			}

			public ArrayList<Table> getTable() {
				return this.table;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Table {

				protected String _type;

				protected String text;

				public Table() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Bootmenu {

			protected String _enable;

			protected String _timeout;

			public Bootmenu() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_enable(String _enable) {
				this._enable = _enable;
			}

			public String get_enable() {
				return this._enable;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_timeout(String _timeout) {
				this._timeout = _timeout;
			}

			public String get_timeout() {
				return this._timeout;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Initgroup {

			protected String text;

			public Initgroup() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Boot {

			protected String _dev;

			public Boot() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_dev(String _dev) {
				this._dev = _dev;
			}

			public String get_dev() {
				return this._dev;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Initdir {

			protected String text;

			public Initdir() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Initenv {

			protected String _name;

			protected String text;

			public Initenv() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Devices {

		protected ArrayList<Memory> memory;

		protected ArrayList<Redirfilter> redirfilter;

		protected ArrayList<Sound> sound;

		protected ArrayList<Channel> channel;
		
		protected Memballoon memballoon;

		protected ArrayList<Graphics> graphics;
		
		protected ArrayList<Video> video;
		
		protected ArrayList<_interface> _interface;
		
		protected Vsock vsock;

		protected ArrayList<Hostdev> hostdev;

		protected Nvram nvram;

		protected Iommu iommu;

		protected ArrayList<Parallel> parallel;

		protected ArrayList<Console> console;
		
		protected ArrayList<Controller> controller;
		
		protected ArrayList<Shmem> shmem;

		protected ArrayList<Redirdev> redirdev;

		protected ArrayList<Rng> rng;
		
		protected ArrayList<Smartcard> smartcard;

		protected ArrayList<Filesystem> filesystem;

		protected ArrayList<Panic> panic;

		protected ArrayList<Tpm> tpm;

		protected Emulator emulator;

		protected ArrayList<Input> input;

		protected ArrayList<Disk> disk;

		protected Watchdog watchdog;

		protected ArrayList<Hub> hub;

		protected ArrayList<Serial> serial;
		
		protected ArrayList<Lease> lease;
		

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemory(ArrayList<Memory> memory) {
			this.memory = memory;
		}

		public ArrayList<Memory> getMemory() {
			return this.memory;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setRedirfilter(ArrayList<Redirfilter> redirfilter) {
			this.redirfilter = redirfilter;
		}

		public ArrayList<Redirfilter> getRedirfilter() {
			return this.redirfilter;
		}

		public ArrayList<Controller> getController() {
			return controller;
		}

		public void setController(ArrayList<Controller> controller) {
			this.controller = controller;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSound(ArrayList<Sound> sound) {
			this.sound = sound;
		}

		public ArrayList<Sound> getSound() {
			return this.sound;
		}

		
		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemballoon(Memballoon memballoon) {
			this.memballoon = memballoon;
		}

		public Memballoon getMemballoon() {
			return this.memballoon;
		}
		
	
		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVsock(Vsock vsock) {
			this.vsock = vsock;
		}

		public ArrayList<_interface> get_interface() {
			return _interface;
		}

		public void set_interface(ArrayList<_interface> _interface) {
			this._interface = _interface;
		}


		public Vsock getVsock() {
			return this.vsock;
		}

		public ArrayList<Channel> getChannel() {
			return channel;
		}

		public void setChannel(ArrayList<Channel> channel) {
			this.channel = channel;
		}

		public ArrayList<Graphics> getGraphics() {
			return graphics;
		}

		public void setGraphics(ArrayList<Graphics> graphics) {
			this.graphics = graphics;
		}

		public ArrayList<Video> getVideo() {
			return video;
		}

		public void setVideo(ArrayList<Video> video) {
			this.video = video;
		}

		public ArrayList<Console> getConsole() {
			return console;
		}

		public void setConsole(ArrayList<Console> console) {
			this.console = console;
		}

		public ArrayList<Rng> getRng() {
			return rng;
		}

		public void setRng(ArrayList<Rng> rng) {
			this.rng = rng;
		}

		public ArrayList<Serial> getSerial() {
			return serial;
		}

		public void setSerial(ArrayList<Serial> serial) {
			this.serial = serial;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHostdev(ArrayList<Hostdev> hostdev) {
			this.hostdev = hostdev;
		}

		public ArrayList<Hostdev> getHostdev() {
			return this.hostdev;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setNvram(Nvram nvram) {
			this.nvram = nvram;
		}

		public Nvram getNvram() {
			return this.nvram;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIommu(Iommu iommu) {
			this.iommu = iommu;
		}

		public Iommu getIommu() {
			return this.iommu;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setParallel(ArrayList<Parallel> parallel) {
			this.parallel = parallel;
		}

		public ArrayList<Parallel> getParallel() {
			return this.parallel;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setShmem(ArrayList<Shmem> shmem) {
			this.shmem = shmem;
		}

		public ArrayList<Shmem> getShmem() {
			return this.shmem;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setRedirdev(ArrayList<Redirdev> redirdev) {
			this.redirdev = redirdev;
		}

		public ArrayList<Redirdev> getRedirdev() {
			return this.redirdev;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSmartcard(ArrayList<Smartcard> smartcard) {
			this.smartcard = smartcard;
		}

		public ArrayList<Smartcard> getSmartcard() {
			return this.smartcard;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setFilesystem(ArrayList<Filesystem> filesystem) {
			this.filesystem = filesystem;
		}

		public ArrayList<Filesystem> getFilesystem() {
			return this.filesystem;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPanic(ArrayList<Panic> panic) {
			this.panic = panic;
		}

		public ArrayList<Panic> getPanic() {
			return this.panic;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setTpm(ArrayList<Tpm> tpm) {
			this.tpm = tpm;
		}

		public ArrayList<Tpm> getTpm() {
			return this.tpm;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setEmulator(Emulator emulator) {
			this.emulator = emulator;
		}

		public Emulator getEmulator() {
			return this.emulator;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setInput(ArrayList<Input> input) {
			this.input = input;
		}

		public ArrayList<Input> getInput() {
			return this.input;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setDisk(ArrayList<Disk> disk) {
			this.disk = disk;
		}

		public ArrayList<Disk> getDisk() {
			return this.disk;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setWatchdog(Watchdog watchdog) {
			this.watchdog = watchdog;
		}

		public Watchdog getWatchdog() {
			return this.watchdog;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setHub(ArrayList<Hub> hub) {
			this.hub = hub;
		}

		public ArrayList<Hub> getHub() {
			return this.hub;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setLease(ArrayList<Lease> lease) {
			this.lease = lease;
		}

		public ArrayList<Lease> getLease() {
			return this.lease;
		}

		
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memory {

			protected String _discard;

			protected Address address;

			protected String _access;

			protected Alias alias;

			protected String _model;

			protected Source source;

			protected Target target;

			public Memory() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_discard(String _discard) {
				this._discard = _discard;
			}

			public String get_discard() {
				return this._discard;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_access(String _access) {
				this._access = _access;
			}

			public String get_access() {
				return this._access;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected Path path;

				protected Pmem pmem;

				protected Alignsize alignsize;

				protected Nodemask nodemask;

				protected Pagesize pagesize;

				public Source() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setPath(Path path) {
					this.path = path;
				}

				public Path getPath() {
					return this.path;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setPmem(Pmem pmem) {
					this.pmem = pmem;
				}

				public Pmem getPmem() {
					return this.pmem;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setAlignsize(Alignsize alignsize) {
					this.alignsize = alignsize;
				}

				public Alignsize getAlignsize() {
					return this.alignsize;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setNodemask(Nodemask nodemask) {
					this.nodemask = nodemask;
				}

				public Nodemask getNodemask() {
					return this.nodemask;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setPagesize(Pagesize pagesize) {
					this.pagesize = pagesize;
				}

				public Pagesize getPagesize() {
					return this.pagesize;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Path {

					protected String text;

					public Path() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Pmem {

					public Pmem() {

					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Alignsize {

					protected String _unit;

					protected String text;

					public Alignsize() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_unit(String _unit) {
						this._unit = _unit;
					}

					public String get_unit() {
						return this._unit;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Nodemask {

					protected String text;

					public Nodemask() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Pagesize {

					protected String _unit;

					protected String text;

					public Pagesize() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_unit(String _unit) {
						this._unit = _unit;
					}

					public String get_unit() {
						return this._unit;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected Node node;

				protected Readonly readonly;

				protected Size size;

				protected Label label;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setNode(Node node) {
					this.node = node;
				}

				public Node getNode() {
					return this.node;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setReadonly(Readonly readonly) {
					this.readonly = readonly;
				}

				public Readonly getReadonly() {
					return this.readonly;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSize(Size size) {
					this.size = size;
				}

				public Size getSize() {
					return this.size;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setLabel(Label label) {
					this.label = label;
				}

				public Label getLabel() {
					return this.label;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Node {

					protected String text;

					public Node() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Readonly {

					public Readonly() {

					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Size {

					protected String _unit;

					protected String text;

					public Size() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_unit(String _unit) {
						this._unit = _unit;
					}

					public String get_unit() {
						return this._unit;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Label {

					protected Size size;

					public Label() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setSize(Size size) {
						this.size = size;
					}

					public Size getSize() {
						return this.size;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Size {

						protected String _unit;

						protected String text;

						public Size() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_unit(String _unit) {
							this._unit = _unit;
						}

						public String get_unit() {
							return this._unit;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void setText(String text) {
							this.text = text;
						}

						public String getText() {
							return this.text;
						}
					}
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Redirfilter {

			protected ArrayList<Usbdev> usbdev;

			public Redirfilter() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setUsbdev(ArrayList<Usbdev> usbdev) {
				this.usbdev = usbdev;
			}

			public ArrayList<Usbdev> getUsbdev() {
				return this.usbdev;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Usbdev {

				protected String _vendor;

				protected String _class;

				protected String _allow;

				protected String _product;

				protected String _version;

				public Usbdev() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vendor(String _vendor) {
					this._vendor = _vendor;
				}

				public String get_vendor() {
					return this._vendor;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_class(String _class) {
					this._class = _class;
				}

				public String get_class() {
					return this._class;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_allow(String _allow) {
					this._allow = _allow;
				}

				public String get_allow() {
					return this._allow;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_product(String _product) {
					this._product = _product;
				}

				public String get_product() {
					return this._product;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_version(String _version) {
					this._version = _version;
				}

				public String get_version() {
					return this._version;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Sound {

			protected ArrayList<Codec> codec;

			protected Address address;

			protected Alias alias;

			protected String _model;

			public Sound() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCodec(ArrayList<Codec> codec) {
				this.codec = codec;
			}

			public ArrayList<Codec> getCodec() {
				return this.codec;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Codec {

				protected String _type;

				public Codec() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _type;
				protected String _slot;
				protected String _bus;
				protected String _function;
				protected String _domain;

				public Address() {
				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Channel {

			protected String _type;
			
			protected Protocol protocol;

			protected Address address;

			protected Log log;

			protected Alias alias;

			protected Source source;

			protected Target target;

			public Channel() {

			}

			
			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLog(Log log) {
				this.log = log;
			}

			public Log getLog() {
				return this.log;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
				
				protected String _controller;
				
				protected String _port;
				
				protected String _type;
				
				public Address() {

				}

				
				public String get_controller() {
					return _controller;
				}

				public void set_controller(String _controller) {
					this._controller = _controller;
				}

				public String get_port() {
					return _port;
				}



				public void set_port(String _port) {
					this._port = _port;
				}



				public String get_type() {
					return _type;
				}



				public void set_type(String _type) {
					this._type = _type;
				}



				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Log {

				protected String _file;

				protected String _append;

				public Log() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_append(String _append) {
					this._append = _append;
				}

				public String get_append() {
					return this._append;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected String _mode;
				
				protected String _path;
				
				public Source() {
					
				}

				public String get_mode() {
					return _mode;
				}

				public void set_mode(String _mode) {
					this._mode = _mode;
				}

				public String get_path() {
					return _path;
				}

				public void set_path(String _path) {
					this._path = _path;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _name;
				
				protected String _state;
				
				protected String _type;
				
				public Target() {

				}

				public String get_name() {
					return _name;
				}

				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_state() {
					return _state;
				}

				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memballoon {

			protected Address address;

			protected Driver driver;

			protected Stats stats;

			protected Alias alias;

			protected String _model;

			protected String _autodeflate;

			public Memballoon() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setStats(Stats stats) {
				this.stats = stats;
			}

			public Stats getStats() {
				return this.stats;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_autodeflate(String _autodeflate) {
				this._autodeflate = _autodeflate;
			}

			public String get_autodeflate() {
				return this._autodeflate;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				 protected String _bus;
				 
				 protected String _domain;
				 
				 protected String _function;
				 
				 protected String _slot;
				 
				 protected String _type;
				
				public Address() {

				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _iommu;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Stats {

				protected String _period;

				public Stats() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_period(String _period) {
					this._period = _period;
				}

				public String get_period() {
					return this._period;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Graphics {

			protected String _autoport;
			
			protected String _listen;
	        
			protected String _port;
			
			protected String _type;
			
			protected Listen listen;
			
			protected Image image;
			
			public Image getImage() {
				return image;
			}

			public void setImage(Image image) {
				this.image = image;
			}

			public Listen getListen() {
				return listen;
			}

			public void setListen(Listen listen) {
				this.listen = listen;
			}

			public String get_listen() {
				return _listen;
			}

			public void set_listen(String _listen) {
				this._listen = _listen;
			}

			public String get_port() {
				return _port;
			}

			public void set_port(String _port) {
				this._port = _port;
			}

			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_autoport() {
				return _autoport;
			}

			public void set_autoport(String _autoport) {
				this._autoport = _autoport;
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Listen {
				
				protected String _address;
				
				protected String _type;

				public Listen() {
					super();
					// TODO Auto-generated constructor stub
				}

				public String get_address() {
					return _address;
				}

				public void set_address(String _address) {
					this._address = _address;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Image {
				protected String _compression;

				public String get_compression() {
					return _compression;
				}

				public void set_compression(String _compression) {
					this._compression = _compression;
				}
				
			}
			
		}

		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Video {

			protected Address address;

			protected Driver driver;

			protected Alias alias;

			protected Model model;

			public Video() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setModel(Model model) {
				this.model = model;
			}

			public Model getModel() {
				return this.model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
				
				protected String _domain;
				
				protected String _function;
				
				protected String _slot;
				
				protected String _type;
				
				public Address() {

				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _vgaconf;

				protected String _iommu;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vgaconf(String _vgaconf) {
					this._vgaconf = _vgaconf;
				}

				public String get_vgaconf() {
					return this._vgaconf;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Model {

				protected String _heads;

				protected String _vgamem;

				protected Acceleration acceleration;

				protected String _ram;

				protected String _vram;

				protected String _vram64;

				protected String _type;

				protected String _primary;

				public Model() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_heads(String _heads) {
					this._heads = _heads;
				}

				public String get_heads() {
					return this._heads;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vgamem(String _vgamem) {
					this._vgamem = _vgamem;
				}

				public String get_vgamem() {
					return this._vgamem;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setAcceleration(Acceleration acceleration) {
					this.acceleration = acceleration;
				}

				public Acceleration getAcceleration() {
					return this.acceleration;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ram(String _ram) {
					this._ram = _ram;
				}

				public String get_ram() {
					return this._ram;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vram(String _vram) {
					this._vram = _vram;
				}

				public String get_vram() {
					return this._vram;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vram64(String _vram64) {
					this._vram64 = _vram64;
				}

				public String get_vram64() {
					return this._vram64;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_primary(String _primary) {
					this._primary = _primary;
				}

				public String get_primary() {
					return this._primary;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Acceleration {

					protected String _accel3d;

					protected String _accel2d;

					public Acceleration() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_accel3d(String _accel3d) {
						this._accel3d = _accel3d;
					}

					public String get_accel3d() {
						return this._accel3d;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_accel2d(String _accel2d) {
						this._accel2d = _accel2d;
					}

					public String get_accel2d() {
						return this._accel2d;
					}
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class _interface {

			protected Address address;

			protected Bandwidth bandwidth;

			protected ArrayList<Ip> ip;

			protected Coalesce coalesce;

			protected Link link;

			protected Source source;

			protected Filterref filterref;

			protected Mac mac;

			protected Script script;

			protected Tune tune;

			protected Mtu mtu;

			protected Target target;

			protected Rom rom;

			protected ArrayList<Route> route;

			protected Driver driver;

			protected Vlan vlan;

			protected String _managed;

			protected String _trustGuestRxFilters;

			protected Alias alias;

			protected Backend backend;

			protected Guest guest;

			protected Model model;

			protected Boot boot;
			
			protected String _type;

			protected Virtualport virtualport;

			public _interface() {

			}

			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}



			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBandwidth(Bandwidth bandwidth) {
				this.bandwidth = bandwidth;
			}

			public Bandwidth getBandwidth() {
				return this.bandwidth;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setIp(ArrayList<Ip> ip) {
				this.ip = ip;
			}

			public ArrayList<Ip> getIp() {
				return this.ip;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCoalesce(Coalesce coalesce) {
				this.coalesce = coalesce;
			}

			public Coalesce getCoalesce() {
				return this.coalesce;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLink(Link link) {
				this.link = link;
			}

			public Link getLink() {
				return this.link;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setFilterref(Filterref filterref) {
				this.filterref = filterref;
			}

			public Filterref getFilterref() {
				return this.filterref;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMac(Mac mac) {
				this.mac = mac;
			}

			public Mac getMac() {
				return this.mac;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setScript(Script script) {
				this.script = script;
			}

			public Script getScript() {
				return this.script;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTune(Tune tune) {
				this.tune = tune;
			}

			public Tune getTune() {
				return this.tune;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMtu(Mtu mtu) {
				this.mtu = mtu;
			}

			public Mtu getMtu() {
				return this.mtu;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRom(Rom rom) {
				this.rom = rom;
			}

			public Rom getRom() {
				return this.rom;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRoute(ArrayList<Route> route) {
				this.route = route;
			}

			public ArrayList<Route> getRoute() {
				return this.route;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVlan(Vlan vlan) {
				this.vlan = vlan;
			}

			public Vlan getVlan() {
				return this.vlan;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_managed(String _managed) {
				this._managed = _managed;
			}

			public String get_managed() {
				return this._managed;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_trustGuestRxFilters(String _trustGuestRxFilters) {
				this._trustGuestRxFilters = _trustGuestRxFilters;
			}

			public String get_trustGuestRxFilters() {
				return this._trustGuestRxFilters;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBackend(Backend backend) {
				this.backend = backend;
			}

			public Backend getBackend() {
				return this.backend;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setGuest(Guest guest) {
				this.guest = guest;
			}

			public Guest getGuest() {
				return this.guest;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setModel(Model model) {
				this.model = model;
			}

			public Model getModel() {
				return this.model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBoot(Boot boot) {
				this.boot = boot;
			}

			public Boot getBoot() {
				return this.boot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVirtualport(Virtualport virtualport) {
				this.virtualport = virtualport;
			}

			public Virtualport getVirtualport() {
				return this.virtualport;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {
				
				protected String _bus;
				
				protected String _domain;
				
				protected String _function;
				
				protected String _slot;
				
				protected String _type;
				
				public Address() {

				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Bandwidth {

				protected Inbound inbound;

				protected Outbound outbound;

				public Bandwidth() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setInbound(Inbound inbound) {
					this.inbound = inbound;
				}

				public Inbound getInbound() {
					return this.inbound;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setOutbound(Outbound outbound) {
					this.outbound = outbound;
				}

				public Outbound getOutbound() {
					return this.outbound;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Inbound {

					protected String _floor;

					protected String _peak;

					protected String _average;

					protected String _burst;

					public Inbound() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_floor(String _floor) {
						this._floor = _floor;
					}

					public String get_floor() {
						return this._floor;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_peak(String _peak) {
						this._peak = _peak;
					}

					public String get_peak() {
						return this._peak;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_average(String _average) {
						this._average = _average;
					}

					public String get_average() {
						return this._average;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_burst(String _burst) {
						this._burst = _burst;
					}

					public String get_burst() {
						return this._burst;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Outbound {

					protected String _floor;

					protected String _peak;

					protected String _average;

					protected String _burst;

					public Outbound() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_floor(String _floor) {
						this._floor = _floor;
					}

					public String get_floor() {
						return this._floor;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_peak(String _peak) {
						this._peak = _peak;
					}

					public String get_peak() {
						return this._peak;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_average(String _average) {
						this._average = _average;
					}

					public String get_average() {
						return this._average;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_burst(String _burst) {
						this._burst = _burst;
					}

					public String get_burst() {
						return this._burst;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Ip {

				protected String _address;

				protected String _prefix;

				protected String _family;

				protected String _peer;

				public Ip() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_address(String _address) {
					this._address = _address;
				}

				public String get_address() {
					return this._address;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_prefix(String _prefix) {
					this._prefix = _prefix;
				}

				public String get_prefix() {
					return this._prefix;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_family(String _family) {
					this._family = _family;
				}

				public String get_family() {
					return this._family;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_peer(String _peer) {
					this._peer = _peer;
				}

				public String get_peer() {
					return this._peer;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Coalesce {

				protected Rx rx;

				public Coalesce() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRx(Rx rx) {
					this.rx = rx;
				}

				public Rx getRx() {
					return this.rx;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Rx {

					protected Frames frames;

					public Rx() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setFrames(Frames frames) {
						this.frames = frames;
					}

					public Frames getFrames() {
						return this.frames;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Frames {

						protected String _max;

						public Frames() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_max(String _max) {
							this._max = _max;
						}

						public String get_max() {
							return this._max;
						}
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Link {

				protected String _state;

				public Link() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_state(String _state) {
					this._state = _state;
				}

				public String get_state() {
					return this._state;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {
				
				protected String _type;
				
				protected String _dev;
				
				protected String _path;
				
				protected String _mode;

				protected String _bridge;
				
				protected String _network;

				
				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_dev() {
					return _dev;
				}

				public void set_dev(String _dev) {
					this._dev = _dev;
				}

				public String get_path() {
					return _path;
				}

				public void set_path(String _path) {
					this._path = _path;
				}

				public String get_mode() {
					return _mode;
				}

				public void set_mode(String _mode) {
					this._mode = _mode;
				}


				public String get_bridge() {
					return _bridge;
				}

				public void set_bridge(String _bridge) {
					this._bridge = _bridge;
				}

				public String get_network() {
					return _network;
				}

				public void set_network(String _network) {
					this._network = _network;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Filterref {

				protected ArrayList<Parameter> parameter;

				protected String _filter;

				public Filterref() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setParameter(ArrayList<Parameter> parameter) {
					this.parameter = parameter;
				}

				public ArrayList<Parameter> getParameter() {
					return this.parameter;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_filter(String _filter) {
					this._filter = _filter;
				}

				public String get_filter() {
					return this._filter;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Parameter {

					protected String _name;

					protected String _value;

					public Parameter() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_name(String _name) {
						this._name = _name;
					}

					public String get_name() {
						return this._name;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_value(String _value) {
						this._value = _value;
					}

					public String get_value() {
						return this._value;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mac {

				protected String _address;

				public Mac() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_address(String _address) {
					this._address = _address;
				}

				public String get_address() {
					return this._address;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Script {

				protected String _path;

				public Script() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_path(String _path) {
					this._path = _path;
				}

				public String get_path() {
					return this._path;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Tune {

				protected Sndbuf sndbuf;

				public Tune() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSndbuf(Sndbuf sndbuf) {
					this.sndbuf = sndbuf;
				}

				public Sndbuf getSndbuf() {
					return this.sndbuf;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Sndbuf {

					protected String text;

					public Sndbuf() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mtu {

				protected String _size;

				public Mtu() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_size(String _size) {
					this._size = _size;
				}

				public String get_size() {
					return this._size;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _dev;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_dev(String _dev) {
					this._dev = _dev;
				}

				public String get_dev() {
					return this._dev;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Rom {

				protected String _file;

				protected String _bar;

				protected String _enabled;

				public Rom() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_bar(String _bar) {
					this._bar = _bar;
				}

				public String get_bar() {
					return this._bar;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_enabled(String _enabled) {
					this._enabled = _enabled;
				}

				public String get_enabled() {
					return this._enabled;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Route {

				protected String _address;

				protected String _prefix;

				protected String _netmask;

				protected String _metric;

				protected String _family;

				protected String _gateway;

				public Route() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_address(String _address) {
					this._address = _address;
				}

				public String get_address() {
					return this._address;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_prefix(String _prefix) {
					this._prefix = _prefix;
				}

				public String get_prefix() {
					return this._prefix;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_netmask(String _netmask) {
					this._netmask = _netmask;
				}

				public String get_netmask() {
					return this._netmask;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_metric(String _metric) {
					this._metric = _metric;
				}

				public String get_metric() {
					return this._metric;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_family(String _family) {
					this._family = _family;
				}

				public String get_family() {
					return this._family;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_gateway(String _gateway) {
					this._gateway = _gateway;
				}

				public String get_gateway() {
					return this._gateway;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _name;

				protected String _queues;

				protected String _txmode;

				protected String _tx_queue_size;

				protected String _iommu;

				protected Host host;

				protected String _ioeventfd;

				protected Guest guest;

				protected String _event_idx;

				protected String _ats;

				protected String _rx_queue_size;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_queues(String _queues) {
					this._queues = _queues;
				}

				public String get_queues() {
					return this._queues;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_txmode(String _txmode) {
					this._txmode = _txmode;
				}

				public String get_txmode() {
					return this._txmode;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_tx_queue_size(String _tx_queue_size) {
					this._tx_queue_size = _tx_queue_size;
				}

				public String get_tx_queue_size() {
					return this._tx_queue_size;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setHost(Host host) {
					this.host = host;
				}

				public Host getHost() {
					return this.host;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ioeventfd(String _ioeventfd) {
					this._ioeventfd = _ioeventfd;
				}

				public String get_ioeventfd() {
					return this._ioeventfd;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setGuest(Guest guest) {
					this.guest = guest;
				}

				public Guest getGuest() {
					return this.guest;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_event_idx(String _event_idx) {
					this._event_idx = _event_idx;
				}

				public String get_event_idx() {
					return this._event_idx;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_rx_queue_size(String _rx_queue_size) {
					this._rx_queue_size = _rx_queue_size;
				}

				public String get_rx_queue_size() {
					return this._rx_queue_size;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Host {

					protected String _tso4;

					protected String _ufo;

					protected String _tso6;

					protected String _mrg_rxbuf;

					protected String _gso;

					protected String _ecn;

					protected String _csum;

					public Host() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_tso4(String _tso4) {
						this._tso4 = _tso4;
					}

					public String get_tso4() {
						return this._tso4;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_ufo(String _ufo) {
						this._ufo = _ufo;
					}

					public String get_ufo() {
						return this._ufo;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_tso6(String _tso6) {
						this._tso6 = _tso6;
					}

					public String get_tso6() {
						return this._tso6;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_mrg_rxbuf(String _mrg_rxbuf) {
						this._mrg_rxbuf = _mrg_rxbuf;
					}

					public String get_mrg_rxbuf() {
						return this._mrg_rxbuf;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_gso(String _gso) {
						this._gso = _gso;
					}

					public String get_gso() {
						return this._gso;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_ecn(String _ecn) {
						this._ecn = _ecn;
					}

					public String get_ecn() {
						return this._ecn;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_csum(String _csum) {
						this._csum = _csum;
					}

					public String get_csum() {
						return this._csum;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Guest {

					protected String _tso4;

					protected String _ufo;

					protected String _tso6;

					protected String _ecn;

					protected String _csum;

					public Guest() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_tso4(String _tso4) {
						this._tso4 = _tso4;
					}

					public String get_tso4() {
						return this._tso4;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_ufo(String _ufo) {
						this._ufo = _ufo;
					}

					public String get_ufo() {
						return this._ufo;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_tso6(String _tso6) {
						this._tso6 = _tso6;
					}

					public String get_tso6() {
						return this._tso6;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_ecn(String _ecn) {
						this._ecn = _ecn;
					}

					public String get_ecn() {
						return this._ecn;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_csum(String _csum) {
						this._csum = _csum;
					}

					public String get_csum() {
						return this._csum;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Vlan {

				protected String _trunk;

				protected ArrayList<Tag> tag;

				public Vlan() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_trunk(String _trunk) {
					this._trunk = _trunk;
				}

				public String get_trunk() {
					return this._trunk;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTag(ArrayList<Tag> tag) {
					this.tag = tag;
				}

				public ArrayList<Tag> getTag() {
					return this.tag;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Tag {

					protected String _nativeMode;

					protected String _id;

					public Tag() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_nativeMode(String _nativeMode) {
						this._nativeMode = _nativeMode;
					}

					public String get_nativeMode() {
						return this._nativeMode;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_id(String _id) {
						this._id = _id;
					}

					public String get_id() {
						return this._id;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Backend {

				protected String _vhost;

				protected String _tap;

				public Backend() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vhost(String _vhost) {
					this._vhost = _vhost;
				}

				public String get_vhost() {
					return this._vhost;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_tap(String _tap) {
					this._tap = _tap;
				}

				public String get_tap() {
					return this._tap;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Guest {

				protected String _actual;

				protected String _dev;

				public Guest() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_actual(String _actual) {
					this._actual = _actual;
				}

				public String get_actual() {
					return this._actual;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_dev(String _dev) {
					this._dev = _dev;
				}

				public String get_dev() {
					return this._dev;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Model {

				protected String _type;

				public Model() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Boot {

				protected String _loadparm;

				protected String _order;

				public Boot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_loadparm(String _loadparm) {
					this._loadparm = _loadparm;
				}

				public String get_loadparm() {
					return this._loadparm;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_order(String _order) {
					this._order = _order;
				}

				public String get_order() {
					return this._order;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Virtualport {

				protected String _type;
				
				protected Parameters parameters;

				public Virtualport() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setParameters(Parameters parameters) {
					this.parameters = parameters;
				}

				public Parameters getParameters() {
					return this.parameters;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}


				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Parameters {

					protected String __interfaceid;
					
					protected String _profileid;

					public String get_profileid() {
						return _profileid;
					}

					public void set_profileid(String _profileid) {
						this._profileid = _profileid;
					}

					public Parameters() {

					}

					public String get__interfaceid() {
						return __interfaceid;
					}

					public void set__interfaceid(String __interfaceid) {
						this.__interfaceid = __interfaceid;
					}
					
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vsock {

			protected Address address;

			protected Alias alias;

			protected String _model;

			protected Cid cid;

			public Vsock() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCid(Cid cid) {
				this.cid = cid;
			}

			public Cid getCid() {
				return this.cid;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Cid {

				protected String _address;

				protected String _auto;

				public Cid() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_address(String _address) {
					this._address = _address;
				}

				public String get_address() {
					return this._address;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_auto(String _auto) {
					this._auto = _auto;
				}

				public String get_auto() {
					return this._auto;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hostdev {

			protected Rom rom;

			protected Address address;

			protected String _managed;

			protected Alias alias;

			protected Boot boot;
			
			protected String _mode;
			
			protected String _type;
			
			protected Source source;
			
			protected Driver driver;

			public Driver getDriver() {
				return driver;
			}

			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Source getSource() {
				return source;
			}

			public void setSource(Source source) {
				this.source = source;
			}

			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_mode() {
				return _mode;
			}

			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public Hostdev() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRom(Rom rom) {
				this.rom = rom;
			}

			public Rom getRom() {
				return this.rom;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_managed(String _managed) {
				this._managed = _managed;
			}

			public String get_managed() {
				return this._managed;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBoot(Boot boot) {
				this.boot = boot;
			}

			public Boot getBoot() {
				return this.boot;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Rom {

				protected String _file;

				protected String _bar;

				protected String _enabled;

				public Rom() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_bar(String _bar) {
					this._bar = _bar;
				}

				public String get_bar() {
					return this._bar;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_enabled(String _enabled) {
					this._enabled = _enabled;
				}

				public String get_enabled() {
					return this._enabled;
				}
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {
				
				protected String _name;

				public String get_name() {
					return _name;
				}

				public void set_name(String _name) {
					this._name = _name;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {
				
				protected String _bus;
				
				protected String _device;
				
				protected String _type;
				
				protected String _port;
				
				protected String _domain;
				
				protected String _slot;
				
				protected String _function;

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public Address() {

				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_device() {
					return _device;
				}

				public void set_device(String _device) {
					this._device = _device;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_port() {
					return _port;
				}

				public void set_port(String _port) {
					this._port = _port;
				}
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {
				
				protected Address address;

				public Address getAddress() {
					return address;
				}

				public void setAddress(Address address) {
					this.address = address;
				}
				
				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Address {
					protected String _bus;
					
					protected String _device;
					
					protected String _domain;
					
					protected String _slot;
					
					protected String _function;

					public String get_domain() {
						return _domain;
					}

					public void set_domain(String _domain) {
						this._domain = _domain;
					}

					public String get_slot() {
						return _slot;
					}

					public void set_slot(String _slot) {
						this._slot = _slot;
					}

					public String get_function() {
						return _function;
					}

					public void set_function(String _function) {
						this._function = _function;
					}

					public String get_bus() {
						return _bus;
					}

					public void set_bus(String _bus) {
						this._bus = _bus;
					}

					public String get_device() {
						return _device;
					}

					public void set_device(String _device) {
						this._device = _device;
					}
					
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Boot {

				protected String _loadparm;

				protected String _order;

				public Boot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_loadparm(String _loadparm) {
					this._loadparm = _loadparm;
				}

				public String get_loadparm() {
					return this._loadparm;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_order(String _order) {
					this._order = _order;
				}

				public String get_order() {
					return this._order;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Nvram {

			protected Address address;

			protected Alias alias;

			public Nvram() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iommu {

			protected Driver driver;

			protected String _model;

			public Iommu() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _caching_mode;

				protected String _eim;

				protected String _iotlb;

				protected String _intremap;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_caching_mode(String _caching_mode) {
					this._caching_mode = _caching_mode;
				}

				public String get_caching_mode() {
					return this._caching_mode;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_eim(String _eim) {
					this._eim = _eim;
				}

				public String get_eim() {
					return this._eim;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iotlb(String _iotlb) {
					this._iotlb = _iotlb;
				}

				public String get_iotlb() {
					return this._iotlb;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_intremap(String _intremap) {
					this._intremap = _intremap;
				}

				public String get_intremap() {
					return this._intremap;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Parallel {

			protected Protocol protocol;

			protected Address address;

			protected Log log;

			protected Alias alias;

			protected Source source;

			protected Target target;

			public Parallel() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLog(Log log) {
				this.log = log;
			}

			public Log getLog() {
				return this.log;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Log {

				protected String _file;

				protected String _append;

				public Log() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_append(String _append) {
					this._append = _append;
				}

				public String get_append() {
					return this._append;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				public Source() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _type;

				protected String _port;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_port(String _port) {
					this._port = _port;
				}

				public String get_port() {
					return this._port;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Console {

			protected Protocol protocol;

			protected Address address;

			protected Log log;

			protected String _tty;
			
			protected String _type;

			protected Alias alias;

			protected Source source;

			protected Target target;

			public Console() {

			}

			public String get_type() {
				return _type;
			}



			public void set_type(String _type) {
				this._type = _type;
			}



			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLog(Log log) {
				this.log = log;
			}

			public Log getLog() {
				return this.log;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_tty(String _tty) {
				this._tty = _tty;
			}

			public String get_tty() {
				return this._tty;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Log {

				protected String _file;

				protected String _append;

				public Log() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_append(String _append) {
					this._append = _append;
				}

				public String get_append() {
					return this._append;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected String _path;
				
				public Source() {

				}

				public String get_path() {
					return _path;
				}

				public void set_path(String _path) {
					this._path = _path;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _type;

				protected String _port;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_port(String _port) {
					this._port = _port;
				}

				public String get_port() {
					return this._port;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Controller {

			protected Master master;
			
			protected Address address;

			protected String _index;

			protected Driver driver;

			protected String _type;

			protected Alias alias;

			protected String _model;

			protected Target target;
			
			protected Model model;
			
			public Target getTarget() {
				return target;
			}

			public void setTarget(Target target) {
				this.target = target;
			}

			public Model getModel() {
				return model;
			}

			public void setModel(Model model) {
				this.model = model;
			}

			public Master getMaster() {
				return master;
			}

			public void setMaster(Master master) {
				this.master = master;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_index(String _index) {
				this._index = _index;
			}

			public String get_index() {
				return this._index;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_type() {
				return this._type;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Model {

				protected String model;
				
				protected String _name;

				public String getModel() {
					return model;
				}

				public void setModel(String model) {
					this.model = model;
				}

				public String get_name() {
					return _name;
				}

				public void set_name(String _name) {
					this._name = _name;
				}
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String  _chassis;

				protected String _chassisNr;

				protected String _port;

				public String get_chassisNr() {
					return _chassisNr;
				}

				public void set_chassisNr(String _chassisNr) {
					this._chassisNr = _chassisNr;
				}

				public String get_chassis() {
					return _chassis;
				}

				public String get_port() {
					return _port;
				}

				public void set_port(String _port) {
					this._port = _port;
				}

				public void set_chassis(String _chassis) {
					this._chassis = _chassis;
				}


			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Master {
				
				protected String _startport;

				public Master() {
					super();
					// TODO Auto-generated constructor stub
				}

				public String get_startport() {
					return _startport;
				}

				public void set_startport(String _startport) {
					this._startport = _startport;
				}
				
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
		        
				protected String _domain;
		            
				protected String _function;
		            
				protected String _slot;
		            
				protected String _type;
				
				protected String _multifunction;
				
				public Address() {

				}

				
				public String get_multifunction() {
					return _multifunction;
				}



				public void set_multifunction(String _multifunction) {
					this._multifunction = _multifunction;
				}



				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _max_sectors;

				protected String _queues;

				protected String _iommu;

				protected String _ioeventfd;

				protected String _iothread;

				protected String _cmd_per_lun;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_max_sectors(String _max_sectors) {
					this._max_sectors = _max_sectors;
				}

				public String get_max_sectors() {
					return this._max_sectors;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_queues(String _queues) {
					this._queues = _queues;
				}

				public String get_queues() {
					return this._queues;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ioeventfd(String _ioeventfd) {
					this._ioeventfd = _ioeventfd;
				}

				public String get_ioeventfd() {
					return this._ioeventfd;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iothread(String _iothread) {
					this._iothread = _iothread;
				}

				public String get_iothread() {
					return this._iothread;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_cmd_per_lun(String _cmd_per_lun) {
					this._cmd_per_lun = _cmd_per_lun;
				}

				public String get_cmd_per_lun() {
					return this._cmd_per_lun;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Shmem {

			protected Server server;

			protected Msi msi;

			protected Address address;

			protected String _name;

			protected Size size;

			protected Alias alias;

			protected Model model;

			public Shmem() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setServer(Server server) {
				this.server = server;
			}

			public Server getServer() {
				return this.server;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMsi(Msi msi) {
				this.msi = msi;
			}

			public Msi getMsi() {
				return this.msi;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSize(Size size) {
				this.size = size;
			}

			public Size getSize() {
				return this.size;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setModel(Model model) {
				this.model = model;
			}

			public Model getModel() {
				return this.model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Server {

				protected String _path;

				public Server() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_path(String _path) {
					this._path = _path;
				}

				public String get_path() {
					return this._path;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Msi {

				protected String _vectors;

				protected String _ioeventfd;

				protected String _enabled;

				public Msi() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vectors(String _vectors) {
					this._vectors = _vectors;
				}

				public String get_vectors() {
					return this._vectors;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ioeventfd(String _ioeventfd) {
					this._ioeventfd = _ioeventfd;
				}

				public String get_ioeventfd() {
					return this._ioeventfd;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_enabled(String _enabled) {
					this._enabled = _enabled;
				}

				public String get_enabled() {
					return this._enabled;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Size {

				protected String _unit;

				protected String text;

				public Size() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Model {

				protected String _type;

				public Model() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Redirdev {

			protected Protocol protocol;

			protected Address address;

			protected Alias alias;

			protected Source source;

			protected Boot boot;

			protected String _bus;
			
			protected String _type;

			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			public Redirdev() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBoot(Boot boot) {
				this.boot = boot;
			}

			public Boot getBoot() {
				return this.boot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_bus(String _bus) {
				this._bus = _bus;
			}

			public String get_bus() {
				return this._bus;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {
				
				protected String _bus;
				
				protected String _type;
				
				protected String _port;

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_port() {
					return _port;
				}

				public void set_port(String _port) {
					this._port = _port;
				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				public Source() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Boot {

				protected String _loadparm;

				protected String _order;

				public Boot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_loadparm(String _loadparm) {
					this._loadparm = _loadparm;
				}

				public String get_loadparm() {
					return this._loadparm;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_order(String _order) {
					this._order = _order;
				}

				public String get_order() {
					return this._order;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Rng {

			protected Address address;

			protected Driver driver;

			protected Rate rate;

			protected Alias alias;

			protected String _model;

			protected Backend backend;

			public Rng() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setRate(Rate rate) {
				this.rate = rate;
			}

			public Rate getRate() {
				return this.rate;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBackend(Backend backend) {
				this.backend = backend;
			}

			public Backend getBackend() {
				return this.backend;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
				
		        protected String _domain;
		        
		        protected String _function;
		        
		        protected String _slot;
		        
		        protected String _type;
				
				public Address() {

				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
				
			}
			
			

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _iommu;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Rate {

				protected String _period;

				protected String _bytes;

				public Rate() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_period(String _period) {
					this._period = _period;
				}

				public String get_period() {
					return this._period;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_bytes(String _bytes) {
					this._bytes = _bytes;
				}

				public String get_bytes() {
					return this._bytes;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Backend {

				protected String _model;
				
				protected String text;
				
				public Backend() {

				}

				public String get_model() {
					return _model;
				}

				public void set_model(String _model) {
					this._model = _model;
				}

				public String getText() {
					return text;
				}

				public void setText(String text) {
					this.text = text;
				}
				
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Smartcard {

			protected Database database;

			protected Protocol protocol;

			protected Address address;

			protected ArrayList<Certificate> certificate;

			protected Alias alias;

			protected Source source;

			public Smartcard() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDatabase(Database database) {
				this.database = database;
			}

			public Database getDatabase() {
				return this.database;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCertificate(ArrayList<Certificate> certificate) {
				this.certificate = certificate;
			}

			public ArrayList<Certificate> getCertificate() {
				return this.certificate;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Database {

				protected String text;

				public Database() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Certificate {

				protected String text;

				public Certificate() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				public Source() {

				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Filesystem {

			protected String _accessmode;

			protected Address address;

			protected Driver driver;

			protected Readonly readonly;

			protected Space_hard_limit space_hard_limit;

			protected Alias alias;

			protected String _model;

			protected Source source;

			protected Space_soft_limit space_soft_limit;

			protected Target target;

			public Filesystem() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_accessmode(String _accessmode) {
				this._accessmode = _accessmode;
			}

			public String get_accessmode() {
				return this._accessmode;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setReadonly(Readonly readonly) {
				this.readonly = readonly;
			}

			public Readonly getReadonly() {
				return this.readonly;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSpace_hard_limit(Space_hard_limit space_hard_limit) {
				this.space_hard_limit = space_hard_limit;
			}

			public Space_hard_limit getSpace_hard_limit() {
				return this.space_hard_limit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSpace_soft_limit(Space_soft_limit space_soft_limit) {
				this.space_soft_limit = space_soft_limit;
			}

			public Space_soft_limit getSpace_soft_limit() {
				return this.space_soft_limit;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _name;

				protected String _iommu;

				protected String _type;

				protected String _format;

				protected String _wrpolicy;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_format(String _format) {
					this._format = _format;
				}

				public String get_format() {
					return this._format;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_wrpolicy(String _wrpolicy) {
					this._wrpolicy = _wrpolicy;
				}

				public String get_wrpolicy() {
					return this._wrpolicy;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Readonly {

				public Readonly() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Space_hard_limit {

				protected String _unit;

				protected String text;

				public Space_hard_limit() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				public Source() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Space_soft_limit {

				protected String _unit;

				protected String text;

				public Space_soft_limit() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _dir;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_dir(String _dir) {
					this._dir = _dir;
				}

				public String get_dir() {
					return this._dir;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Panic {

			protected Address address;

			protected Alias alias;

			protected String _model;

			public Panic() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Tpm {

			protected Address address;

			protected Alias alias;

			protected String _model;

			protected Backend backend;

			public Tpm() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBackend(Backend backend) {
				this.backend = backend;
			}

			public Backend getBackend() {
				return this.backend;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Backend {

				public Backend() {

				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Emulator {

			protected String text;

			public Emulator() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Input {

			protected Address address;

			protected Driver driver;

			protected String _type;

			protected Alias alias;

			protected String _model;

			protected Source source;

			protected String _bus;

			public Input() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_type() {
				return this._type;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_bus(String _bus) {
				this._bus = _bus;
			}

			public String get_bus() {
				return this._bus;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
				
				protected String _port;
				
				protected String _type;
				
				public Address() {

				}

				public String get_port() {
					return _port;
				}

				public void set_port(String _port) {
					this._port = _port;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}



				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _iommu;

				protected String _ats;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected String _evdev;

				public Source() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_evdev(String _evdev) {
					this._evdev = _evdev;
				}

				public String get_evdev() {
					return this._evdev;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Disk {

			protected String _type;
			
			protected Shareable shareable;

			protected Mirror mirror;

			protected String _snapshot;

			protected Auth auth;

			protected Blockio blockio;

			protected Source source;

			protected _transient _transient;

			protected Wwn wwn;

			protected Encryption encryption;

			protected Readonly readonly;

			protected Vendor vendor;

			protected Alias alias;

			protected Boot boot;

			protected String _rawio;

			protected Iotune iotune;

			protected Product product;

			protected Address address;

			protected String _sgio;

			protected String _device;

			protected Target target;

			protected Driver driver;

			protected Serial serial;

			protected BackingStore backingStore;

			protected String _model;

			protected Geometry geometry;

			public Disk() {

			}

			
			public String get_type() {
				return _type;
			}

			public void set_type(String _type) {
				this._type = _type;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setShareable(Shareable shareable) {
				this.shareable = shareable;
			}

			public Shareable getShareable() {
				return this.shareable;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMirror(Mirror mirror) {
				this.mirror = mirror;
			}

			public Mirror getMirror() {
				return this.mirror;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_snapshot(String _snapshot) {
				this._snapshot = _snapshot;
			}

			public String get_snapshot() {
				return this._snapshot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAuth(Auth auth) {
				this.auth = auth;
			}

			public Auth getAuth() {
				return this.auth;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBlockio(Blockio blockio) {
				this.blockio = blockio;
			}

			public Blockio getBlockio() {
				return this.blockio;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_transient(_transient _transient) {
				this._transient = _transient;
			}

			public _transient get_transient() {
				return this._transient;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setWwn(Wwn wwn) {
				this.wwn = wwn;
			}

			public Wwn getWwn() {
				return this.wwn;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setEncryption(Encryption encryption) {
				this.encryption = encryption;
			}

			public Encryption getEncryption() {
				return this.encryption;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setReadonly(Readonly readonly) {
				this.readonly = readonly;
			}

			public Readonly getReadonly() {
				return this.readonly;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setVendor(Vendor vendor) {
				this.vendor = vendor;
			}

			public Vendor getVendor() {
				return this.vendor;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBoot(Boot boot) {
				this.boot = boot;
			}

			public Boot getBoot() {
				return this.boot;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_rawio(String _rawio) {
				this._rawio = _rawio;
			}

			public String get_rawio() {
				return this._rawio;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setIotune(Iotune iotune) {
				this.iotune = iotune;
			}

			public Iotune getIotune() {
				return this.iotune;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProduct(Product product) {
				this.product = product;
			}

			public Product getProduct() {
				return this.product;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_sgio(String _sgio) {
				this._sgio = _sgio;
			}

			public String get_sgio() {
				return this._sgio;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_device(String _device) {
				this._device = _device;
			}

			public String get_device() {
				return this._device;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setDriver(Driver driver) {
				this.driver = driver;
			}

			public Driver getDriver() {
				return this.driver;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSerial(Serial serial) {
				this.serial = serial;
			}

			public Serial getSerial() {
				return this.serial;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setBackingStore(BackingStore backingStore) {
				this.backingStore = backingStore;
			}

			public BackingStore getBackingStore() {
				return this.backingStore;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setGeometry(Geometry geometry) {
				this.geometry = geometry;
			}

			public Geometry getGeometry() {
				return this.geometry;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Shareable {

				public Shareable() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Mirror {

				protected String _job;

				protected String _ready;

				protected Format format;

				protected Source source;

				public Mirror() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_job(String _job) {
					this._job = _job;
				}

				public String get_job() {
					return this._job;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ready(String _ready) {
					this._ready = _ready;
				}

				public String get_ready() {
					return this._ready;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setFormat(Format format) {
					this.format = format;
				}

				public Format getFormat() {
					return this.format;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSource(Source source) {
					this.source = source;
				}

				public Source getSource() {
					return this.source;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Format {

					protected String _type;

					public Format() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_type(String _type) {
						this._type = _type;
					}

					public String get_type() {
						return this._type;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Source {

					protected String _index;

					protected Encryption encryption;

					protected Reservations reservations;

					protected String _startupPolicy;

					public Source() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_index(String _index) {
						this._index = _index;
					}

					public String get_index() {
						return this._index;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setEncryption(Encryption encryption) {
						this.encryption = encryption;
					}

					public Encryption getEncryption() {
						return this.encryption;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setReservations(Reservations reservations) {
						this.reservations = reservations;
					}

					public Reservations getReservations() {
						return this.reservations;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_startupPolicy(String _startupPolicy) {
						this._startupPolicy = _startupPolicy;
					}

					public String get_startupPolicy() {
						return this._startupPolicy;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Encryption {

						protected String _format;

						protected Secret secret;

						public Encryption() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_format(String _format) {
							this._format = _format;
						}

						public String get_format() {
							return this._format;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void setSecret(Secret secret) {
							this.secret = secret;
						}

						public Secret getSecret() {
							return this.secret;
						}

						@JsonInclude(JsonInclude.Include.NON_NULL)
						@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
						public static class Secret {

							protected String _usage;

							protected String _type;

							protected String _uuid;

							public Secret() {

							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_usage(String _usage) {
								this._usage = _usage;
							}

							public String get_usage() {
								return this._usage;
							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_type(String _type) {
								this._type = _type;
							}

							public String get_type() {
								return this._type;
							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_uuid(String _uuid) {
								this._uuid = _uuid;
							}

							public String get_uuid() {
								return this._uuid;
							}
						}
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Reservations {

						protected String _managed;

						protected Domain.Source source;

						protected String _enabled;

						public Reservations() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_managed(String _managed) {
							this._managed = _managed;
						}

						public String get_managed() {
							return this._managed;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void setSource(Domain.Source source) {
							this.source = source;
						}

						public Domain.Source getSource() {
							return this.source;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_enabled(String _enabled) {
							this._enabled = _enabled;
						}

						public String get_enabled() {
							return this._enabled;
						}
						
					}
					
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Auth {

				protected String _username;

				protected Secret secret;

				public Auth() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_username(String _username) {
					this._username = _username;
				}

				public String get_username() {
					return this._username;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSecret(Secret secret) {
					this.secret = secret;
				}

				public Secret getSecret() {
					return this.secret;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Secret {

					protected String _usage;

					protected String _type;

					protected String _uuid;

					public Secret() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_usage(String _usage) {
						this._usage = _usage;
					}

					public String get_usage() {
						return this._usage;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_type(String _type) {
						this._type = _type;
					}

					public String get_type() {
						return this._type;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_uuid(String _uuid) {
						this._uuid = _uuid;
					}

					public String get_uuid() {
						return this._uuid;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Blockio {

				protected String _physical_block_size;

				protected String _logical_block_size;

				public Blockio() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_physical_block_size(String _physical_block_size) {
					this._physical_block_size = _physical_block_size;
				}

				public String get_physical_block_size() {
					return this._physical_block_size;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_logical_block_size(String _logical_block_size) {
					this._logical_block_size = _logical_block_size;
				}

				public String get_logical_block_size() {
					return this._logical_block_size;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected String _index;

				protected Encryption encryption;

				protected Reservations reservations;

				protected String _startupPolicy;
				
				protected String _file;
				
				protected String _controller;

				protected String _dev;

				public Source() {

				}

				public String get_dev() {
					return _dev;
				}

				public void set_dev(String _dev) {
					this._dev = _dev;
				}

				public String get_controller() {
					return _controller;
				}

				public void set_controller(String _controller) {
					this._controller = _controller;
				}



				public String get_file() {
					return _file;
				}



				public void set_file(String _file) {
					this._file = _file;
				}



				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_index(String _index) {
					this._index = _index;
				}

				public String get_index() {
					return this._index;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setEncryption(Encryption encryption) {
					this.encryption = encryption;
				}

				public Encryption getEncryption() {
					return this.encryption;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setReservations(Reservations reservations) {
					this.reservations = reservations;
				}

				public Reservations getReservations() {
					return this.reservations;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_startupPolicy(String _startupPolicy) {
					this._startupPolicy = _startupPolicy;
				}

				public String get_startupPolicy() {
					return this._startupPolicy;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Encryption {

					protected String _format;

					protected Secret secret;

					public Encryption() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_format(String _format) {
						this._format = _format;
					}

					public String get_format() {
						return this._format;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setSecret(Secret secret) {
						this.secret = secret;
					}

					public Secret getSecret() {
						return this.secret;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Secret {

						protected String _usage;

						protected String _type;

						protected String _uuid;

						public Secret() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_usage(String _usage) {
							this._usage = _usage;
						}

						public String get_usage() {
							return this._usage;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_type(String _type) {
							this._type = _type;
						}

						public String get_type() {
							return this._type;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_uuid(String _uuid) {
							this._uuid = _uuid;
						}

						public String get_uuid() {
							return this._uuid;
						}
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Reservations {

					protected String _managed;

					protected Domain.Source source;

					protected String _enabled;

					public Reservations() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_managed(String _managed) {
						this._managed = _managed;
					}

					public String get_managed() {
						return this._managed;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setSource(Domain.Source source) {
						this.source = source;
					}

					public Domain.Source getSource() {
						return this.source;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_enabled(String _enabled) {
						this._enabled = _enabled;
					}

					public String get_enabled() {
						return this._enabled;
					}

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class _transient {

				public _transient() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Wwn {

				protected String text;

				public Wwn() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Encryption {

				protected String _format;

				protected Secret secret;

				public Encryption() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_format(String _format) {
					this._format = _format;
				}

				public String get_format() {
					return this._format;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSecret(Secret secret) {
					this.secret = secret;
				}

				public Secret getSecret() {
					return this.secret;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Secret {

					protected String _usage;

					protected String _type;

					protected String _uuid;

					public Secret() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_usage(String _usage) {
						this._usage = _usage;
					}

					public String get_usage() {
						return this._usage;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_type(String _type) {
						this._type = _type;
					}

					public String get_type() {
						return this._type;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_uuid(String _uuid) {
						this._uuid = _uuid;
					}

					public String get_uuid() {
						return this._uuid;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Readonly {

				public Readonly() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Vendor {

				protected String text;

				public Vendor() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Boot {

				protected String _loadparm;

				protected String _order;

				public Boot() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_loadparm(String _loadparm) {
					this._loadparm = _loadparm;
				}

				public String get_loadparm() {
					return this._loadparm;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_order(String _order) {
					this._order = _order;
				}

				public String get_order() {
					return this._order;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Iotune {

				protected Write_iops_sec_max_length write_iops_sec_max_length;

				protected Group_name group_name;

				protected Write_iops_sec write_iops_sec;

				protected Read_bytes_sec_max read_bytes_sec_max;

				protected Read_bytes_sec_max_length read_bytes_sec_max_length;

				protected Total_iops_sec total_iops_sec;

				protected Write_iops_sec_max write_iops_sec_max;

				protected Total_bytes_sec total_bytes_sec;

				protected Total_iops_sec_max total_iops_sec_max;

				protected Total_bytes_sec_max_length total_bytes_sec_max_length;

				protected Write_bytes_sec write_bytes_sec;

				protected Total_bytes_sec_max total_bytes_sec_max;

				protected Write_bytes_sec_max write_bytes_sec_max;

				protected Read_iops_sec_max read_iops_sec_max;

				protected Read_iops_sec_max_length read_iops_sec_max_length;

				protected Size_iops_sec size_iops_sec;

				protected Read_bytes_sec read_bytes_sec;

				protected Read_iops_sec read_iops_sec;

				protected Total_iops_sec_max_length total_iops_sec_max_length;

				protected Write_bytes_sec_max_length write_bytes_sec_max_length;

				public Iotune() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_iops_sec_max_length(Write_iops_sec_max_length write_iops_sec_max_length) {
					this.write_iops_sec_max_length = write_iops_sec_max_length;
				}

				public Write_iops_sec_max_length getWrite_iops_sec_max_length() {
					return this.write_iops_sec_max_length;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setGroup_name(Group_name group_name) {
					this.group_name = group_name;
				}

				public Group_name getGroup_name() {
					return this.group_name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_iops_sec(Write_iops_sec write_iops_sec) {
					this.write_iops_sec = write_iops_sec;
				}

				public Write_iops_sec getWrite_iops_sec() {
					return this.write_iops_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_bytes_sec_max(Read_bytes_sec_max read_bytes_sec_max) {
					this.read_bytes_sec_max = read_bytes_sec_max;
				}

				public Read_bytes_sec_max getRead_bytes_sec_max() {
					return this.read_bytes_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_bytes_sec_max_length(Read_bytes_sec_max_length read_bytes_sec_max_length) {
					this.read_bytes_sec_max_length = read_bytes_sec_max_length;
				}

				public Read_bytes_sec_max_length getRead_bytes_sec_max_length() {
					return this.read_bytes_sec_max_length;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_iops_sec(Total_iops_sec total_iops_sec) {
					this.total_iops_sec = total_iops_sec;
				}

				public Total_iops_sec getTotal_iops_sec() {
					return this.total_iops_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_iops_sec_max(Write_iops_sec_max write_iops_sec_max) {
					this.write_iops_sec_max = write_iops_sec_max;
				}

				public Write_iops_sec_max getWrite_iops_sec_max() {
					return this.write_iops_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_bytes_sec(Total_bytes_sec total_bytes_sec) {
					this.total_bytes_sec = total_bytes_sec;
				}

				public Total_bytes_sec getTotal_bytes_sec() {
					return this.total_bytes_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_iops_sec_max(Total_iops_sec_max total_iops_sec_max) {
					this.total_iops_sec_max = total_iops_sec_max;
				}

				public Total_iops_sec_max getTotal_iops_sec_max() {
					return this.total_iops_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_bytes_sec_max_length(Total_bytes_sec_max_length total_bytes_sec_max_length) {
					this.total_bytes_sec_max_length = total_bytes_sec_max_length;
				}

				public Total_bytes_sec_max_length getTotal_bytes_sec_max_length() {
					return this.total_bytes_sec_max_length;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_bytes_sec(Write_bytes_sec write_bytes_sec) {
					this.write_bytes_sec = write_bytes_sec;
				}

				public Write_bytes_sec getWrite_bytes_sec() {
					return this.write_bytes_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_bytes_sec_max(Total_bytes_sec_max total_bytes_sec_max) {
					this.total_bytes_sec_max = total_bytes_sec_max;
				}

				public Total_bytes_sec_max getTotal_bytes_sec_max() {
					return this.total_bytes_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_bytes_sec_max(Write_bytes_sec_max write_bytes_sec_max) {
					this.write_bytes_sec_max = write_bytes_sec_max;
				}

				public Write_bytes_sec_max getWrite_bytes_sec_max() {
					return this.write_bytes_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_iops_sec_max(Read_iops_sec_max read_iops_sec_max) {
					this.read_iops_sec_max = read_iops_sec_max;
				}

				public Read_iops_sec_max getRead_iops_sec_max() {
					return this.read_iops_sec_max;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_iops_sec_max_length(Read_iops_sec_max_length read_iops_sec_max_length) {
					this.read_iops_sec_max_length = read_iops_sec_max_length;
				}

				public Read_iops_sec_max_length getRead_iops_sec_max_length() {
					return this.read_iops_sec_max_length;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSize_iops_sec(Size_iops_sec size_iops_sec) {
					this.size_iops_sec = size_iops_sec;
				}

				public Size_iops_sec getSize_iops_sec() {
					return this.size_iops_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_bytes_sec(Read_bytes_sec read_bytes_sec) {
					this.read_bytes_sec = read_bytes_sec;
				}

				public Read_bytes_sec getRead_bytes_sec() {
					return this.read_bytes_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setRead_iops_sec(Read_iops_sec read_iops_sec) {
					this.read_iops_sec = read_iops_sec;
				}

				public Read_iops_sec getRead_iops_sec() {
					return this.read_iops_sec;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setTotal_iops_sec_max_length(Total_iops_sec_max_length total_iops_sec_max_length) {
					this.total_iops_sec_max_length = total_iops_sec_max_length;
				}

				public Total_iops_sec_max_length getTotal_iops_sec_max_length() {
					return this.total_iops_sec_max_length;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setWrite_bytes_sec_max_length(Write_bytes_sec_max_length write_bytes_sec_max_length) {
					this.write_bytes_sec_max_length = write_bytes_sec_max_length;
				}

				public Write_bytes_sec_max_length getWrite_bytes_sec_max_length() {
					return this.write_bytes_sec_max_length;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_iops_sec_max_length {

					protected String text;

					public Write_iops_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Group_name {

					protected String text;

					public Group_name() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_iops_sec {

					protected String text;

					public Write_iops_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_bytes_sec_max {

					protected String text;

					public Read_bytes_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_bytes_sec_max_length {

					protected String text;

					public Read_bytes_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_iops_sec {

					protected String text;

					public Total_iops_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_iops_sec_max {

					protected String text;

					public Write_iops_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_bytes_sec {

					protected String text;

					public Total_bytes_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_iops_sec_max {

					protected String text;

					public Total_iops_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_bytes_sec_max_length {

					protected String text;

					public Total_bytes_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_bytes_sec {

					protected String text;

					public Write_bytes_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_bytes_sec_max {

					protected String text;

					public Total_bytes_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_bytes_sec_max {

					protected String text;

					public Write_bytes_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_iops_sec_max {

					protected String text;

					public Read_iops_sec_max() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_iops_sec_max_length {

					protected String text;

					public Read_iops_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Size_iops_sec {

					protected String text;

					public Size_iops_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_bytes_sec {

					protected String text;

					public Read_bytes_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Read_iops_sec {

					protected String text;

					public Read_iops_sec() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Total_iops_sec_max_length {

					protected String text;

					public Total_iops_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Write_bytes_sec_max_length {

					protected String text;

					public Write_bytes_sec_max_length() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setText(String text) {
						this.text = text;
					}

					public String getText() {
						return this.text;
					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Product {

				protected String text;

				public Product() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				protected String _bus;
				
				protected String _domain;
				
				protected String _function;
				
				protected String _slot;
				
				protected String _type;
				
				protected String _controller;
				
				protected String _target;
				
				protected String _unit;
				
				public Address() {

				}

				public String get_unit() {
					return _unit;
				}



				public void set_unit(String _unit) {
					this._unit = _unit;
				}



				public String get_target() {
					return _target;
				}


				public void set_target(String _target) {
					this._target = _target;
				}


				public String get_controller() {
					return _controller;
				}



				public void set_controller(String _controller) {
					this._controller = _controller;
				}



				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_domain() {
					return _domain;
				}

				public void set_domain(String _domain) {
					this._domain = _domain;
				}

				public String get_function() {
					return _function;
				}

				public void set_function(String _function) {
					this._function = _function;
				}

				public String get_slot() {
					return _slot;
				}

				public void set_slot(String _slot) {
					this._slot = _slot;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _removable;

				protected String _tray;

				protected String _dev;

				protected String _bus;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_removable(String _removable) {
					this._removable = _removable;
				}

				public String get_removable() {
					return this._removable;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_tray(String _tray) {
					this._tray = _tray;
				}

				public String get_tray() {
					return this._tray;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_dev(String _dev) {
					this._dev = _dev;
				}

				public String get_dev() {
					return this._dev;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_bus() {
					return this._bus;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _detect_zeroes;

				protected String _io;

				protected String _name;

				protected String _rerror_policy;

				protected String _queues;

				protected String _iommu;

				protected String _type;

				protected String _ats;

				protected String _discard;

				protected String _copy_on_read;

				protected String _error_policy;

				protected String _ioeventfd;

				protected String _iothread;

				protected String _event_idx;

				protected String _cache;

				public Driver() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_detect_zeroes(String _detect_zeroes) {
					this._detect_zeroes = _detect_zeroes;
				}

				public String get_detect_zeroes() {
					return this._detect_zeroes;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_io(String _io) {
					this._io = _io;
				}

				public String get_io() {
					return this._io;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_rerror_policy(String _rerror_policy) {
					this._rerror_policy = _rerror_policy;
				}

				public String get_rerror_policy() {
					return this._rerror_policy;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_queues(String _queues) {
					this._queues = _queues;
				}

				public String get_queues() {
					return this._queues;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iommu(String _iommu) {
					this._iommu = _iommu;
				}

				public String get_iommu() {
					return this._iommu;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ats(String _ats) {
					this._ats = _ats;
				}

				public String get_ats() {
					return this._ats;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_discard(String _discard) {
					this._discard = _discard;
				}

				public String get_discard() {
					return this._discard;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_copy_on_read(String _copy_on_read) {
					this._copy_on_read = _copy_on_read;
				}

				public String get_copy_on_read() {
					return this._copy_on_read;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_error_policy(String _error_policy) {
					this._error_policy = _error_policy;
				}

				public String get_error_policy() {
					return this._error_policy;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_ioeventfd(String _ioeventfd) {
					this._ioeventfd = _ioeventfd;
				}

				public String get_ioeventfd() {
					return this._ioeventfd;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_iothread(String _iothread) {
					this._iothread = _iothread;
				}

				public String get_iothread() {
					return this._iothread;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_event_idx(String _event_idx) {
					this._event_idx = _event_idx;
				}

				public String get_event_idx() {
					return this._event_idx;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_cache(String _cache) {
					this._cache = _cache;
				}

				public String get_cache() {
					return this._cache;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Serial {

				protected String _type;
				
				protected String text;

				public Serial() {

				}

				public String get_type() {
					return _type;
				}



				public void set_type(String _type) {
					this._type = _type;
				}



				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class BackingStore {

				protected String _index;

				protected Format format;

				protected Source source;

				protected String _type;
				
				protected String _file;
				
				protected BackingStore backingStore;
				
				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_index(String _index) {
					this._index = _index;
				}

				public String get_index() {
					return this._index;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setFormat(Format format) {
					this.format = format;
				}

				public Format getFormat() {
					return this.format;
				}

				
				public String get_file() {
					return _file;
				}

				public void set_file(String _file) {
					this._file = _file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setSource(Source source) {
					this.source = source;
				}

				public Source getSource() {
					return this.source;
				}

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}
				
				public BackingStore getBackingStore() {
					return backingStore;
				}

				public void setBackingStore(BackingStore backingStore) {
					this.backingStore = backingStore;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Format {

					protected String _type;

					public Format() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_type(String _type) {
						this._type = _type;
					}

					public String get_type() {
						return this._type;
					}
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Source {

					protected String _index;

					protected Encryption encryption;

					protected Reservations reservations;

					protected String _startupPolicy;
					
					protected String _file;
					
					protected String _dev;
					
					public String get_dev() {
						return _dev;
					}

					public void set_dev(String _dev) {
						this._dev = _dev;
					}

					public String get_file() {
						return _file;
					}

					public void set_file(String _file) {
						this._file = _file;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_index(String _index) {
						this._index = _index;
					}

					public String get_index() {
						return this._index;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setEncryption(Encryption encryption) {
						this.encryption = encryption;
					}

					public Encryption getEncryption() {
						return this.encryption;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setReservations(Reservations reservations) {
						this.reservations = reservations;
					}

					public Reservations getReservations() {
						return this.reservations;
					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_startupPolicy(String _startupPolicy) {
						this._startupPolicy = _startupPolicy;
					}

					public String get_startupPolicy() {
						return this._startupPolicy;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Encryption {

						protected String _format;

						protected Secret secret;

						public Encryption() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_format(String _format) {
							this._format = _format;
						}

						public String get_format() {
							return this._format;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void setSecret(Secret secret) {
							this.secret = secret;
						}

						public Secret getSecret() {
							return this.secret;
						}

						@JsonInclude(JsonInclude.Include.NON_NULL)
						@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
						public static class Secret {

							protected String _usage;

							protected String _type;

							protected String _uuid;

							public Secret() {

							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_usage(String _usage) {
								this._usage = _usage;
							}

							public String get_usage() {
								return this._usage;
							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_type(String _type) {
								this._type = _type;
							}

							public String get_type() {
								return this._type;
							}

							/**
							 * Ignore the user setting, use 'lifecycle' to update VM's info
							 *
							 */
							public void set_uuid(String _uuid) {
								this._uuid = _uuid;
							}

							public String get_uuid() {
								return this._uuid;
							}
						}
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Reservations {

						protected String _managed;

						protected Domain.Source source;

						protected String _enabled;

						public Reservations() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_managed(String _managed) {
							this._managed = _managed;
						}

						public String get_managed() {
							return this._managed;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void setSource(Domain.Source source) {
							this.source = source;
						}

						public Domain.Source getSource() {
							return this.source;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_enabled(String _enabled) {
							this._enabled = _enabled;
						}

						public String get_enabled() {
							return this._enabled;
						}

					}
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Geometry {

				protected String _heads;

				protected String _secs;

				protected String _cyls;

				protected String _trans;

				public Geometry() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_heads(String _heads) {
					this._heads = _heads;
				}

				public String get_heads() {
					return this._heads;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_secs(String _secs) {
					this._secs = _secs;
				}

				public String get_secs() {
					return this._secs;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_cyls(String _cyls) {
					this._cyls = _cyls;
				}

				public String get_cyls() {
					return this._cyls;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_trans(String _trans) {
					this._trans = _trans;
				}

				public String get_trans() {
					return this._trans;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Watchdog {

			protected Address address;

			protected Alias alias;

			protected String _action;

			protected String _model;

			public Watchdog() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_action(String _action) {
				this._action = _action;
			}

			public String get_action() {
				return this._action;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_model(String _model) {
				this._model = _model;
			}

			public String get_model() {
				return this._model;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Hub {

			protected Address address;

			protected String _type;

			protected Alias alias;

			public Hub() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_type(String _type) {
				this._type = _type;
			}

			public String get_type() {
				return this._type;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {
				
				protected String _type;
				
				protected String _bus;
				
				protected String _port;

				public String get_type() {
					return _type;
				}

				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_bus() {
					return _bus;
				}

				public void set_bus(String _bus) {
					this._bus = _bus;
				}

				public String get_port() {
					return _port;
				}

				public void set_port(String _port) {
					this._port = _port;
				}

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Serial {

			protected String _type;
			
			protected Protocol protocol;

			protected Address address;

			protected Log log;

			protected Alias alias;

			protected Source source;

			protected Target target;

			public Serial() {

			}

			public String get_type() {
				return _type;
			}



			public void set_type(String _type) {
				this._type = _type;
			}



			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setProtocol(Protocol protocol) {
				this.protocol = protocol;
			}

			public Protocol getProtocol() {
				return this.protocol;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAddress(Address address) {
				this.address = address;
			}

			public Address getAddress() {
				return this.address;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLog(Log log) {
				this.log = log;
			}

			public Log getLog() {
				return this.log;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setAlias(Alias alias) {
				this.alias = alias;
			}

			public Alias getAlias() {
				return this.alias;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Protocol {

				protected String _type;

				public Protocol() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Address {

				public Address() {

				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Log {

				protected String _file;

				protected String _append;

				public Log() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_file(String _file) {
					this._file = _file;
				}

				public String get_file() {
					return this._file;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_append(String _append) {
					this._append = _append;
				}

				public String get_append() {
					return this._append;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Alias {

				protected String _name;

				public Alias() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_name() {
					return this._name;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Source {

				protected String _path;
				
				public Source() {

				}

				public String get_path() {
					return _path;
				}

				public void set_path(String _path) {
					this._path = _path;
				}
				
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _type;

				protected Model model;

				protected String _port;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setModel(Model model) {
					this.model = model;
				}

				public Model getModel() {
					return this.model;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_port(String _port) {
					this._port = _port;
				}

				public String get_port() {
					return this._port;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Model {

					protected String _name;

					public Model() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void set_name(String _name) {
						this._name = _name;
					}

					public String get_name() {
						return this._name;
					}
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Lease {

			protected Lockspace lockspace;

			protected Key key;

			protected Target target;

			public Lease() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setLockspace(Lockspace lockspace) {
				this.lockspace = lockspace;
			}

			public Lockspace getLockspace() {
				return this.lockspace;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setKey(Key key) {
				this.key = key;
			}

			public Key getKey() {
				return this.key;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setTarget(Target target) {
				this.target = target;
			}

			public Target getTarget() {
				return this.target;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Lockspace {

				protected String text;

				public Lockspace() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Key {

				protected String text;

				public Key() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setText(String text) {
					this.text = text;
				}

				public String getText() {
					return this.text;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Target {

				protected String _offset;

				protected String _path;

				public Target() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_offset(String _offset) {
					this._offset = _offset;
				}

				public String get_offset() {
					return this._offset;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_path(String _path) {
					this._path = _path;
				}

				public String get_path() {
					return this._path;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Resource {

		protected Partition partition;

		public Resource() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPartition(Partition partition) {
			this.partition = partition;
		}

		public Partition getPartition() {
			return this.partition;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Partition {

			protected String text;

			public Partition() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class On_reboot {

		protected String text;

		public On_reboot() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Cpu {

		protected Cache cache;

		protected ArrayList<Feature> feature;

		protected Topology topology;

		protected Vendor vendor;

		protected Numa numa;

		protected String _check;

		protected Model model;

		protected String _match;

		protected String _mode;

		public Cpu() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setCache(Cache cache) {
			this.cache = cache;
		}

		public Cache getCache() {
			return this.cache;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setFeature(ArrayList<Feature> feature) {
			this.feature = feature;
		}

		public ArrayList<Feature> getFeature() {
			return this.feature;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setTopology(Topology topology) {
			this.topology = topology;
		}

		public Topology getTopology() {
			return this.topology;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVendor(Vendor vendor) {
			this.vendor = vendor;
		}

		public Vendor getVendor() {
			return this.vendor;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setNuma(Numa numa) {
			this.numa = numa;
		}

		public Numa getNuma() {
			return this.numa;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_check(String _check) {
			this._check = _check;
		}

		public String get_check() {
			return this._check;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setModel(Model model) {
			this.model = model;
		}

		public Model getModel() {
			return this.model;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_match(String _match) {
			this._match = _match;
		}

		public String get_match() {
			return this._match;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_mode(String _mode) {
			this._mode = _mode;
		}

		public String get_mode() {
			return this._mode;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Cache {

			protected String _level;

			protected String _mode;

			public Cache() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_level(String _level) {
				this._level = _level;
			}

			public String get_level() {
				return this._level;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Feature {

			protected String _name;

			protected String _policy;

			public Feature() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_policy(String _policy) {
				this._policy = _policy;
			}

			public String get_policy() {
				return this._policy;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Topology {

			protected String _cores;

			protected String _sockets;

			protected String _threads;

			public Topology() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_cores(String _cores) {
				this._cores = _cores;
			}

			public String get_cores() {
				return this._cores;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_sockets(String _sockets) {
				this._sockets = _sockets;
			}

			public String get_sockets() {
				return this._sockets;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_threads(String _threads) {
				this._threads = _threads;
			}

			public String get_threads() {
				return this._threads;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vendor {

			protected String text;

			public Vendor() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Numa {

			protected ArrayList<Cell> cell;

			public Numa() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCell(ArrayList<Cell> cell) {
				this.cell = cell;
			}

			public ArrayList<Cell> getCell() {
				return this.cell;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Cell {

				protected String _discard;

				protected Distances distances;

				protected String _memory;

				protected String _unit;

				protected String _cpus;

				protected String _memAccess;

				protected String _id;

				public Cell() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_discard(String _discard) {
					this._discard = _discard;
				}

				public String get_discard() {
					return this._discard;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void setDistances(Distances distances) {
					this.distances = distances;
				}

				public Distances getDistances() {
					return this.distances;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_memory(String _memory) {
					this._memory = _memory;
				}

				public String get_memory() {
					return this._memory;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_cpus(String _cpus) {
					this._cpus = _cpus;
				}

				public String get_cpus() {
					return this._cpus;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_memAccess(String _memAccess) {
					this._memAccess = _memAccess;
				}

				public String get_memAccess() {
					return this._memAccess;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_id(String _id) {
					this._id = _id;
				}

				public String get_id() {
					return this._id;
				}

				@JsonInclude(JsonInclude.Include.NON_NULL)
				@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
				public static class Distances {

					protected ArrayList<Sibling> sibling;

					public Distances() {

					}

					/**
					 * Ignore the user setting, use 'lifecycle' to update VM's info
					 *
					 */
					public void setSibling(ArrayList<Sibling> sibling) {
						this.sibling = sibling;
					}

					public ArrayList<Sibling> getSibling() {
						return this.sibling;
					}

					@JsonInclude(JsonInclude.Include.NON_NULL)
					@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
					public static class Sibling {

						protected String _value;

						protected String _id;

						public Sibling() {

						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_value(String _value) {
							this._value = _value;
						}

						public String get_value() {
							return this._value;
						}

						/**
						 * Ignore the user setting, use 'lifecycle' to update VM's info
						 *
						 */
						public void set_id(String _id) {
							this._id = _id;
						}

						public String get_id() {
							return this._id;
						}
					}
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Model {

			protected String _fallback;

			protected String _vendor_id;

			protected String text;

			public Model() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_fallback(String _fallback) {
				this._fallback = _fallback;
			}

			public String get_fallback() {
				return this._fallback;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_vendor_id(String _vendor_id) {
				this._vendor_id = _vendor_id;
			}

			public String get_vendor_id() {
				return this._vendor_id;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Clock {

		protected String _basis;

		protected ArrayList<Timer> timer;

		protected String _offset;

		protected String _adjustment;

		protected String _timezone;

		public Clock() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_basis(String _basis) {
			this._basis = _basis;
		}

		public String get_basis() {
			return this._basis;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setTimer(ArrayList<Timer> timer) {
			this.timer = timer;
		}

		public ArrayList<Timer> getTimer() {
			return this.timer;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_offset(String _offset) {
			this._offset = _offset;
		}

		public String get_offset() {
			return this._offset;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_adjustment(String _adjustment) {
			this._adjustment = _adjustment;
		}

		public String get_adjustment() {
			return this._adjustment;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_timezone(String _timezone) {
			this._timezone = _timezone;
		}

		public String get_timezone() {
			return this._timezone;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Timer {

			protected String _name;

			protected Catchup catchup;

			protected String _track;

			protected String _frequency;

			protected String _present;

			protected String _tickpolicy;

			protected String _mode;

			public Timer() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_name(String _name) {
				this._name = _name;
			}

			public String get_name() {
				return this._name;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCatchup(Catchup catchup) {
				this.catchup = catchup;
			}

			public Catchup getCatchup() {
				return this.catchup;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_track(String _track) {
				this._track = _track;
			}

			public String get_track() {
				return this._track;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_frequency(String _frequency) {
				this._frequency = _frequency;
			}

			public String get_frequency() {
				return this._frequency;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_present(String _present) {
				this._present = _present;
			}

			public String get_present() {
				return this._present;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_tickpolicy(String _tickpolicy) {
				this._tickpolicy = _tickpolicy;
			}

			public String get_tickpolicy() {
				return this._tickpolicy;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public String get_mode() {
				return this._mode;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Catchup {

				protected String _limit;

				protected String _slew;

				protected String _threshold;

				public Catchup() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_limit(String _limit) {
					this._limit = _limit;
				}

				public String get_limit() {
					return this._limit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_slew(String _slew) {
					this._slew = _slew;
				}

				public String get_slew() {
					return this._slew;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_threshold(String _threshold) {
					this._threshold = _threshold;
				}

				public String get_threshold() {
					return this._threshold;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Vcpus {

		protected ArrayList<Vcpu> vcpu;

		public Vcpus() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVcpu(ArrayList<Vcpu> vcpu) {
			this.vcpu = vcpu;
		}

		public ArrayList<Vcpu> getVcpu() {
			return this.vcpu;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vcpu {

			protected String _order;

			protected String _hotpluggable;

			protected String _id;

			protected String _enabled;

			public Vcpu() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_order(String _order) {
				this._order = _order;
			}

			public String get_order() {
				return this._order;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_hotpluggable(String _hotpluggable) {
				this._hotpluggable = _hotpluggable;
			}

			public String get_hotpluggable() {
				return this._hotpluggable;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_id(String _id) {
				this._id = _id;
			}

			public String get_id() {
				return this._id;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_enabled(String _enabled) {
				this._enabled = _enabled;
			}

			public String get_enabled() {
				return this._enabled;
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Cputune {

		protected Global_quota global_quota;

		protected ArrayList<Iothreadpin> iothreadpin;

		protected Period period;

		protected Emulator_period emulator_period;

		protected Emulatorpin emulatorpin;

		protected ArrayList<Vcpusched> vcpusched;

		protected ArrayList<Iothreadsched> iothreadsched;

		protected Iothread_period iothread_period;

		protected Global_period global_period;

		protected Emulator_quota emulator_quota;

		protected Shares shares;

		protected ArrayList<Vcpupin> vcpupin;

		protected ArrayList<Cachetune> cachetune;

		protected Quota quota;

		protected Iothread_quota iothread_quota;

		protected ArrayList<Memorytune> memorytune;

		public Cputune() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setGlobal_quota(Global_quota global_quota) {
			this.global_quota = global_quota;
		}

		public Global_quota getGlobal_quota() {
			return this.global_quota;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIothreadpin(ArrayList<Iothreadpin> iothreadpin) {
			this.iothreadpin = iothreadpin;
		}

		public ArrayList<Iothreadpin> getIothreadpin() {
			return this.iothreadpin;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setPeriod(Period period) {
			this.period = period;
		}

		public Period getPeriod() {
			return this.period;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setEmulator_period(Emulator_period emulator_period) {
			this.emulator_period = emulator_period;
		}

		public Emulator_period getEmulator_period() {
			return this.emulator_period;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setEmulatorpin(Emulatorpin emulatorpin) {
			this.emulatorpin = emulatorpin;
		}

		public Emulatorpin getEmulatorpin() {
			return this.emulatorpin;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVcpusched(ArrayList<Vcpusched> vcpusched) {
			this.vcpusched = vcpusched;
		}

		public ArrayList<Vcpusched> getVcpusched() {
			return this.vcpusched;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIothreadsched(ArrayList<Iothreadsched> iothreadsched) {
			this.iothreadsched = iothreadsched;
		}

		public ArrayList<Iothreadsched> getIothreadsched() {
			return this.iothreadsched;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIothread_period(Iothread_period iothread_period) {
			this.iothread_period = iothread_period;
		}

		public Iothread_period getIothread_period() {
			return this.iothread_period;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setGlobal_period(Global_period global_period) {
			this.global_period = global_period;
		}

		public Global_period getGlobal_period() {
			return this.global_period;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setEmulator_quota(Emulator_quota emulator_quota) {
			this.emulator_quota = emulator_quota;
		}

		public Emulator_quota getEmulator_quota() {
			return this.emulator_quota;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setShares(Shares shares) {
			this.shares = shares;
		}

		public Shares getShares() {
			return this.shares;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setVcpupin(ArrayList<Vcpupin> vcpupin) {
			this.vcpupin = vcpupin;
		}

		public ArrayList<Vcpupin> getVcpupin() {
			return this.vcpupin;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setCachetune(ArrayList<Cachetune> cachetune) {
			this.cachetune = cachetune;
		}

		public ArrayList<Cachetune> getCachetune() {
			return this.cachetune;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setQuota(Quota quota) {
			this.quota = quota;
		}

		public Quota getQuota() {
			return this.quota;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setIothread_quota(Iothread_quota iothread_quota) {
			this.iothread_quota = iothread_quota;
		}

		public Iothread_quota getIothread_quota() {
			return this.iothread_quota;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setMemorytune(ArrayList<Memorytune> memorytune) {
			this.memorytune = memorytune;
		}

		public ArrayList<Memorytune> getMemorytune() {
			return this.memorytune;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Global_quota {

			protected String text;

			public Global_quota() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iothreadpin {

			protected String _cpuset;

			protected String _iothread;

			public Iothreadpin() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_cpuset(String _cpuset) {
				this._cpuset = _cpuset;
			}

			public String get_cpuset() {
				return this._cpuset;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_iothread(String _iothread) {
				this._iothread = _iothread;
			}

			public String get_iothread() {
				return this._iothread;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Period {

			protected String text;

			public Period() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Emulator_period {

			protected String text;

			public Emulator_period() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Emulatorpin {

			protected String _cpuset;

			public Emulatorpin() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_cpuset(String _cpuset) {
				this._cpuset = _cpuset;
			}

			public String get_cpuset() {
				return this._cpuset;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vcpusched {

			protected String _scheduler;

			protected String _vcpus;

			protected String _priority;

			public Vcpusched() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_scheduler(String _scheduler) {
				this._scheduler = _scheduler;
			}

			public String get_scheduler() {
				return this._scheduler;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_vcpus(String _vcpus) {
				this._vcpus = _vcpus;
			}

			public String get_vcpus() {
				return this._vcpus;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_priority(String _priority) {
				this._priority = _priority;
			}

			public String get_priority() {
				return this._priority;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iothreadsched {

			protected String _scheduler;

			protected String _iothreads;

			protected String _priority;

			public Iothreadsched() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_scheduler(String _scheduler) {
				this._scheduler = _scheduler;
			}

			public String get_scheduler() {
				return this._scheduler;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_iothreads(String _iothreads) {
				this._iothreads = _iothreads;
			}

			public String get_iothreads() {
				return this._iothreads;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_priority(String _priority) {
				this._priority = _priority;
			}

			public String get_priority() {
				return this._priority;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iothread_period {

			protected String text;

			public Iothread_period() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Global_period {

			protected String text;

			public Global_period() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Emulator_quota {

			protected String text;

			public Emulator_quota() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Shares {

			protected String text;

			public Shares() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Vcpupin {

			protected String _vcpu;

			protected String _cpuset;

			public Vcpupin() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_vcpu(String _vcpu) {
				this._vcpu = _vcpu;
			}

			public String get_vcpu() {
				return this._vcpu;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_cpuset(String _cpuset) {
				this._cpuset = _cpuset;
			}

			public String get_cpuset() {
				return this._cpuset;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Cachetune {

			protected ArrayList<Cache> cache;

			protected ArrayList<Monitor> monitor;

			protected String _vcpus;

			public Cachetune() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setCache(ArrayList<Cache> cache) {
				this.cache = cache;
			}

			public ArrayList<Cache> getCache() {
				return this.cache;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setMonitor(ArrayList<Monitor> monitor) {
				this.monitor = monitor;
			}

			public ArrayList<Monitor> getMonitor() {
				return this.monitor;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_vcpus(String _vcpus) {
				this._vcpus = _vcpus;
			}

			public String get_vcpus() {
				return this._vcpus;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Cache {

				protected String _size;

				protected String _unit;

				protected String _level;

				protected String _type;

				protected String _id;

				public Cache() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_size(String _size) {
					this._size = _size;
				}

				public String get_size() {
					return this._size;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_unit(String _unit) {
					this._unit = _unit;
				}

				public String get_unit() {
					return this._unit;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_level(String _level) {
					this._level = _level;
				}

				public String get_level() {
					return this._level;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_type(String _type) {
					this._type = _type;
				}

				public String get_type() {
					return this._type;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_id(String _id) {
					this._id = _id;
				}

				public String get_id() {
					return this._id;
				}
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Monitor {

				protected String _level;

				protected String _vcpus;

				public Monitor() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_level(String _level) {
					this._level = _level;
				}

				public String get_level() {
					return this._level;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_vcpus(String _vcpus) {
					this._vcpus = _vcpus;
				}

				public String get_vcpus() {
					return this._vcpus;
				}
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Quota {

			protected String text;

			public Quota() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Iothread_quota {

			protected String text;

			public Iothread_quota() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setText(String text) {
				this.text = text;
			}

			public String getText() {
				return this.text;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Memorytune {

			protected ArrayList<Node> node;

			protected String _vcpus;

			public Memorytune() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void setNode(ArrayList<Node> node) {
				this.node = node;
			}

			public ArrayList<Node> getNode() {
				return this.node;
			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_vcpus(String _vcpus) {
				this._vcpus = _vcpus;
			}

			public String get_vcpus() {
				return this._vcpus;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Node {

				protected String _bandwidth;

				protected String _id;

				public Node() {

				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_bandwidth(String _bandwidth) {
					this._bandwidth = _bandwidth;
				}

				public String get_bandwidth() {
					return this._bandwidth;
				}

				/**
				 * Ignore the user setting, use 'lifecycle' to update VM's info
				 *
				 */
				public void set_id(String _id) {
					this._id = _id;
				}

				public String get_id() {
					return this._id;
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Genid {

		protected String text;

		public Genid() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Iothreads {

		protected String text;

		public Iothreads() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Name {

		protected String text;

		public Name() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CurrentMemory {

		protected String _unit;

		protected String text;

		public CurrentMemory() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void set_unit(String _unit) {
			this._unit = _unit;
		}

		public String get_unit() {
			return this._unit;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setText(String text) {
			this.text = text;
		}

		public String getText() {
			return this.text;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Pm {

		protected Suspend_to_disk suspend_to_disk;

		protected Suspend_to_mem suspend_to_mem;

		public Pm() {

		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSuspend_to_disk(Suspend_to_disk suspend_to_disk) {
			this.suspend_to_disk = suspend_to_disk;
		}

		public Suspend_to_disk getSuspend_to_disk() {
			return this.suspend_to_disk;
		}

		/**
		 * Ignore the user setting, use 'lifecycle' to update VM's info
		 *
		 */
		public void setSuspend_to_mem(Suspend_to_mem suspend_to_mem) {
			this.suspend_to_mem = suspend_to_mem;
		}

		public Suspend_to_mem getSuspend_to_mem() {
			return this.suspend_to_mem;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Suspend_to_disk {

			protected String _enabled;

			public Suspend_to_disk() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_enabled(String _enabled) {
				this._enabled = _enabled;
			}

			public String get_enabled() {
				return this._enabled;
			}
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Suspend_to_mem {

			protected String _enabled;

			public Suspend_to_mem() {

			}

			/**
			 * Ignore the user setting, use 'lifecycle' to update VM's info
			 *
			 */
			public void set_enabled(String _enabled) {
				this._enabled = _enabled;
			}

			public String get_enabled() {
				return this._enabled;
			}
		}
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Source {
		
		protected String _type;
		
		protected String _path;
		
		protected String _mode;
		
		protected String _dev;

		public Source() {
			super();
			// TODO Auto-generated constructor stub
		}

		public String get_type() {
			return _type;
		}

		public void set_type(String _type) {
			this._type = _type;
		}

		public String get_path() {
			return _path;
		}

		public void set_path(String _path) {
			this._path = _path;
		}

		public String get_mode() {
			return _mode;
		}

		public void set_mode(String _mode) {
			this._mode = _mode;
		}

		public String get_dev() {
			return _dev;
		}

		public void set_dev(String _dev) {
			this._dev = _dev;
		}
	}
}


