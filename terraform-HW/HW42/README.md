# HW42 — Import существующей инфраструктуры в Terraform (Yandex Cloud)

## 📌 Цель задания

Научиться:

* анализировать существующую инфраструктуру в облаке;
* описывать её в Terraform;
* импортировать ресурсы в Terraform state;
* выравнивать конфигурацию до состояния `No changes`.

---

## 🏗 Используемая инфраструктура

В работе использовалась уже существующая инфраструктура в Yandex Cloud:

* Cloud: `b1g7n8p29nt9r3i5e3m5`
* Folder: `b1gcijdrjlf3m935prl2`

Ресурсы:

* VM: `hw-35-vm`
* Network: `default`
* Subnet: `default-ru-central1-a`
* Security Group: `default-sg-enpnkes38osg7vp076d5`

---

## 🔐 Аутентификация

Создан отдельный Service Account для HW42:

```bash
yc iam service-account create --name hw42-sa
```

Назначены права:

```bash
yc resource-manager folder add-access-binding b1gcijdrjlf3m935prl2 \
  --role editor \
  --subject serviceAccount:<SA_ID>
```

Создан ключ:

```bash
yc iam key create \
  --service-account-id <SA_ID> \
  --output key.json
```

Используется в Terraform:

```hcl
provider "yandex" {
  service_account_key_file = var.yc_sa_key_file
}
```

---

## 📂 Структура проекта

```text
HW42/
├── main.tf
├── variables.tf
├── provider.tf
├── versions.tf
├── outputs.tf
├── terraform.tfvars
├── .gitignore
├── key.json
├── files/
│   └── cloud-init.yaml
└── modules/
    └── vm/
```

---

## ⚙️ Логика Terraform

### Используются как data (не управляются):

* VPC network
* subnet

```hcl
data "yandex_vpc_network" "existing" {}
data "yandex_vpc_subnet" "existing" {}
```

---

### Управляются Terraform (через import):

* VM
* Security Group

---

## 📥 Импорт ресурсов

### Security Group

```bash
terraform import yandex_vpc_security_group.main enphjtt8rsthpkhent15
```

---

### VM

```bash
terraform import yandex_compute_instance.main fhmfuakdsbraqv7es0e8
```

---

## ⚖️ Выравнивание конфигурации

После импорта Terraform показал расхождения:

* тип диска
* ресурсы VM
* metadata
* network settings

Конфигурация была приведена к реальному состоянию.

---

## ⚠️ Особенность metadata

Оставался diff по:

```hcl
metadata["user-data"]
```

Причина:

* различие форматирования строки (CRLF/LF)

Решение:

```hcl
lifecycle {
  ignore_changes = [
    metadata["user-data"]
  ]
}
```

---

## ✅ Финальный результат

```bash
terraform plan
```

```text
No changes. Your infrastructure matches the configuration.
```

---

## 🧠 Выводы

В рамках задания освоены:

* работа с существующей инфраструктурой
* импорт ресурсов в Terraform
* анализ `terraform plan`
* устранение diff
* работа с IAM (Service Account)
* использование lifecycle.ignore_changes

---

