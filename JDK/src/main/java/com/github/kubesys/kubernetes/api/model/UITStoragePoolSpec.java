/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import java.util.List;
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
public class UITStoragePoolSpec extends CustomResourceDefinitionSpec implements KubernetesResource {

	/**
	 * 
	 */
	private static final long serialVersionUID = 1171174592223281364L;

	protected Map<String, String> description;

	protected String nodeName;
	
	protected Result result;
	
	protected List<Data> data;
	
	protected String obj;
	
	protected Lifecycle lifecycle;
	
	protected Status status;
	
	public UITStoragePoolSpec() {

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

	public List<Data> getData() {
		return data;
	}

	public void setData(List<Data> data) {
		this.data = data;
	}

	public String getObj() {
		return obj;
	}

	public void setObj(String obj) {
		this.obj = obj;
	}


	public Status getStatus() {
		return status;
	}

	public void setStatus(Status status) {
		this.status = status;
	}

	public Map<String, String> getDescription() {
		return description;
	}

	public void setDescription(Map<String, String> description) {
		this.description = description;
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
			// TODO Auto-generated constructor stub
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
		
		protected String status;
		
		protected String mountpath;
		
		protected String proto;
		
		protected String url;
		
		protected String poolname;
		
		protected Long free;
		
		protected String disktype;
		
		protected Long used;
		
		protected Long total;

		public String getStatus() {
			return status;
		}

		public void setStatus(String status) {
			this.status = status;
		}

		public String getMountpath() {
			return mountpath;
		}

		public void setMountpath(String mountpath) {
			this.mountpath = mountpath;
		}

		public String getProto() {
			return proto;
		}

		public void setProto(String proto) {
			this.proto = proto;
		}

		public String getUrl() {
			return url;
		}

		public void setUrl(String url) {
			this.url = url;
		}

		public String getPoolname() {
			return poolname;
		}

		public void setPoolname(String poolname) {
			this.poolname = poolname;
		}

		public Long getFree() {
			return free;
		}

		public void setFree(Long free) {
			this.free = free;
		}

		public String getDisktype() {
			return disktype;
		}

		public void setDisktype(String disktype) {
			this.disktype = disktype;
		}

		public Long getUsed() {
			return used;
		}

		public void setUsed(Long used) {
			this.used = used;
		}

		public Long getTotal() {
			return total;
		}

		public void setTotal(Long total) {
			this.total = total;
		}
	}
	
	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class Lifecycle {
		
		protected CreateUITPool createUITPool;
		
		protected DeleteUITPool deleteUITPool;

		public CreateUITPool getCreateUITPool() {
			return createUITPool;
		}

		public void setCreateUITPool(CreateUITPool createUITPool) {
			this.createUITPool = createUITPool;
		}

		public DeleteUITPool getDeleteUITPool() {
			return deleteUITPool;
		}

		public void setDeleteUITPool(DeleteUITPool deleteUITPool) {
			this.deleteUITPool = deleteUITPool;
		}

		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class CreateUITPool {
			
			protected String poolType;
			
			protected String poolname;
			
			protected String url;

			public String getPoolType() {
				return poolType;
			}

			public void setPoolType(String poolType) {
				this.poolType = poolType;
			}

			public String getPoolname() {
				return poolname;
			}

			public void setPoolname(String poolname) {
				this.poolname = poolname;
			}

			public String getUrl() {
				return url;
			}

			public void setUrl(String url) {
				this.url = url;
			}
			
		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class DeleteUITPool {
			
			protected String poolname;

			public String getPoolname() {
				return poolname;
			}

			public void setPoolname(String poolname) {
				this.poolname = poolname;
			}
			
		}
		
	}
}
