/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import java.util.Map;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

import io.fabric8.kubernetes.api.model.KubernetesResource;
import io.fabric8.kubernetes.api.model.Status;
import io.fabric8.kubernetes.api.model.apiextensions.CustomResourceDefinitionSpec;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @author xianghao16@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @since Thu Jun 13 21:44:40 CST 2019
 **/
@SuppressWarnings("rawtypes")
@JsonDeserialize(using = JsonDeserializer.None.class)
@Deprecated
public class UITSnapshotSpec extends CustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1171174592223281364L;

	protected Map<String, String> description;

	protected String nodeName;
	
	protected Result result;
	
	protected Data data;
	
	protected String obj;
	
	protected Lifecycle lifecycle;
	
	protected Status status;
	
	public UITSnapshotSpec() {

	}

	public Lifecycle getLifecycle() {
		return lifecycle;
	}

	public void setLifecycle(Lifecycle lifecycle) {
		this.lifecycle = lifecycle;
	}

	public String getNodeName() {
		return nodeName;
	}

	public void setNodeName(String nodeName) {
		this.nodeName = nodeName;
	}

	public Result getResult() {
		return result;
	}

	public void setResult(Result result) {
		this.result = result;
	}

	public Data getData() {
		return data;
	}

	public void setData(Data data) {
		this.data = data;
	}

	public String getObj() {
		return obj;
	}

	public void setObj(String obj) {
		this.obj = obj;
	}

	public Map<String, String> getDescription() {
		return description;
	}

	public void setDescription(Map<String, String> description) {
		this.description = description;
	}

	public Status getStatus() {
		return status;
	}

	public void setStatus(Status status) {
		this.status = status;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Result {
		/**
		 * 
		 */
		protected int code;
		
		protected String msg;

		public Result() {
			super();
		}

		public int getCode() {
			return code;
		}

		public void setCode(int code) {
			this.code = code;
		}

		public String getMsg() {
			return msg;
		}

		public void setMsg(String msg) {
			this.msg = msg;
		}
		
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Data {
		
		protected String sname;
		
		protected String name;
		
		protected String poolname;
		
		protected String date;
		
		protected String path;
		
		protected String filetype;
		
		protected Long vmsize;
		
		public String getSname() {
			return sname;
		}

		public void setSname(String sname) {
			this.sname = sname;
		}

		public String getDate() {
			return date;
		}

		public void setDate(String date) {
			this.date = date;
		}

		public Long getVmsize() {
			return vmsize;
		}

		public void setVmsize(Long vmsize) {
			this.vmsize = vmsize;
		}

		public String getPath() {
			return path;
		}

		public void setPath(String path) {
			this.path = path;
		}

		public String getFiletype() {
			return filetype;
		}

		public void setFiletype(String filetype) {
			this.filetype = filetype;
		}

		public String getName() {
			return name;
		}

		public void setName(String name) {
			this.name = name;
		}

		public String getPoolname() {
			return poolname;
		}

		public void setPoolname(String poolname) {
			this.poolname = poolname;
		}

	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Lifecycle {
		
		protected CreateUITSnapshot createUITSnapshot;
		
		protected RecoveryUITSnapshot recoveryUITSnapshot;
		
		protected RemoveUITSnapshot removeUITSnapshot;
		
		public CreateUITSnapshot getCreateUITSnapshot() {
			return createUITSnapshot;
		}

		public void setCreateUITSnapshot(CreateUITSnapshot createUITSnapshot) {
			this.createUITSnapshot = createUITSnapshot;
		}

		public RecoveryUITSnapshot getRecoveryUITSnapshot() {
			return recoveryUITSnapshot;
		}

		public void setRecoveryUITSnapshot(RecoveryUITSnapshot recoveryUITSnapshot) {
			this.recoveryUITSnapshot = recoveryUITSnapshot;
		}

		public RemoveUITSnapshot getRemoveUITSnapshot() {
			return removeUITSnapshot;
		}

		public void setRemoveUITSnapshot(RemoveUITSnapshot removeUITSnapshot) {
			this.removeUITSnapshot = removeUITSnapshot;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class CreateUITSnapshot {
			
			protected String poolname;
			
			protected String name;
			
			protected String sname;

			public String getPoolname() {
				return poolname;
			}

			public void setPoolname(String poolname) {
				this.poolname = poolname;
			}

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getSname() {
				return sname;
			}

			public void setSname(String sname) {
				this.sname = sname;
			}

		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class RecoveryUITSnapshot {
			
			protected String poolname;
			
			protected String name;
			
			protected String sname;

			public String getPoolname() {
				return poolname;
			}

			public void setPoolname(String poolname) {
				this.poolname = poolname;
			}

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getSname() {
				return sname;
			}

			public void setSname(String sname) {
				this.sname = sname;
			}

		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class RemoveUITSnapshot {
			
			protected String poolname;
			
			protected String name;
			
			protected String sname;

			public String getPoolname() {
				return poolname;
			}

			public void setPoolname(String poolname) {
				this.poolname = poolname;
			}

			public String getName() {
				return name;
			}

			public void setName(String name) {
				this.name = name;
			}

			public String getSname() {
				return sname;
			}

			public void setSname(String sname) {
				this.sname = sname;
			}

		}
		
	}
}
