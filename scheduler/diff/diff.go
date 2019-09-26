import (
        "k8s.io/apimachinery/pkg/runtime/schema"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
        "k8s.io/client-go/dynamic"
)

// New returns a Scheduler
func New(client clientset.Interface,
	......

        // Additional clients for CRD's lifecycle
        config.CoreClient = client
	config.CRDClient, _ = NewCRDClient()

	......
}

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

	var gvr = schema.GroupVersionResource {
		Group:    pod.GetAnnotations()["crdGroup"],
		Version:  pod.GetAnnotations()["crdVersion"],
		Resource: pod.GetAnnotations()["crdKind"],
	}

        // get resource
	resource, _ := crdClient.Resource(gvr).Namespace(pod.GetAnnotations()["crdNamespace"]).
		Get(pod.GetAnnotations()["crdName"], metav1.GetOptions{})

        // bind CRD resource
	if resource != nil {
		resource.Object["spec"].(map[string]interface{})["nodeName"] = suggestedHost

		labels := make(map[string]interface{})
		labels["host"] = suggestedHost

		if resource.Object["metadata"].(map[string]interface{})["labels"] != nil {
			for k, v := range resource.Object["metadata"].(map[string]interface{})["labels"].(map[string]interface{})  {
				labels[k] = v
			}
		}
		resource.Object["metadata"].(map[string]interface{})["labels"] = labels

                klog.Info(resource)

		// update CRD resource
		crdClient.Resource(gvr).Namespace(pod.GetAnnotations()["crdNamespace"]).Update(resource, metav1.UpdateOptions{})
	}

	// delete this pod
	coreClient.CoreV1().Pods("default").Delete(pod.GetName(), &metav1.DeleteOptions{})

}
