# HW46 — Managed Kubernetes в Yandex Cloud

## Цель работы

Развернуть Managed Kubernetes кластер в Yandex Cloud при помощи Terraform и выполнить базовую настройку Kubernetes:

- создать кластер и node group;
- настроить IAM и Security Group;
- подключиться через kubectl;
- развернуть приложение;
- настроить Service разных типов;
- проверить LoadBalancer;
- настроить Storage через PVC/PV;
- проверить self-healing Deployment.

---

# Архитектура

```text
Terraform
 ├── Managed Kubernetes Cluster
 ├── Node Group
 ├── Service Accounts
 ├── IAM Roles
 ├── Security Group
 └── Network/Subnet

Kubernetes
 ├── Namespace
 ├── ServiceAccount
 ├── Role
 ├── RoleBinding
 ├── Deployment
 ├── ClusterIP Service
 ├── NodePort Service
 ├── LoadBalancer Service
 ├── PersistentVolumeClaim
 ├── PersistentVolume
 └── Pod с volume
```

---

# Terraform часть

## Что было создано

### Managed Kubernetes Cluster

```text
Cluster name: hw46-k8s-cluster
Version: 1.31
Zone: ru-central1-a
```

### Node Group

```text
platform_id = standard-v3
cores       = 2
memory      = 2 GB
disk        = network-ssd 32 GB
preemptible = true
nat         = true
```

### Service Accounts

Созданы:

```text
hw46-k8s-manager
hw46-k8s-node-sa
```

### IAM роли

```text
k8s.clusters.agent
load-balancer.admin
vpc.publicAdmin
container-registry.images.puller
```

### Security Group

Разрешены:

```text
22
443
6443
30000-32767
internal traffic
health checks
```

---

# Важная проблема

## Node Group зависал в PROVISIONING

Первоначально размер диска был:

```text
24 GB
```

Node group не создавался и Terraform зависал.

Причина:

```text
Managed Kubernetes требует минимум 30 GB для node group.
```

Исправление:

```text
node_disk_size = 32
```

После изменения node group успешно создался.

---

# Подключение к кластеру

Получение kubeconfig:

```powershell
yc managed-kubernetes cluster get-credentials `
  --id cattlm4lsua4h3gogbvm `
  --external `
  --force
```

Проверка:

```powershell
kubectl cluster-info
kubectl get nodes -o wide
```

---

# Kubernetes RBAC

Созданы:

## Namespace

```text
hw46
```

## ServiceAccount

```text
hw46-sa
```

## Role

```text
pods/services:
- get
- list
- watch
```

## RoleBinding

Привязка Role к ServiceAccount.

---

# Deployment

Создан Deployment:

```text
hw46-nginx
replicas = 2
image = nginx:1.27
```

Проверка:

```powershell
kubectl get deployment -n hw46
kubectl get pods -n hw46
```

---

# Self-healing проверка

Удаление Pod:

```powershell
kubectl delete pod -n hw46 -l app=hw46-nginx
```

Kubernetes автоматически создал новые Pod.

Это подтверждает работу:

```text
Deployment
ReplicaSet
desired state
self-healing
```

---

# Kubernetes Services

## ClusterIP

Внутренний сервис:

```text
hw46-nginx-clusterip
```

Проверка endpoints:

```powershell
kubectl get endpoints -n hw46
```

---

## NodePort

Создан:

```text
NodePort: 30080
```

Проверка:

```powershell
curl http://51.250.95.43:30080
```

---

## LoadBalancer

Создан сервис:

```text
hw46-nginx-loadbalancer
```

Yandex Cloud автоматически создал:

```text
Network Load Balancer
External IP
Target Group
```

Проверка:

```powershell
curl http://89.169.185.5
```

---

# Проблема с LoadBalancer

Первоначально:

```text
curl -> Empty reply from server
```

Причина:

```text
Security Group не разрешал health checks от Yandex Load Balancer.
```

Target был:

```text
UNHEALTHY
```

Исправление:

Добавлено правило:

```text
predefined_target = "loadbalancer_healthchecks"
```

После этого:

```text
Target -> HEALTHY
LoadBalancer заработал
```

---

# Storage

Проверка StorageClass:

```powershell
kubectl get storageclass
```

Использован:

```text
yc-network-hdd
```

---

# PVC

Создан:

```text
hw46-pvc
```

```yaml
storage: 1Gi
accessMode: ReadWriteOnce
```

---

# PV

PersistentVolume создался автоматически через CSI-driver.

Проверка:

```powershell
kubectl get pvc -n hw46
kubectl get pv
```

---

# Pod с volume

Создан Pod:

```text
hw46-storage-pod
```

Volume mounted:

```text
/usr/share/nginx/html
```

Проверка записи:

```powershell
kubectl exec -n hw46 hw46-storage-pod -- sh -c "echo 'Hello from HW46 PVC' > /usr/share/nginx/html/index.html"

kubectl exec -n hw46 hw46-storage-pod -- cat /usr/share/nginx/html/index.html
```

Результат:

```text
Hello from HW46 PVC
```

Это подтверждает работу Persistent Volume.

---

# Проверки

## Kubernetes

```powershell
kubectl get all -n hw46
kubectl get svc -n hw46
kubectl get pvc -n hw46
kubectl get pv
kubectl get nodes -o wide
```

## Yandex Cloud

```powershell
yc managed-kubernetes cluster list
yc managed-kubernetes node-group list
yc compute instance list
yc load-balancer network-load-balancer list
```

---

# Итог

В ходе работы был успешно развернут Managed Kubernetes кластер в Yandex Cloud через Terraform.

Были настроены:

- RBAC;
- Deployment;
- ClusterIP;
- NodePort;
- LoadBalancer;
- Persistent Volumes;
- динамический Storage;
- self-healing Deployment.

Также были диагностированы и исправлены проблемы:

- недостаточный размер диска node group;
- health checks для LoadBalancer.

В результате кластер успешно работает и обслуживает приложение nginx через Kubernetes Services и Yandex Cloud Load Balancer.