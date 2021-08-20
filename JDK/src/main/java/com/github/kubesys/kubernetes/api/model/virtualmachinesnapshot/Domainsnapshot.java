/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinesnapshot;

import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Domain;
import com.github.kubesys.kubernetes.api.model.virtualmachine.Domain.Name;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @since Thu Jun 22 21:36:39 CST 2019
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
public class Domainsnapshot {
	
	protected Cookie cookie;

	protected Parent parent;

	protected Memory memory;

	protected CreationTime creationTime;

	protected Disks disks;

	protected Domain domain;

	protected Name name;

	protected Active active;

	protected Description description;

	protected State state;

	public Domainsnapshot() {

	}
	
	public Cookie getCookie() {
		return cookie;
	}

	public void setCookie(Cookie cookie) {
		this.cookie = cookie;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setParent(Parent parent) {
		this.parent = parent;
	}

	public Parent getParent() {
		return this.parent;
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
	public void setCreationTime(CreationTime creationTime) {
		this.creationTime = creationTime;
	}

	public CreationTime getCreationTime() {
		return this.creationTime;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setDisks(Disks disks) {
		this.disks = disks;
	}

	public Disks getDisks() {
		return this.disks;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setDomain(Domain domain) {
		this.domain = domain;
	}

	public Domain getDomain() {
		return this.domain;
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
	public void setActive(Active active) {
		this.active = active;
	}

	public Active getActive() {
		return this.active;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setDescription(Description description) {
		this.description = description;
	}

	public Description getDescription() {
		return this.description;
	}

	/**
	 * Ignore the user setting, use 'lifecycle' to update VM's info
	 *
	 */
	public void setState(State state) {
		this.state = state;
	}

	public State getState() {
		return this.state;
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Cookie {
		protected Cpu cpu;

		public Cpu getCpu() {
			return cpu;
		}

		public void setCpu(Cpu cpu) {
			this.cpu = cpu;
		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Cpu {
			
			protected String _check;
			
			protected String _match;
			
			protected String _mode;
			
			protected List<Feature> feature;
			
			protected Model model;

			public String get_check() {
				return _check;
			}

			public void set_check(String _check) {
				this._check = _check;
			}

			public String get_match() {
				return _match;
			}

			public void set_match(String _match) {
				this._match = _match;
			}

			public String get_mode() {
				return _mode;
			}

			public void set_mode(String _mode) {
				this._mode = _mode;
			}

			public List<Feature> getFeature() {
				return feature;
			}

			public void setFeature(List<Feature> feature) {
				this.feature = feature;
			}

			public Model getModel() {
				return model;
			}

			public void setModel(Model model) {
				this.model = model;
			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Feature {
				
				protected String _name;
				
				protected String _policy;

				public String get_name() {
					return _name;
				}

				public void set_name(String _name) {
					this._name = _name;
				}

				public String get_policy() {
					return _policy;
				}

				public void set_policy(String _policy) {
					this._policy = _policy;
				}

			}
			
			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Model {
				
				protected String _fallback;
				
				protected String text;

				public String get_fallback() {
					return _fallback;
				}

				public void set_fallback(String _fallback) {
					this._fallback = _fallback;
				}

				public String getText() {
					return text;
				}

				public void setText(String text) {
					this.text = text;
				}
				
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Parent {

		protected Name name;

		public Parent() {

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
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Memory {

		protected String _file;

		protected String _snapshot;

		public Memory() {

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
		public void set_snapshot(String _snapshot) {
			this._snapshot = _snapshot;
		}

		public String get_snapshot() {
			return this._snapshot;
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class CreationTime {

		protected String text;

		public CreationTime() {

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
	public static class Disks {

		protected ArrayList<Disk> disk;

		public Disks() {

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

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Disk {

			protected String _snapshot;

			protected String _name;

			protected Driver driver;

			protected Source source;
			
			protected String _type;

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
			public void setSource(Source source) {
				this.source = source;
			}

			public Source getSource() {
				return this.source;
			}

			@JsonInclude(JsonInclude.Include.NON_NULL)
			@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
			public static class Driver {

				protected String _type;

				public Driver() {

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
				
				protected String _file;

				protected Encryption encryption;

				protected Reservations reservations;

				protected String _startupPolicy;

				public Source() {

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

					public Domain.Source getSource() {
						return source;
					}

					public void setSource(Domain.Source source) {
						this.source = source;
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
					public void set_enabled(String _enabled) {
						this._enabled = _enabled;
					}

					public String get_enabled() {
						return this._enabled;
					}

					
				}
			}
		}
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Active {

		protected String text;

		public Active() {

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
	public static class State {

		protected String text;

		public State() {

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
