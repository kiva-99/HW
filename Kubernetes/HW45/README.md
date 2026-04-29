# HW45: Kubernetes #2 (Namespaces, Pods, Controllers)

## 👤 Студент
Кирилл


```
🎯 Цель задания

Изучить:
- Namespaces (создание, управление, применение)
- Pods (создание и управление)
- Controllers (ReplicaSet, Deployment, StatefulSet)
- Масштабирование и управление состоянием кластера
```


# 🏗 Общая архитектура

```
Kubernetes Cluster (minikube)

hw45-dev
├── Pod (nginx)
└── Service (NodePort)

hw45-test
└── ReplicaSet
└── 2 Pod (http-echo)

hw45-prod
└── Deployment
└── ReplicaSet
└── Pod (nginx)
```

###  1. Namespaces

📌 Основные команды

Создание
```bash
kubectl create namespace hw45-dev

или через YAML:

kubectl apply -f namespace.yaml
Просмотр
kubectl get namespaces
kubectl get ns
kubectl get namespaces --show-labels
Удаление
kubectl delete namespace hw45-dev
Работа внутри namespace
kubectl get pods -n hw45-dev

```
📌 Практическое применение Namespaces
```
Namespaces используются для:

разделения окружений (dev / test / prod)
изоляции ресурсов разных проектов
разграничения доступа (RBAC)
управления квотами ресурсов
предотвращения конфликтов имён ресурсов

```
### 2. Pods

```
📌 Способы создания Pod

Через YAML (использовано в работе)
kubectl apply -f pod.yaml
Через CLI
kubectl run nginx-pod \
  --image=nginx:1.27 \
  --restart=Never \
  -n hw45-dev


📌 Управление Pod

Просмотр
kubectl get pods -n hw45-dev
kubectl get pods -o wide
Детальная информация
kubectl describe pod hw45-nginx-pod -n hw45-dev
Логи
kubectl logs hw45-nginx-pod -n hw45-dev
Удаление
kubectl delete pod hw45-nginx-pod -n hw45-dev
Подключение внутрь контейнера
kubectl exec -it hw45-nginx-pod -n hw45-dev -- bash


⚠️ Важный вывод

Pod — это базовая единица Kubernetes,
но в реальной работе почти не используется напрямую.

Обычно используются контроллеры.
```
### 3. Controllers
```
 📌 Роль Controllers

Controllers обеспечивают соответствие текущего состояния желаемому:

если pod меньше нужного количества → создаётся новый
если pod упал → создаётся новый

 📌 Типы Controllers
🔹 ReplicaSet

Назначение:

поддерживает заданное количество Pod

Пример:

replicas: 2

Проверка:

kubectl get replicaset -n hw45-test
kubectl get pods -n hw45-test

Проверка self-healing:

kubectl delete pod <pod-name> -n hw45-test

Результат:

Pod автоматически пересоздаётся
🔹 Deployment

Назначение:

управляет ReplicaSet
обновляет приложение
масштабирует
обеспечивает rollback

Проверка:

kubectl get deployment -n hw45-prod
kubectl get pods -n hw45-prod
🔹 StatefulSet

Используется для stateful-приложений:

базы данных (PostgreSQL, MongoDB)
брокеры сообщений (Kafka)
приложения с постоянным состоянием

Особенности:

стабильные имена Pod
постоянные volume
строгий порядок запуска/остановки
📌 Управление Controllers
Мониторинг
kubectl get deployment -n hw45-prod
kubectl get replicaset -n hw45-test
kubectl get pods -n hw45-prod
Масштабирование
kubectl scale deployment hw45-nginx-deployment \
  --replicas=5 -n hw45-prod

Уменьшение:

kubectl scale deployment hw45-nginx-deployment \
  --replicas=2 -n hw45-prod
Обновление приложения
kubectl set image deployment/hw45-nginx-deployment \
  nginx=nginx:1.28 \
  -n hw45-prod
Rollout и откат
kubectl rollout history deployment hw45-nginx-deployment -n hw45-prod
kubectl rollout undo deployment hw45-nginx-deployment -n hw45-prod

```
### 📦 Service (дополнительно)
```
Использован Service типа NodePort:

type: NodePort

Проверка:

kubectl get service -n hw45-dev

Доступ:

minikube service hw45-nginx-pod-service -n hw45-dev --url
```
### 📁 Структура проекта
```
HW45/
├── manifests/
│   ├── 01-namespace-dev.yaml
│   ├── 02-namespace-test.yaml
│   ├── 03-namespace-prod.yaml
│   ├── 04-pod-nginx-dev.yaml
│   ├── 05-service-nginx-pod-dev.yaml
│   ├── 06-replicaset-echo-test.yaml
│   └── 07-deployment-nginx-prod.yaml
├── screenshots/
└── README.md

```
### 📸 Скриншоты (обязательно)
```

🧠 Основные выводы
Kubernetes управляет не контейнерами напрямую, а через объекты
Pod — минимальная единица
ReplicaSet обеспечивает отказоустойчивость
Deployment управляет обновлениями и масштабированием
Namespace используется для изоляции
Kubernetes работает по принципу desired state
🚀 Итог

HW45 выполнено полностью:

реализованы namespace
создан Pod и Service
реализован ReplicaSet и self-healing
реализован Deployment
выполнено масштабирование
изучены основные команды и принципы Kubernetes