```markdown
# HW37: Load Balancer + Auto Scaling (Yandex Cloud)

## 📋 Описание
Реализация балансировки нагрузки с автоскейлингом в Yandex Cloud.  
Аналог AWS ELB + Auto Scaling + Route 53 для учебного проекта.

## 🏗 Архитектура

```
                    ┌─────────────────────────────────────┐
                    │         Yandex Cloud ALB            │
                    │  IP: 158.160.239.87                 │
                    │  hw37-load-balancer                 │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┴──────────────────────┐
                    │         HTTP Router                 │
                    │  hw37-http-router                   │
                    │  Authority: typespeedarena.ru       │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┴──────────────────────┐
                    │        Backend Group                │
                    │  hw37-backend-group                 │
                    │  Health Check: HTTP /, port 80      │
                    └──────────────┬──────────────────────┘
                                   │
        ┌──────────────────────────┴──────────────────────────┐
        │                  Target Group                       │
        │  hw37-target-group                                  │
        └──────────────────────┬──────────────────────────────┘
                               │
        ┌──────────────────────┴──────────────────────┐
        │                                             │
┌───────▼────────┐                          ┌────────▼────────┐
│   hw-35-vm     │                          │  Instance Group │
│  10.128.0.18   │                          │  10.128.0.11    │
│  Nginx:80      │                          │  Nginx:80       │
└────────────────                          └─────────────────┘
```

## 📊 Созданные ресурсы

| Ресурс | Имя | ID | Статус |
|--------|-----|-----|--------|
| **Load Balancer** | `hw37-load-balancer` | `ds7td3na9phfosb7tl0a` | ACTIVE |
| **HTTP Router** | `hw37-http-router` | `ds7kv2qbvsglrnj0cjbd` | Created |
| **Backend Group** | `hw37-backend-group` | `ds7kskia9953ghc5646e` | Created |
| **Target Group** | `hw37-target-group` | `ds73dvq9jjukqhj3rb4t` | Created |
| **Instance Group** | `hw35-autoscale-group` | `cl1hkibntfggv5qcemfc` | ACTIVE |
| **DNS Zone** | `typespeedarena-ru` | `dns694tvq2cnev68fl0q` | PUBLIC |
| **Domain** | `typespeedarena.ru` | - | Delegated |

## 🌐 Домен и DNS

- **Домен**: `typespeedarena.ru` (куплен на reg.ru)
- **DNS-зона**: Yandex Cloud DNS
- **NS-серверы**: `ns1.yandexcloud.net`, `ns2.yandexcloud.net`
- **A-запись**: `@` → `158.160.239.87` (IP балансировщика)

## 🛠 Команды для развёртывания

### 1. Создание Target Group
```bash
yc application-load-balancer target-group create hw37-target-group \
  --description "Target group for HW37 Load Balancer" \
  --target subnet-id=e9b1etf7pjdo6dlm96o4,ip-address=10.128.0.18 \
  --target subnet-id=e9b1etf7pjdo6dlm96o4,ip-address=10.128.0.11
```

### 2. Создание Backend Group
```bash
yc alb backend-group create hw37-backend-group \
  --named-health-check http-health-check \
  --http-health-check port=80,path=/,timeout=3s,interval=1s,healthy-threshold=2,unhealthy-threshold=3 \
  --target-group hw37-target-group
```

### 3. Создание HTTP Router
```bash
yc alb http-router create hw37-http-router \
  --virtual-host name=vh1,hostname=typespeedarena.ru,route-name=main-route,route-path-prefix=/,backend-group-name=hw37-backend-group
```

### 4. Создание Load Balancer
```bash
yc alb load-balancer create hw37-load-balancer \
  --description "Load Balancer for HW37" \
  --region-id ru-central1 \
  --network-id enpnkes38osg7vp076d5 \
  --listener name=listener1,port=80,protocol=http,http-handler \
  --target-group hw37-target-group \
  --health-check name=http-check,interval=10s,timeout=5s,unhealthy-threshold=3,healthy-threshold=2,http-options port=80,path=/
```

### 5. Обновление DNS
```bash
yc dns zone add-records typespeedarena-ru \
  --name "@" \
  --ttl 300 \
  --ipv4 158.160.239.87
```

## 🧪 Тестирование

### Проверка балансировки
```bash
# 5 запросов для проверки чередования ВМ
for i in {1..5}; do
  curl -s -H "Host: typespeedarena.ru" http://158.160.239.87 | grep "Server:"
done
```

### Проверка по домену
```bash
curl http://typespeedarena.ru
```

### Проверка статуса целей
```bash
yc application-load-balancer target-group get hw37-target-group
```

## 🔒 Security Group

| Правило | Порт | Протокол | Источник | Назначение |
|---------|------|----------|----------|------------|
| HTTP | 80 | TCP | 0.0.0.0/0 | Веб-трафик |
| HTTPS | 443 | TCP | 0.0.0.0/0 | HTTPS трафик |
| SSH | 22 | TCP | 0.0.0.0/0 | Доступ по SSH |
| Health Check | 30080 | TCP | Проверки состояния балансировщика | ALB health checks |
| ICMP | - | ICMP | 0.0.0.0/0 | Ping |

## 💰 Стоимость (ежемесячно)

| Ресурс | Стоимость | Примечание |
|--------|-----------|------------|
| Application Load Balancer | ~2000 ₽ | Удалить после сдачи |
| Instance Group (2 ВМ) | ~900 ₽ | Остановить после сдачи |
| Cloud DNS | ~50 ₽ | Можно оставить для диплома |
| Домен | ~200 ₽/год | Уже оплачен |
| **Итого** | **~3150 ₽/мес** | В рамках гранта 4000 ₽ |

## 🧹 Очистка ресурсов (после сдачи)

```bash
# 1. Удалить Load Balancer
yc alb load-balancer delete hw37-load-balancer

# 2. Удалить HTTP Router
yc alb http-router delete hw37-http-router

# 3. Удалить Backend Group
yc alb backend-group delete hw37-backend-group

# 4. Удалить Target Group
yc application-load-balancer target-group delete hw37-target-group

# 5. Остановить Instance Group (не удалять!)
yc compute instance-group stop hw35-autoscale-group

# 6. DNS-зону можно оставить для диплома
```

## ⚠️ Известные проблемы

1. **Балансировщик возвращает `request-id`** (502 ошибка)
   - Причина: Health checks могут не проходить из-за Security Group
   - Решение: Проверить правило порта 30080 с источником "Проверки состояния балансировщика"

2. **ВМ из Instance Group пересоздаются с новыми IP**
   - Причина: Обновление шаблона группы
   - Решение: Обновлять Target Group при изменении IP

## 📸 Скриншоты для отчёта

- [x] Страница "Балансировщики" (статус ACTIVE)
- [x] Страница "Целевые группы" (2 цели)
- [x] Страница "Группы бэкендов" (health check настройки)
- [x] Страница "HTTP-роутеры" (маршрут /)
- [x] Страница "Cloud DNS" (A-запись)
- [x] Ответ `curl` с чередующимися hostname