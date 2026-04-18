# HW43 — Развёртывание веб-сервера в Terraform (Yandex Cloud)

## Цель задания

Практически развернуть веб-сервер с помощью Terraform:

* описать инфраструктуру в коде
* применить конфигурацию
* проверить доступность веб-страницы
* удалить созданные ресурсы

---

## Используемая инфраструктура

Проект развёрнут в Yandex Cloud:

* Cloud ID: `b1g7n8p29nt9r3i5e3m5`
* Folder ID: `b1gcijdrjlf3m935prl2`
* Zone: `ru-central1-a`

---

## Создаваемые ресурсы

Terraform создаёт:

* `yandex_vpc_security_group.main` — security group для SSH и HTTP
* `yandex_compute_instance.main` — виртуальная машина с веб-сервером

Terraform использует существующие ресурсы как `data`:

* existing VPC network: `default`
* existing subnet: `default-ru-central1-a`

---

## Структура проекта

```text
HW43/
├── .gitignore
├── README.md
├── versions.tf
├── provider.tf
├── variables.tf
├── terraform.tfvars
├── main.tf
├── outputs.tf
├── key.json
└── files/
    └── cloud-init.yaml
```

---

## Файлы проекта

### `versions.tf`

Определяет версию Terraform и провайдера Yandex Cloud.

### `provider.tf`

Настраивает подключение к Yandex Cloud через service account key.

### `variables.tf`

Содержит входные переменные:

* cloud_id
* folder_id
* zone
* ssh_public_key
* имена ресурсов

### `terraform.tfvars`

Содержит конкретные значения переменных.

### `main.tf`

Описывает:

* existing network/subnet как `data`
* security group
* виртуальную машину
* metadata с `ssh-keys` и `user-data`

### `outputs.tf`

Выводит:

* `vm_id`
* `vm_internal_ip`
* `vm_public_ip`
* `network_id`
* `subnet_id`

### `files/cloud-init.yaml`

Сценарий cloud-init:

* обновляет пакеты
* устанавливает nginx
* создаёт страницу `index.html`
* запускает nginx

---

## Основная конфигурация

### Security Group

Открыты:

* SSH `22/tcp`
* HTTP `80/tcp`

### Virtual Machine

Параметры:

* platform: `standard-v3`
* 2 vCPU
* 1 GB RAM
* core_fraction: `20`
* preemptible: `true`
* boot disk: `10 GB network-ssd`

---

## Команды выполнения

### Инициализация

```bash
terraform init
```

### Проверка конфигурации

```bash
terraform validate
terraform plan
```

### Применение

```bash
terraform apply
```

### Проверка результата

```bash
terraform output vm_public_ip
curl http://<PUBLIC_IP>
```

### Удаление ресурсов

```bash
terraform destroy
```

---

## Результат

После выполнения `terraform apply` была создана VM с установленным nginx.

Публичный IP:
`89.169.137.48`

Проверка через браузер и `curl` показала успешную работу веб-сервера:

```html
<html>
  <head><title>HW43</title></head>
  <body>
    <h1>HW43 web server is running</h1>
    <p>This VM was created by Terraform in Yandex Cloud.</p>
  </body>
</html>
```

---

## Особенность выполнения

Изначально использовался `cloud-init`, содержащий heredoc с HTML, из-за чего YAML оказался невалидным и nginx не установился. Проблема была исправлена переводом создания `index.html` в `write_files`, после чего VM была пересоздана через Terraform и веб-сервер успешно поднялся.

---

## Вывод

В рамках HW43 были отработаны:

* создание инфраструктуры через Terraform
* работа с существующей сетью через `data`
* создание security group
* развёртывание VM
* автоматическая установка nginx через `cloud-init`
* проверка результата через браузер и `curl`
* подготовка инфраструктуры к удалению через `terraform destroy`
