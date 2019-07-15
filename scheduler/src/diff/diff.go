/************************************************************************************
 *
 *                        Model free architecture
 *
 *   author: wuheng@otcaix.iscas.ac.cn
 *   author: xianghao16@otcaix.iscas.ac.cn
 *   author: yangchen18@otcaix.iscas.ac.cn
 ************************************************************************************/


func NewCRDClient() (dynamic.Interface, error) {
	bytes, _ := ioutil.ReadFile("/etc/kubernetes/admin.conf")
	config, _ := clientcmd.NewClientConfigFromBytes(bytes)
	clientConfig, _ := config.ClientConfig()
	return dynamic.NewForConfig(clientConfig)
}

// we would consider some exceptions later
func SupportCRD(suggestedHost string, pod *v1.Pod, coreClient clientset.Interface, crdClient dynamic.Interface) {

	gvr := schema.GroupVersionResource {
		Group:    pod.GetAnnotations()["crdGroup"],
		Version:  pod.GetAnnotations()["crdVersion"],
		Resource: pod.GetAnnotations()["crdKind"],
	}

	// bind resource
	resource, _ := crdClient.Resource(gvr).Namespace(pod.GetAnnotations()["crdNamespace"]).
								Get(pod.GetAnnotations()["crdName"], metav1.GetOptions{})

	// add nodeName
	if resource != nil {
		resource.Object["spec"].(map[string]interface{})["nodeName"] = suggestedHost

		labels := make(map[string]interface{})
		labels["host"] = suggestedHost
		resource.Object["metadata"].(map[string]interface{})["labels"] = labels

		crdClient.Resource(gvr).Namespace(pod.GetAnnotations()["crdNamespace"]).
										Update(resource, metav1.UpdateOptions{})
	}


	// delete this pod
	coreClient.CoreV1().Pods("default").Delete(pod.GetName(), &metav1.DeleteOptions{})

}

