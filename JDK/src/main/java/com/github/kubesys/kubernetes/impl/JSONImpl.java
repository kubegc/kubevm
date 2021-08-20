/**
 * Copyright (2019, ) Institute of Software, Chinese Academy of Sciences
 */
package com.github.kubesys.kubernetes.impl;

import java.lang.reflect.Method;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import java.util.function.Predicate;

import com.alibaba.fastjson.JSON;
import com.github.kubesys.kubernetes.ExtendedKubernetesClient;

import io.fabric8.kubernetes.api.builder.Visitor;
import io.fabric8.kubernetes.api.model.HasMetadata;
import io.fabric8.kubernetes.client.dsl.ParameterNamespaceListVisitFromServerGetDeleteRecreateWaitApplicable;

/**
 * @author wuheng@otcaix.iscas.ac.cn
 * @since  Thu Oct 10 21:39:55 CST 2019
 **/
@SuppressWarnings("rawtypes")
public class JSONImpl implements ParameterNamespaceListVisitFromServerGetDeleteRecreateWaitApplicable {

	protected final static String API_MODEL_PACKAGE = "com.github.kubesys.kubernetes.api.model.";
	
	protected final AbstractImpl impl;
	
	protected final HasMetadata object;
	
	public JSONImpl(ExtendedKubernetesClient client, String kind, String jsonStr) throws Exception {
		super();
		Method method = client.getClass().getMethod(getMethodName(kind));
		this.impl = (AbstractImpl) method.invoke(client);
		Type type = Class.forName(API_MODEL_PACKAGE + kind);
		this.object = (HasMetadata) JSON.parseObject(jsonStr, type);
	}

	@Override
	public List<HasMetadata> createOrReplace() {
		List<HasMetadata> mdl = new ArrayList<HasMetadata>();
		String name = object.getMetadata().getName();
		try {
			if (impl.get(name) == null) {
				impl.create(object);
			} else {
				impl.update((HasMetadata) object); 
			}
		} catch (Exception ex) {
			throw new RuntimeException(ex);
		}
		mdl.add((HasMetadata)impl.get(name));
		return mdl;
	}

	@Override
	public Object delete() {
		try {
			impl.delete(object); 
		} catch (Exception ex) {
			throw new RuntimeException(ex);
		}
		return object;
	}

	public static String getMethodName(String kind) {
		return kind.substring(0, 1).toLowerCase() + kind.substring(1) + "s";
	}
	
	// ============================
	@Override
	public Object inNamespace(String name) {
		return null;
	}

	@Override
	public Object waitUntilReady(long amount, TimeUnit timeUnit) throws InterruptedException {
		return null;
	}

	@Override
	public Object waitUntilCondition(Predicate condition, long amount, TimeUnit timeUnit) throws InterruptedException {
		return null;
	}

	@Override
	public Object withGracePeriod(long gracePeriodSeconds) {
		return null;
	}

	@Override
	public Object get() {
		return null;
	}

	@Override
	public Object deletingExisting() {
		return null;
	}

	@Override
	public Object accept(Visitor visitor) {
		return null;
	}

	@Override
	public Object withParameters(Map parameters) {
		return null;
	}

	@Override
	public Object cascading(boolean enabled) {
		return null;
	}

	@Override
	public Object createOrReplaceAnd() {
		return null;
	}

	@Override
	public Object apply() {
		return null;
	}

	@Override
	public Object fromServer() {
		return null;
	}

	@Override
	public Object withPropagationPolicy(String propagationPolicy) {
		// TODO Auto-generated method stub
		return null;
	}
	
}