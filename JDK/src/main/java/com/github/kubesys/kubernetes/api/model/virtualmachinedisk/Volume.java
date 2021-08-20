/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model.virtualmachinedisk;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @author xuyuanjia2017@otcaix.iscas.ac.cn
 * @author xianghao16@otcaix.iscas.ac.cn
 * @author yangchen18@otcaix.iscas.ac.cn
 * @since Thu Jun 22 21:36:39 CST 2019
 **/
@JsonInclude(JsonInclude.Include.NON_NULL)
@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
public class Volume {

	protected String actual_size;
	
	protected String backing_filename;
	
	protected String backing_filename_format;
	
	protected String cluster_size;
	
	protected String current;
	
	protected String dirty_flag;
	
	protected String disk;
	
	protected String filename;
	
	protected String format;
	
	protected FormatSpecific format_specific;
	
	protected String full_backing_filename;
	
	protected String virtual_size;
	
	protected String pool;

	protected String uni;
	
	protected String disktype;

	protected String poolname;
	
	public String getDisktype() {
		return disktype;
	}

	public void setDisktype(String disktype) {
		this.disktype = disktype;
	}

	public String getPool() {
		return pool;
	}

	public void setPool(String pool) {
		this.pool = pool;
	}

	public String getPoolname() {
		return poolname;
	}

	public void setPoolname(String poolname) {
		this.poolname = poolname;
	}

	public String getUni() {
		return uni;
	}

	public void setUni(String uni) {
		this.uni = uni;
	}

	public String getBacking_filename_format() {
		return backing_filename_format;
	}

	public void setBacking_filename_format(String backing_filename_format) {
		this.backing_filename_format = backing_filename_format;
	}

	public String getDisk() {
		return disk;
	}

	public void setDisk(String disk) {
		this.disk = disk;
	}

	public String getBacking_filename() {
		return backing_filename;
	}

	public void setBacking_filename(String backing_filename) {
		this.backing_filename = backing_filename;
	}

	@JsonInclude(JsonInclude.Include.NON_NULL)
	@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
	public static class FormatSpecific {
		
		protected Data data;
		
		protected String type;
		
		@JsonInclude(JsonInclude.Include.NON_NULL)
		@JsonDeserialize(using = com.fasterxml.jackson.databind.JsonDeserializer.None.class)
		public static class Data {
			
			protected String compat;
			
			protected Boolean corrupt;
			
			protected Boolean lazy_refcounts;
			
			protected String refcount_bits;

			public String getCompat() {
				return compat;
			}

			public void setCompat(String compat) {
				this.compat = compat;
			}

			public Boolean getCorrupt() {
				return corrupt;
			}

			public void setCorrupt(Boolean corrupt) {
				this.corrupt = corrupt;
			}

			public Boolean getLazy_refcounts() {
				return lazy_refcounts;
			}

			public void setLazy_refcounts(Boolean lazy_refcounts) {
				this.lazy_refcounts = lazy_refcounts;
			}

			public String getRefcount_bits() {
				return refcount_bits;
			}

			public void setRefcount_bits(String refcount_bits) {
				this.refcount_bits = refcount_bits;
			}
		}

		public Data getData() {
			return data;
		}

		public void setData(Data data) {
			this.data = data;
		}

		public String getType() {
			return type;
		}

		public void setType(String type) {
			this.type = type;
		}
	}

	public String getActual_size() {
		return actual_size;
	}

	public void setActual_size(String actual_size) {
		this.actual_size = actual_size;
	}

	public String getCluster_size() {
		return cluster_size;
	}

	public void setCluster_size(String cluster_size) {
		this.cluster_size = cluster_size;
	}

	public String getCurrent() {
		return current;
	}

	public void setCurrent(String current) {
		this.current = current;
	}

	public String getDirty_flag() {
		return dirty_flag;
	}

	public void setDirty_flag(String dirty_flag) {
		this.dirty_flag = dirty_flag;
	}

	public String getFilename() {
		return filename;
	}

	public void setFilename(String filename) {
		this.filename = filename;
	}

	public String getFormat() {
		return format;
	}

	public void setFormat(String format) {
		this.format = format;
	}

	public FormatSpecific getFormat_specific() {
		return format_specific;
	}

	public void setFormat_specific(FormatSpecific format_specific) {
		this.format_specific = format_specific;
	}

	public String getFull_backing_filename() {
		return full_backing_filename;
	}

	public void setFull_backing_filename(String full_backing_filename) {
		this.full_backing_filename = full_backing_filename;
	}

	public String getVirtual_size() {
		return virtual_size;
	}

	public void setVirtual_size(String virtual_size) {
		this.virtual_size = virtual_size;
	}
}
