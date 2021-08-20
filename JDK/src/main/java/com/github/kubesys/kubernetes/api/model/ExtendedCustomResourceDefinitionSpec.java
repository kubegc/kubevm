/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.api.model;

import java.util.Map;

import com.fasterxml.jackson.databind.JsonDeserializer;
import com.fasterxml.jackson.databind.annotation.JsonDeserialize;

import io.fabric8.kubernetes.api.model.Affinity;
import io.fabric8.kubernetes.api.model.Status;
import io.fabric8.kubernetes.api.model.apiextensions.CustomResourceDefinitionSpec;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * 
 * @version 1.0.0
 * @since  Thu Aug 29 21:44:40 CST 2019
 * 
 * This class is used for supporting advanced scheduling policy 
 * for CustomResourceDefinition(CRD).
 **/
@JsonDeserialize(using = JsonDeserializer.None.class)
public abstract class ExtendedCustomResourceDefinitionSpec extends CustomResourceDefinitionSpec {

	/**
	 * serialVersionUID
	 */
	private static final long serialVersionUID = 1171174592223281364L;

	/**
	 * user description for CRD
	 */
	@Deprecated
	protected Map<String, String> description;

	/**
	 * just like 'docker images'
	 */
	@Deprecated
	protected String image;

	/**
	 * advanced scheduling policy based on node name
	 */
	protected String nodeName;
	
	/**
	 * advanced scheduling policy based on node selector
	 */
	protected Map<String, String> nodeSelector;

	/**
	 * affinity and anti-affinity
	 */
	protected Affinity affinity;
	
	/**
	 * CRD status
	 */
	protected Status status;

	/**
	 * @return                    user description
	 */
	public Map<String, String> getDescription() {
		return description;
	}

	/**
	 * set user description
	 * 
	 * @param description          description
	 */
	public void setDescription(Map<String, String> description) {
		this.description = description;
	}

	/**
	 * @return                     image name
	 */
	public String getImage() {
		return image;
	}

	/**
	 * set image name
	 * 
	 * @param image                image
	 */
	public void setImage(String image) {
		this.image = image;
	}

	/**
	 * @return                      node name
	 */
	public String getNodeName() {
		return nodeName;
	}

	/**
	 * set node name
	 * 
	 * @param nodeName              node name
	 */
	public void setNodeName(String nodeName) {
		this.nodeName = nodeName;
	}


	/**
	 * @return                      node selector
	 */
	public Map<String, String> getNodeSelector() {
		return nodeSelector;
	}

	/**
	 * @param nodeSelector          node selector
	 */
	public void setNodeSelector(Map<String, String> nodeSelector) {
		this.nodeSelector = nodeSelector;
	}

	/**
	 * @return                      affinity
	 */
	public Affinity getAffinity() {
		return affinity;
	}

	/**
	 * @param affinity              set affinity
	 */
	public void setAffinity(Affinity affinity) {
		this.affinity = affinity;
	}

	/**
	 * @return                       status
	 */
	public Status getStatus() {
		return status;
	}

	/**
	 * set status
	 * 
	 * @param status                 status
	 */
	public void setStatus(Status status) {
		this.status = status;
	}
	
}
