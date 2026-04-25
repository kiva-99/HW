# Kubernetes — шпаргалка (HW44)

## 📌 Базовая идея

Kubernetes = оркестратор контейнеров

```text
Ты описываешь желаемое состояние
↓
Kubernetes сам его поддерживает
```

---

## 📦 Основные сущности

### Pod
- минимальная единица запуска
- внутри контейнер(ы)
- имеет свой IP (меняется при пересоздании)

---

### Deployment
- описывает приложение
- управляет ReplicaSet
- задаёт:
  - образ
  - количество реплик
  - labels

```text
Deployment → ReplicaSet → Pods
```

---

### ReplicaSet
- следит за количеством pod'ов
- если pod умер → создаёт новый

---

### Service
- стабильная точка доступа к pod'ам
- работает через labels

```text
Client → Service → Pod
```

Типы:
- ClusterIP (внутри кластера)
- NodePort (доступ снаружи)
- LoadBalancer (в облаке)

---

### Labels + Selector

```yaml
labels:
  app: nginx

selector:
  app: nginx
```

👉 Service находит pod’ы через labels

---

### EndpointSlice
- список реальных IP pod'ов
- куда Service шлёт трафик

---

## ⚙️ Основные команды

### Кластер

```powershell
minikube start --driver=docker
kubectl cluster-info
kubectl get nodes
```

---

### Объекты

```powershell
kubectl get all
kubectl get pods
kubectl get deploy
kubectl get svc
```

---

### Применение YAML

```powershell
kubectl apply -f file.yaml
```

---

### Логи и диагностика

```powershell
kubectl logs <pod>
kubectl logs deployment/<name>
kubectl describe pod <pod>
kubectl describe deployment <name>
```

---

### EndpointSlice

```powershell
kubectl get endpointslices
kubectl describe endpointslice
```

---

### Port-forward (доступ извне)

```powershell
kubectl port-forward service/<name> 8080:80
```

---

### Удаление

```powershell
kubectl delete pod <name>
```

👉 Kubernetes пересоздаст pod (self-healing)

---

### Масштабирование

```powershell
kubectl scale deployment <name> --replicas=3
```

---

## 🔥 Важные концепции

### Self-healing

```text
Pod умер → Kubernetes создал новый
```

---

### Scaling

```text
Меняем replicas → Kubernetes добавляет/удаляет pod'ы
```

---

### Declarative approach

```text
Ты пишешь YAML
а не команды "запусти контейнер"
```

---

### Service routing

```text
Service не знает pod'ы напрямую
он использует labels
```

---

## 🧠 Частые ошибки

❌ selector ≠ labels → Service не работает  
❌ забыли Service → нет доступа к pod  
❌ containerPort ≠ targetPort → нет ответа  
❌ NodePort вне диапазона 30000–32767  

---

## 💡 Минимальный набор для запуска приложения

1. Deployment
2. Service

---

## 📊 Минимальная архитектура

```text
User
 ↓
Service
 ↓
Pod (nginx / app)
 ↓
Container
```

---

## 🚀 Что нужно помнить на контрольной

- Pod — не контейнер
- Deployment управляет ReplicaSet
- ReplicaSet управляет pod’ами
- Service работает через labels
- Kubernetes сам восстанавливает состояние
- scaling = изменение replicas