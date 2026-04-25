# HW44 — Kubernetes #1

## 1. Цель работы

Цель домашнего задания — познакомиться с основами Kubernetes, его архитектурой, базовыми объектами и получить практический опыт развёртывания приложений в Kubernetes-кластере.

В рамках работы были выполнены следующие действия:

- изучены базовые понятия Kubernetes;
- поднят локальный Kubernetes-кластер с помощью Minikube;
- созданы Kubernetes-манифесты;
- развёрнуты два контейнеризированных приложения;
- настроены Deployment и Service;
- выполнена проверка состояния кластера через kubectl;
- проверены логи, endpoints, EndpointSlice;
- протестировано самовосстановление Kubernetes;
- протестировано ручное масштабирование приложения.

---

## 2. Используемые инструменты

| Инструмент | Назначение |
|---|---|
| Docker Desktop | Контейнерная среда, внутри которой запущен Minikube |
| Minikube | Локальный Kubernetes-кластер |
| kubectl | CLI для управления Kubernetes |
| PowerShell | Терминал |
| Git | Контроль версий |

Проверка версий:

```powershell
docker --version
kubectl version --client
minikube version
```

---

## 3. Структура проекта

```
HW44/
├── manifests/
│   ├── echo-deployment.yaml
│   ├── echo-service.yaml
│   ├── nginx-deployment.yaml
│   └── nginx-service.yaml
├── scripts/
├── notes.md
└── README.md
```

---

## 4. Основные понятия Kubernetes

### Node

Node — это машина в Kubernetes-кластере, на которой запускаются приложения.

### Pod

Pod — минимальная единица запуска. Внутри pod находится контейнер.

### Deployment

Deployment описывает:

- какой образ запускать;
- сколько реплик держать;
- какие labels использовать.

Цепочка:

```
Deployment → ReplicaSet → Pod → Container
```

### Service

Service — стабильная точка доступа к pod'ам.

Цепочка:

```
Client → Service → EndpointSlice → Pod → Container
```

### EndpointSlice

Содержит реальные IP pod'ов, на которые направляется трафик.

---

## 5. Запуск кластера

```powershell
minikube start --driver=docker
```

Проверка:

```powershell
kubectl cluster-info
kubectl get nodes
kubectl get pods -A
```

---

## 6. Приложение №1 — nginx

### Deployment

Файл:

```
manifests/nginx-deployment.yaml
```

Назначение:

- запускает nginx;
- использует образ nginx:1.27;
- держит 2 реплики;
- назначает pod'ам label app=nginx-demo.

Применение:

```powershell
kubectl apply -f .\manifests\nginx-deployment.yaml
```

Проверка:

```powershell
kubectl get deploy
kubectl get pods -o wide
```

### Service

Файл:

```
manifests/nginx-service.yaml
```

Назначение:

- создаёт Service типа NodePort;
- выбирает pod'ы по selector app=nginx-demo;
- направляет трафик на порт контейнера 80.

Применение:

```powershell
kubectl apply -f .\manifests\nginx-service.yaml
```

Проверка:

```powershell
kubectl get svc
kubectl describe service nginx-service
```

---

## 7. Приложение №2 — echo

### Deployment

Файл:

```
manifests/echo-deployment.yaml
```

Назначение:

- запускает HTTP-приложение;
- использует образ hashicorp/http-echo:1.0;
- возвращает текст Hello from HW44 second app;
- держит 1 реплику.

Применение:

```powershell
kubectl apply -f .\manifests\echo-deployment.yaml
```

### Service

Файл:

```
manifests/echo-service.yaml
```

Назначение:

- создаёт Service типа NodePort;
- выбирает pod по selector app=echo-demo;
- направляет трафик на порт 5678.

Применение:

```powershell
kubectl apply -f .\manifests\echo-service.yaml
```

---

## 8. Проверка доступа

### Echo

Терминал 1:

```powershell
kubectl port-forward service/echo-service 18081:5678
```

Терминал 2:

```powershell
curl.exe http://127.0.0.1:18081
```

Результат:

```
Hello from HW44 second app
```

### Nginx

Терминал 1:

```powershell
kubectl port-forward service/nginx-service 18080:80
```

Терминал 2:

```powershell
curl.exe http://127.0.0.1:18080
```

---

## 9. Диагностика

```powershell
kubectl get all
kubectl logs deployment/nginx-deployment
kubectl logs deployment/echo-deployment
kubectl describe deployment nginx-deployment
kubectl describe deployment echo-deployment
kubectl get endpointslices
kubectl describe endpointslice
```

---

## 10. Самовосстановление

Удаление pod:

```powershell
kubectl delete pod <pod-name>
```

Результат:

- pod удаляется;
- Kubernetes автоматически создаёт новый.

Вывод:

Kubernetes поддерживает желаемое состояние системы.

---

## 11. Масштабирование

Увеличение количества реплик:

```powershell
kubectl scale deployment nginx-deployment --replicas=3
```

Возврат к исходному состоянию:

```powershell
kubectl scale deployment nginx-deployment --replicas=2
```

Вывод:

Kubernetes позволяет динамически изменять количество экземпляров приложения.

---

## 12. Итог

В ходе работы:

- поднят Kubernetes-кластер;
- развёрнуты два приложения;
- настроены Deployment и Service;
- проверены logs, endpoints, EndpointSlice;
- протестированы self-healing и scaling.

Основные принципы Kubernetes:

- декларативное описание состояния;
- автоматическое поддержание реплик;
- отказоустойчивость;
- масштабируемость;
- централизованное управление через kubectl.