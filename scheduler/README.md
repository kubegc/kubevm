# Scheduler (GA)

Queue-oriented, Model-free Kubernetes's scheduler for Various Application Lifecycle Management

Please see project [kubeext-scheduler](https://github.com/kubesys/kubeext-scheduler)

# Prerequisite

Ensure you have configured GOROOT and GOPATH

- IDE: GoLand 
- Go: >= 1.12.9

# Deploy Steps
#### Prerequisite

You are on the master with installed kubernetes

#### Step 1: Add code to kube-scheduler source code
Find `$GOPATH/k8s.io/kubernetes/pkg/scheduler/scheduler.go`, namely original `scheduler.go`.
Find `$GOPATH/k8s.io/kubernetes/pkg/scheduler/factory/factory.go`, namely original `factory.go`.

Copy all the code snippets in file `<RepoPath>/diff.go` to the end of `scheduler.go`, resolve all the import and package problems, then find `func (sched *Scheduler) Run()` in original `scheduler.go`(around line 281), change it as shown below.

find `func(sched *Scheduler) scheduleOne()` in original `scheduler.go`, insert several lines of code behind 
`suggestedHost, err := sched.schedule(pod)`
(around line 540). After the insertion, `func(sched *Scheduler) scheduleOne()` should look like this:

```go
func (sched *Scheduler) scheduleOne() {
	[...]
	start := time.Now()
	scheduleResult, err := sched.schedule(pod)
	if err != nil {
	   ...
	} 
	 //--------------------------------------
	 //          Support CRD
	 //-------------------------------------
	 if pod.GetAnnotations()["crdKind"] != "" {
		SupportCRD(scheduleResult.SuggestedHost,
			pod, sched.config.CoreClient, sched.config.CRDClient)
		return
	}
	   
```

#### Step 2: Rebuild scheduler
Move to `$GOPATH/k8s.io/kubernetes/cmd/kube-scheduler/`, and build with command `env GOOS=linux GOARCH=amd64 go build scheduler.go`, now you get a executable binary file `scheduler`.
#### Step 3: Pack as a image
Build the image with `<RepoPath>/build/Dockerfile`, before that you need to move executable scheduler binary file to /build path, then build image with command.

```
cp scheduler docker/
cp /etc/kubernetes/admin.conf docker/
docker build docker/ -t registry.cn-hangzhou.aliyuncs.com/cloudplus-lab/kubevirt-scheduler:v1.14.6
```
#### Step 4: Deploy
Created a Deployment configuration file and ran it in an existing Kubernetes cluster, using the Deployment resource rather than creating a Pod resource directly because the Deployment resource can better handle the case of a scheduler running node failure. We offered a Deployment configuration example, saved as the `custom-scheduler.yaml` in `<RepoPath>/yaml/`.

Then Create Deployment resource in Kubernetes cluster

```
kubectl create -f yamls/KubeCRDScheduler.yaml
```

# Run in Goland IDE

```
--kubeconfig=/etc/kubernetes/admin.conf --scheduler-name=kubecrd-scheduler --port=10253 --secure-port=10261 --leader-elect=true --lock-object-namespace=cloudplus
```
