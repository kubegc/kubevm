# Scheduler (GA)

Queue-oriented, Model-free Kubernetes's scheduler for Various Application Lifecycle Management

Note that this is a stable solution from ISCAS, please see project [kubeext-scheduler](https://github.com/kubesys/kubeext-scheduler).
So what we need to do is release it for a specific Kubernetes' version

# Prerequisite

Ensure you have configured GOROOT and GOPATH

- IDE: GoLand 
- Go: >= 1.12.9

# Roadmap

- for Kubernetes 1.14.1 (20190630)
- for Kubernetes 1.14.6 (20190930)
- for Kubernetes 1.15.6 (20191230)
- for Kubernetes 1.17.1 (20200201)

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

- https://system51.github.io/2019/12/05/Kubeadm-certificate-modified/
- https://github.com/kubernetes/kubernetes (see You have a working Docker environment.)
