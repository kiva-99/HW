# HW49 — Prometheus Monitoring Stack

## Цель работы

Развернуть стек мониторинга на базе Prometheus и Grafana.
Подключить exporters для сбора системных и контейнерных метрик.
Проверить получение метрик и визуализацию данных.

---

# Используемые компоненты

* Prometheus
* Grafana
* Node Exporter
* cAdvisor
* Docker Compose

---

# Структура проекта

```text
HW49/
│
├── docker-compose.yml
│
├── prometheus/
│   └── prometheus.yml
│
└── screenshots/
```

---

# docker-compose.yml

Используется Docker Compose для запуска сервисов:

* prometheus
* grafana
* cadvisor
* node-exporter

Prometheus и Grafana используют persistent Docker volumes:

* lesson18052026_prometheus_data
* lesson18052026_grafana_data

---

# Конфигурация Prometheus

Файл:

```text
prometheus/prometheus.yml
```

Содержит scrape targets:

```yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'node_exporter'
    static_configs:
      - targets: ['node-exporter:9100']
```

---

# Запуск проекта

## Запуск контейнеров

```powershell
docker compose up -d
```

## Проверка контейнеров

```powershell
docker compose ps
```

## Проверка targets Prometheus

```powershell
Invoke-RestMethod http://localhost:9090/api/v1/targets | ConvertTo-Json -Depth 10
```

---

# Проверка метрик

## Проверка Prometheus metric up

```promql
up
```

Показывает доступность targets.

Значение:

* 1 = target доступен
* 0 = target недоступен

---

## Проверка CPU-метрик Node Exporter

```promql
node_cpu_seconds_total
```

Показывает использование CPU.

---

## Проверка container metrics cAdvisor

```promql
container_memory_usage_bytes
```

Показывает использование памяти контейнерами.

---

# Доступ к сервисам

## Prometheus

```text
http://localhost:9090
```

## Grafana

```text
http://localhost:3000
```

## cAdvisor

```text
http://localhost:8070/containers/
```

## Node Exporter metrics endpoint

```text
http://localhost:9100/metrics
```

---

# Используемые Grafana dashboards

## Node Exporter Full

Dashboard для отображения:

* CPU
* RAM
* SWAP
* filesystem
* network
* load average

---

## cAdvisor exporter

Dashboard для отображения:

* container CPU usage
* container memory usage
* container activity

---

# Persistent Storage

Для сохранения:

* dashboards Grafana
* historical metrics Prometheus

используются Docker volumes:

```text
lesson18052026_prometheus_data
lesson18052026_grafana_data
```

---

# Скриншоты

## 01-running-monitoring-containers.png

Запущенные контейнеры мониторинга.

---

## 02-prometheus-grafana-volumes.png

Подключённые Docker volumes для Prometheus и Grafana.

---

## 03-prometheus-up-metric.png

Проверка metric `up`.

---

## 04-node-exporter-cpu-metrics.png

CPU metrics от Node Exporter.

---

## 05-prometheus-targets.png

Targets Prometheus со статусом UP.

---

## 06-prometheus-query-up.png

PromQL query в Prometheus UI.

---

## 07-grafana-dashboards.png

Список dashboards Grafana.

---

## 07-1-grafana-cadvisor-dashboard.png

Dashboard cAdvisor в Grafana.

---

## 07-2-grafana-node-exporter-dashboard.png

Dashboard Node Exporter Full в Grafana.

---

## 08-cadvisor-ui.png

Web UI cAdvisor.

---

## 09-node-exporter-metrics-endpoint.png

Raw metrics endpoint Node Exporter.

---

# Итог

В результате работы:

* развернут стек мониторинга;
* настроен Prometheus;
* подключены exporters;
* проверен сбор метрик;
* настроена Grafana;
* восстановлены persistent dashboards и historical metrics через Docker volumes.

