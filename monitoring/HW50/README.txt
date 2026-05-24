HW50 — Prometheus + Grafana + Alertmanager Monitoring Stack

Описание
========

В рамках HW50 был реализован полноценный monitoring stack
для дипломного проекта TypeSpeed Arena.

Мониторинг был развёрнут в Yandex Cloud на отдельной monitoring VM.

Использованные технологии
=========================

- Prometheus
- Grafana
- Alertmanager
- Blackbox Exporter
- Node Exporter
- Docker Compose
- Ansible
- Terraform
- Yandex Cloud

Архитектура
===========

Internet
    |
    +----------------------+
    |                      |
    v                      v
App VM                Monitoring VM
(Frontend/API)        (Prometheus/Grafana)

    |
    v

DB VM
(PostgreSQL)

Monitoring stack
================

На monitoring node были развёрнуты:

- Prometheus
- Grafana
- Alertmanager
- Blackbox Exporter
- Node Exporter

Monitoring targets
==================

Мониторятся:

Infrastructure:
- App VM CPU
- App VM RAM
- App VM Disk
- DB VM CPU
- DB VM RAM
- DB VM Disk
- Monitoring VM resources

HTTP endpoints:
- /
- /health
- /api/texts
- /api/leaderboard

Grafana dashboard
=================

Был реализован dashboard:

TypeSpeed Infrastructure

Dashboard отображает:
- CPU usage
- Memory usage
- Disk usage
- HTTP availability
- HTTP response time
- Prometheus targets state

Infrastructure as Code
======================

Monitoring stack описан как код:

Terraform:
- создание monitoring VM
- security groups
- cloud infrastructure

Ansible:
- provisioning monitoring stack
- deployment docker compose
- provisioning Grafana dashboards
- provisioning Prometheus configs

Docker Compose:
- запуск monitoring services

Проверка работоспособности
==========================

Проверены:

- docker compose ps
- Prometheus targets
- Grafana dashboard
- Prometheus API query
- Node Exporter metrics
- HTTP availability probes

Скриншоты
==========

01-wsl-environment.png
02-ansible-monitoring-syntax-check.png
03-monitoring-containers-running.png
04-prometheus-query-up.png
05-grafana-typespeed-dashboard.png
06-alertmanager-ui.png

Результат
=========

Был реализован полноценный cloud monitoring stack
для дипломного проекта TypeSpeed Arena.

Monitoring система поддерживает:
- infrastructure monitoring
- application monitoring
- metrics collection
- dashboard visualization
- дальнейшее внедрение alerting и notifications
