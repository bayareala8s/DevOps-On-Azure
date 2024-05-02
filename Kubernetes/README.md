## Azure Kubernetes Service (AKS)

Azure Kubernetes Service (AKS)
│
├── Control Plane (Master Node)
│   ├── etcd: Distributed key-value store for storing Kubernetes cluster state.
│   │   ├── Replicated across multiple nodes for high availability.
│   │   └── Provides consistent and fault-tolerant storage.
│   │
│   ├── API Server: Frontend for the Kubernetes control plane, serves Kubernetes API.
│   │   ├── Handles RESTful API requests for cluster management operations.
│   │   ├── Authenticates and authorizes requests.
│   │   └── Validates and processes requests against etcd.
│   │
│   ├── Scheduler: Component responsible for scheduling pods onto nodes.
│   │   ├── Selects optimal nodes based on resource requirements and constraints.
│   │   ├── Considers factors like CPU, memory, and locality.
│   │   └── Monitors node health and availability.
│   │
│   └── Controller Manager: Manages various controllers that regulate the state of the cluster.
│       ├── Node Controller: Manages lifecycle and configuration of nodes.
│       ├── Replication Controller: Maintains desired number of pod replicas.
│       ├── Endpoint Controller: Populates endpoint objects (e.g., services) with backend pod IPs.
│       └── Namespace Controller: Manages namespaces within the cluster.
│
├── Worker Nodes
│   ├── Node 1
│   │   ├── Kubelet: Agent that runs on each node and ensures that containers are running in a pod.
│   │   │   ├── Registers node with the API server.
│   │   │   ├── Receives pod definitions from API server and ensures their execution.
│   │   │   └── Monitors pod health and reports to API server.
│   │   │
│   │   ├── Kube Proxy: Network proxy that maintains network rules on nodes.
│   │   │   ├── Implements Kubernetes Service concept (ClusterIP, NodePort, LoadBalancer).
│   │   │   └── Manages pod-to-pod communication within the cluster.
│   │   │
│   │   └── Container Runtime: Software responsible for running containers.
│   │       ├── Docker: Popular container runtime supporting Docker images.
│   │       ├── containerd: Lightweight container runtime compatible with OCI standards.
│   │       └── CRI-O: Lightweight container runtime optimized for Kubernetes.
│   │
│   ├── Node 2
│   │   ├── Kubelet
│   │   ├── Kube Proxy
│   │   └── Container Runtime
│   │
│   └── ...
│
├── Load Balancer
│   ├── Public IP: Publicly accessible IP address assigned to the load balancer.
│   │
│   └── Routes Traffic to Pods: Distributes incoming traffic among pods based on defined rules.
│       ├── Azure Standard Load Balancer: Provides high availability and scalability.
│       └── Azure Application Gateway: Offers layer 7 (HTTP/HTTPS) load balancing and WAF capabilities.
│
├── Storage
│   ├── Azure Disk: Managed disks for persistent storage.
│   │   ├── Supports both Premium and Standard disk types.
│   │   └── Provides durability and high availability.
│   │
│   ├── Azure Files: Fully managed file shares for cloud applications.
│   │   ├── Supports SMB (Server Message Block) protocol.
│   │   └── Enables sharing of data between multiple pods.
│   │
│   └── Azure NetApp Files: Enterprise-grade shared file storage with NFSv4 support.
│       ├── High-performance file storage suitable for demanding workloads.
│       └── Integrated with Azure infrastructure for seamless deployment.
│
└── Networking
    ├── Virtual Network (VNet): Isolated network environment for deploying AKS resources.
    │   ├── Subnet Configuration: Allows grouping of resources within VNets.
    │   └── Address Space: Defines the IP address range for VNets.
    │
    ├── Network Security Groups (NSGs): Filter network traffic to and from AKS resources.
    │   ├── Inbound and Outbound Rules: Define allowed and denied traffic patterns.
    │   └── Associate with Subnets: Apply NSG rules to specific subnets.
    │
    └── Azure Container Networking Interface (CNI): Plugin for integrating Kubernetes pods with Azure networking.
        ├── IP Address Management: Assigns IP addresses to pods.
        ├── Network Policy Enforcement: Defines network policies for traffic control.
        └── Integration with Azure Virtual Network: Enables secure and efficient communication between pods and other Azure services.


### High-Level Architecture Diagram for CI/CD for AKS apps with Azure Pipelines

Here's a high-level architecture diagram for a CI/CD pipeline for AKS applications using Azure Pipelines:

```
+----------------+     +----------------+     +----------------+     +----------------+
|                |     |                |     |                |     |                |
|  Developer's   |     |   Azure Repo   |     | Azure Pipelines|     |   AKS Cluster  |
|  Local System  | --> | (Source Code)  | --> |  (CI/CD Tool)  | --> | (Deployed App) |
|                |     |                |     |                |     |                |
+----------------+     +----------------+     +----------------+     +----------------+
       |                      |                      |                      |
       |                      |                      |                      |
       v                      v                      v                      v
+----------------+     +----------------+     +----------------+     +----------------+
|                |     |                |     |                |     |                |
|   Git (VCS)    |     |   Build & Test |     |   Docker Image |     |   Kubernetes   |
|                |     |                |     |   Repository   |     |   Services     |
+----------------+     +----------------+     +----------------+     +----------------+
```

1. **Developer's Local System**: Developers write code on their local systems. They use Git for version control.

2. **Azure Repo (Source Code)**: The code is pushed to a repository in Azure Repo. This triggers the CI/CD pipeline in Azure Pipelines.

3. **Azure Pipelines (CI/CD Tool)**: Azure Pipelines pulls the latest code from Azure Repo. It then builds the Docker image, runs tests, and pushes the Docker image to a Docker image repository.

4. **AKS Cluster (Deployed App)**: Azure Pipelines deploys the Docker image to an AKS cluster. The application is now running in a Kubernetes service in the AKS cluster.

The arrows represent the flow of code and artifacts through the pipeline:

- Code flows from the developer's local system to Azure Repo.
- Azure Pipelines pulls the code from Azure Repo, builds and tests the code, and pushes the Docker image to a Docker image repository.
- Azure Pipelines deploys the Docker image from the Docker image repository to the AKS cluster.

This is a high-level overview and the actual implementation may vary based on specific requirements.
