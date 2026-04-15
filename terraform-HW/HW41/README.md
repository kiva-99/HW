# 🚀 HW41 — Terraform: Remote Backend + YDB Locking

## 📌 Описание

В рамках задания реализована инфраструктура с использованием **Terraform**, включающая:

* 📦 Удалённое хранение состояния (Remote State)
* 🔒 Механизм блокировки (State Locking)
* 🧩 Модульную структуру Terraform
* 🔐 IAM и безопасный доступ к backend

---

## 🧱 Архитектура решения

```
terraform HW/
│
├── backend-bootstrap/   # Создание backend-инфраструктуры
│
├── HW41/                # Основной Terraform проект
│   ├── modules/
│   │   └── vm/          # Модуль виртуальной машины
│   │
│   ├── main.tf
│   ├── backend.tf
│   ├── variables.tf
│   └── outputs.tf
│
└── HW40/ (предыдущее ДЗ)
```

---

## ⚙️ Backend Terraform (реализован вручную)

### Используемые сервисы

| AWS аналог | Yandex Cloud       |
| ---------- | ------------------ |
| S3         | Object Storage     |
| DynamoDB   | YDB (Document API) |

---

### 🔐 Компоненты backend

* 📦 **Object Storage** — хранение `terraform.tfstate`
* 🔒 **YDB (Document API)** — блокировка состояния
* 👤 **Service Account** — доступ Terraform к backend
* 🔑 **Access Key / Secret Key** — для S3 API

---

## 📁 Конфигурация backend

```hcl
terraform {
  backend "s3" {
    endpoints = {
      s3 = "https://storage.yandexcloud.net"
    }

    bucket = "kko-hw41-tf-b85be757"
    key    = "hw41/terraform.tfstate"
    region = "ru-central1"

    # 🔥 Аналог DynamoDB locking
    dynamodb_endpoint = "https://docapi.serverless.yandexcloud.net/ru-central1/..."
    dynamodb_table    = "state-lock-table"

    skip_region_validation      = true
    skip_credentials_validation = true
    skip_requesting_account_id  = true
    skip_s3_checksum            = true
  }
}
```

---

## 🧩 Использование модуля

Модуль виртуальной машины:

```
modules/vm
```

Пример использования:

```hcl
module "hw41-vm" {
  source = "./modules/vm"

  vm_name        = var.vm_name
  vm_hostname    = var.vm_hostname
  vm_description = var.vm_description

  zone      = var.yc_zone
  subnet_id = var.subnet_id

  image_family = var.image_family
  image_id     = var.image_id

  cores  = var.cores
  memory = var.memory

  ssh_public_key = var.ssh_public_key
}
```

---

## ⚠️ Важный момент: image_id vs image_family

### Проблема

```hcl
image_family = "ubuntu-2204-lts"
```

➡️ Всегда выбирает последний образ → приводит к пересозданию ВМ

### Решение

```hcl
image_id = "fd8r71tg4mg5b3uiholm"
```

➡️ Фиксация образа → стабильный Terraform plan

---

## 🔄 Проверка работы

### Terraform

```bash
terraform validate
terraform plan
terraform state list
terraform output
```

✔️ Ожидаемый результат:

```
No changes. Your infrastructure matches the configuration.
```

---

### 📦 Проверка state в Object Storage

```bash
yc storage s3api list-objects --bucket kko-hw41-tf-b85be757 --prefix hw41/
```

✔️ Должен быть:

```
hw41/terraform.tfstate
```

---

### 🔒 Проверка блокировки (State Locking)

Запустить в **двух терминалах**:

```bash
terraform plan
```

✔️ Второй процесс:

```
Acquiring state lock...
```

➡️ Значит locking работает

---

### 🖥 Проверка инфраструктуры

```bash
yc compute instance list
yc ydb database list
yc storage bucket list
```

---

### 🔐 Проверка IAM

```bash
yc resource-manager folder list-access-bindings <folder_id>
```

✔️ Должны быть роли:

* `storage.editor`
* `ydb.admin`

---

## 🧠 Сравнение HW40 vs HW41

| HW40              | HW41              |
| ----------------- | ----------------- |
| Локальный state   | Remote backend    |
| Нет блокировок    | YDB locking       |
| Один пользователь | Поддержка команды |
| Простой Terraform | Production-ready  |

---

## ✅ Итог

Реализовано:

* 📦 Remote Terraform state
* 🔒 State locking через YDB
* 🧩 Модульная архитектура
* 🔐 IAM доступ к backend
* ⚙️ Полностью воспроизводимая инфраструктура

---

## 🏁 Вывод

Terraform используется не просто как инструмент, а как:

> 💡 **Система управления инфраструктурой уровня production**

---
## 📸 Скриншоты

- Terraform plan
- Object Storage state
- YDB table
- Locking (2 terminals)