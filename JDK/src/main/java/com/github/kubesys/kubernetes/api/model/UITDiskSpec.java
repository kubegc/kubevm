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
public class UITDiskSpec extends CustomResourceDefinitionSpec implements KubernetesResource {

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
	
	public UITDiskSpec() {

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
		
		protected String path;
		
		protected String filetype;
		
		protected Long size;
		
		protected String name;
		
		protected String poolname;

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

		public Long getSize() {
			return size;
		}

		public void setSize(Long size) {
			this.size = size;
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
		
		protected CreateUITDisk createUITDisk;
		
		protected ExpandUITDisk expandUITDisk;

		protected DeleteUITDisk deleteUITDisk;
		
		protected ReleaseUITDisk releaseUITDisk;
		
		protected PrepareUITDisk prepareUITDisk;
		
		public CreateUITDisk getCreateUITDisk() {
			return createUITDisk;
		}

		public void setCreateUITDisk(CreateUITDisk createUITDisk) {
			this.createUITDisk = createUITDisk;
		}

		public ExpandUITDisk getExpandUITDisk() {
			return expandUITDisk;
		}

		public void setExpandUITDisk(ExpandUITDisk expandUITDisk) {
			this.expandUITDisk = expandUITDisk;
		}

		public DeleteUITDisk getDeleteUITDisk() {
			return deleteUITDisk;
		}

		public void setDeleteUITDisk(DeleteUITDisk deleteUITDisk) {
			this.deleteUITDisk = deleteUITDisk;
		}

		
		public ReleaseUITDisk getReleaseUITDisk() {
			return releaseUITDisk;
		}

		public void setReleaseUITDisk(ReleaseUITDisk releaseUITDisk) {
			this.releaseUITDisk = releaseUITDisk;
		}

		public PrepareUITDisk getPrepareUITDisk() {
			return prepareUITDisk;
		}

		public void setPrepareUITDisk(PrepareUITDisk prepareUITDisk) {
			this.prepareUITDisk = prepareUITDisk;
		}



		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class CreateUITDisk {
			
			protected String poolname;
			
			protected String name;
			
			protected Long size;

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

			public Long getSize() {
				return size;
			}

			public void setSize(Long size) {
				this.size = size;
			}
			
		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class ExpandUITDisk {
			
			protected String poolname;
			
			protected String name;
			
			protected Long size;

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

			public Long getSize() {
				return size;
			}

			public void setSize(Long size) {
				this.size = size;
			}
			
		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class DeleteUITDisk {
			
			protected String poolname;
			
			protected String name;
			
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

		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class ReleaseUITDisk {
			
			protected String poolname;
			
			protected String name;
			
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

		}
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class PrepareUITDisk {
			
			protected String poolname;
			
			protected String name;
			
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

		}
		
	}
}
