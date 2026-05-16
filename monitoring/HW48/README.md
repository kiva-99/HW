```
# HW48 — Мониторинг приложения с помощью Zabbix

## Цель работы

Цель домашнего задания — изучить принципы мониторинга инфраструктуры и приложений, развернуть Zabbix, настроить сбор метрик, web monitoring, триггеры, dashboard и проверить реакцию системы мониторинга на отказ приложения.

В качестве практического стенда использован локальный Docker-стенд и приложение дипломного проекта **TypeSpeed Arena**.

---

## Используемые технологии

- Docker
- Docker Compose
- Zabbix 7.0
- Zabbix Agent 2
- MySQL 8.0
- Nginx
- PostgreSQL
- Web monitoring
- Docker container discovery
- Zabbix triggers
- Zabbix dashboards

---

## Структура проекта

```
HW48
├── configs
│   ├── docker-compose.yml
│   ├── nginx-status.conf
│   └── zabbix_agent2.conf
├── screenshots
│   └── ...
├── notes
└── README.md
```

Архитектура стенда

Zabbix был развёрнут в Docker-контейнерах:

MySQL
  ↓
Zabbix Server
  ↓
Zabbix Frontend
  ↓
Zabbix Agent 2
  ↓
Docker / Nginx / PostgreSQL / TypeSpeed Arena

Основные контейнеры:

Контейнер	Назначение
mysql-server	База данных Zabbix
zabbix-server	Центральный сервер мониторинга
zabbix-frontend	Web UI Zabbix
zabbix-agent	Сбор метрик через Zabbix Agent 2
demo-web-nginx	Тестовый nginx
demo-db-postgres	Тестовая PostgreSQL БД
typespeed-frontend	Frontend дипломного приложения
typespeed-backend	Backend дипломного приложения

Запуск Zabbix

Рабочий стенд расположен в отдельной директории:

D:\Docker\zabbix

Запуск выполняется командой:

docker compose up -d

Проверка контейнеров:

docker compose ps

Zabbix UI доступен по адресу:

http://localhost:8083
Docker monitoring

Для мониторинга Docker используется Zabbix Agent 2.

В docker-compose.yml агенту проброшен Docker socket:

volumes:
  - /var/run/docker.sock:/var/run/docker.sock:ro

Это позволяет Zabbix Agent 2 получать информацию о контейнерах, образах, CPU, RAM, сети и статусах контейнеров.

Для ограничения области мониторинга используются Docker labels:

labels:
  - "zabbix.monitor=true"
Nginx monitoring

Для nginx был подготовлен конфиг nginx-status.conf:
```
server {
    listen 80;
    server_name localhost;

    location /basic_status {
        stub_status on;
        allow all;
    }
}
```
stub_status позволяет получать базовые метрики nginx:

active connections;
accepted connections;
handled connections;
requests;
reading;
writing;
waiting.
Интеграция с дипломным проектом

Для мониторинга дипломного приложения TypeSpeed Arena Zabbix Server был подключён к Docker-сети приложения:

docker network connect local_app-network zabbix-zabbix-server-1

После этого Zabbix получил доступ к контейнерам дипломного приложения по внутренним Docker DNS-именам:

http://typespeed-frontend/
http://typespeed-backend:5000/health

Проверка доступности из контейнера Zabbix Server:

docker compose exec zabbix-server sh -c "wget -S -O - http://typespeed-frontend/ 2>&1 | head -20"

docker compose exec zabbix-server sh -c "wget -S -O - http://typespeed-backend:5000/health 2>&1"
Web monitoring

В Zabbix был создан web scenario:

TypeSpeed Arena availability

Сценарий состоит из двух шагов.

Step 1 — Backend health
URL: http://typespeed-backend:5000/health
Required string: healthy
Required status codes: 200
Timeout: 5s
Step 2 — Frontend homepage
URL: http://typespeed-frontend/
Required status codes: 200
Timeout: 15s

Этот сценарий проверяет не только факт запуска контейнеров, но и реальную доступность приложения по HTTP.

Trigger

Для web scenario был создан trigger:

TypeSpeed Arena web scenario failed

Severity:

High

Expression:

last(/Zabbix server/web.test.fail[TypeSpeed Arena availability])>0

Логика:

0 = сценарий работает успешно
1 = сценарий завершился ошибкой

Если backend или frontend становятся недоступны, Zabbix автоматически создаёт проблему.

Проверка отказа

Для проверки работы мониторинга backend был остановлен вручную:

docker stop typespeed-backend

После этого Zabbix обнаружил ошибку web scenario и создал problem:

TypeSpeed Arena web scenario failed

После восстановления контейнера:

docker start typespeed-backend

Zabbix автоматически закрыл проблему.

Dashboard

Создан dashboard:

TypeSpeed Arena Monitoring

На dashboard выведены:

Current problems;
Web scenario status;
Backend response time;
Frontend download speed;
Backend CPU usage;
Frontend CPU usage;
Backend RAM;
Frontend RAM;
Docker containers overview.

Dashboard позволяет быстро увидеть:

доступно ли приложение;
есть ли активные проблемы;
как отвечает backend;
как ведут себя контейнеры;
сколько CPU/RAM используют frontend и backend.



Итог

В ходе работы был развёрнут полноценный monitoring stack на базе Zabbix.

Реализовано:

развёртывание Zabbix в Docker;
подключение Zabbix Agent 2;
мониторинг Docker-контейнеров;
мониторинг nginx;
web monitoring дипломного приложения;
healthcheck backend API;
trigger на отказ приложения;
проверка incident detection;
автоматическое восстановление problem после recovery;
dashboard для визуализации состояния приложения.

Полученный стенд можно использовать как основу мониторинга для дипломного проекта.