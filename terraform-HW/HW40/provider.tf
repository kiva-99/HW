terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = ">= 0.120.0" # ✅ явно укажите версию для стабильности
    }
  }
  required_version = ">= 1.0"
}

provider "yandex" {
  cloud_id                 = var.cloud_id
  folder_id                = var.folder_id
  service_account_key_file = var.sa_key_file # ✅ путь к key.json
  zone                     = "ru-central1-a"
}