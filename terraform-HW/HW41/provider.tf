# =============================================================================
# HW-41: Продвинутые практики Terraform
# =============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.196.0"
    }
  }


  # Бэкенд будет настроен в backend.tf после создания бакета и таблицы
}

# -----------------------------------------------------------------------------
# Конфигурация провайдера (базовая)
# -----------------------------------------------------------------------------
provider "yandex" {
  # Аутентификация через переменные (значения в terraform.tfvars)
#  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = var.yc_zone
  service_account_key_file = var.sa_key_file # ✅ путь к key.json
}