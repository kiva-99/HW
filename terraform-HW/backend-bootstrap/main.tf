# =============================================================================
# BACKEND BOOTSTRAP: Инфраструктура для удалённого хранения tfstate
# -----------------------------------------------------------------------------
# Назначение bootstrap-проекта:
# 1. Создать бакет Object Storage для хранения terraform.tfstate
# 2. Создать сервисный аккаунт для доступа Terraform backend к Object Storage
# 3. Создать статические S3-ключи (access key / secret key)
# 4. Создать Serverless YDB для механизма блокировок state
#
# ВАЖНО:
# - Этот bootstrap-проект хранит свой state ЛОКАЛЬНО
# - Основной проект HW41 будет использовать УДАЛЁННЫЙ backend
# - Таблицу блокировок Document API создаём отдельно через UI Yandex Cloud
# =============================================================================

terraform {
  required_version = ">= 1.0"

  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.196.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }

  # ---------------------------------------------------------------------------
  # Bootstrap хранит state локально, потому что он сам создаёт backend.
  # Иначе получится циклическая зависимость: backend ещё не создан, а
  # Terraform уже пытается туда писать state.
  # ---------------------------------------------------------------------------
  backend "local" {
    path = "bootstrap.tfstate"
  }
}

# =============================================================================
# PROVIDER
# =============================================================================
provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
}

# =============================================================================
# ПЕРЕМЕННЫЕ
# =============================================================================
variable "yc_token" {
  description = "IAM токен для аутентификации"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  description = "ID облака"
  type        = string
  default     = "b1g7n8p29nt9r3i5e3m5"
}

variable "yc_folder_id" {
  description = "ID каталога"
  type        = string
  default     = "b1ga0ad79qngmcfham7u"
}

# =============================================================================
# 1. СЛУЧАЙНЫЙ СУФФИКС ДЛЯ УНИКАЛЬНОГО ИМЕНИ БАКЕТА
# -----------------------------------------------------------------------------
# Имя бакета должно быть глобально уникальным, поэтому добавляем случайный
# hex-суффикс.
# =============================================================================
resource "random_id" "bucket_suffix" {
  byte_length = 4
}

# =============================================================================
# 2. СЕРВИСНЫЙ АККАУНТ ДЛЯ ДОСТУПА К BACKEND
# -----------------------------------------------------------------------------
# Этот сервисный аккаунт будет использоваться Terraform backend'ом для:
# - чтения и записи state в Object Storage
# - доступа к YDB для state locking
#
# ВНИМАНИЕ:
# description оставляем прежним, чтобы Terraform не пытался лишний раз
# менять ресурс и не тянул за собой побочные изменения.
# =============================================================================
resource "yandex_iam_service_account" "backend_sa" {
  name        = "hw41-backend-sa"
  description = "SA для хранения tfstate в Object Storage"
}

# -----------------------------------------------------------------------------
# Роль для работы с бакетом Object Storage
# -----------------------------------------------------------------------------
resource "yandex_resourcemanager_folder_iam_member" "backend_sa_storage_editor" {
  folder_id = var.yc_folder_id
  member    = "serviceAccount:${yandex_iam_service_account.backend_sa.id}"
  role      = "storage.editor"
}

# -----------------------------------------------------------------------------
# Роль для работы с YDB
# Для строгого варианта HW41 оставляем именно ydb.admin.
# ydb.editor здесь быть НЕ должно.
# -----------------------------------------------------------------------------
resource "yandex_resourcemanager_folder_iam_member" "backend_sa_ydb_admin" {
  folder_id = var.yc_folder_id
  member    = "serviceAccount:${yandex_iam_service_account.backend_sa.id}"
  role      = "ydb.admin"
}

# =============================================================================
# 3. СТАТИЧЕСКИЕ КЛЮЧИ ДЛЯ S3 API
# -----------------------------------------------------------------------------
# Terraform backend "s3" не использует IAM token.
# Ему нужны Access Key / Secret Key, совместимые с S3 API.
#
# ВНИМАНИЕ:
# description оставляем прежним, чтобы не вызвать replacement ключей.
# =============================================================================
resource "yandex_iam_service_account_static_access_key" "backend_keys" {
  service_account_id = yandex_iam_service_account.backend_sa.id
  description        = "Static keys for Terraform S3 backend"
}

# =============================================================================
# 4. OBJECT STORAGE BUCKET ДЛЯ ХРАНЕНИЯ TFSTATE
# -----------------------------------------------------------------------------
# Здесь будет храниться terraform.tfstate основного проекта HW41.
# Версионирование включено обязательно — это best practice для state.
# =============================================================================
resource "yandex_storage_bucket" "tf_state" {
  bucket    = "kko-hw41-tf-${random_id.bucket_suffix.hex}"
  folder_id = var.yc_folder_id

  versioning {
    enabled = true
  }

  # Защита от случайного удаления содержимого бакета вместе со state
  force_destroy = false
}

# =============================================================================
# 5. SERVERLESS YDB ДЛЯ STATE LOCKING
# -----------------------------------------------------------------------------
# Это база, внутри которой отдельно создаётся Document API table:
#   state-lock-table
#
# Именно она будет использоваться Terraform backend'ом как аналог
# DynamoDB table для блокировок state.
# =============================================================================
resource "yandex_ydb_database_serverless" "state_lock_db" {
  name      = "hw41-state-lock-db"
  folder_id = var.yc_folder_id

  # Логическая зависимость:
  # сначала бакет, потом база под блокировки
  depends_on = [yandex_storage_bucket.tf_state]
}

# =============================================================================
# 6. ТАБЛИЦА БЛОКИРОВОК
# -----------------------------------------------------------------------------
# НЕ создаём через resource "yandex_ydb_table", потому что для Terraform
# backend нужен именно DynamoDB-compatible / Document API table.
#
# Поэтому таблицу создаём отдельно через UI Yandex Cloud:
#   - имя таблицы: state-lock-table
#   - тип: Document table
#   - колонка: LockID
#   - тип колонки: String
#   - LockID = partition key
# =============================================================================

# =============================================================================
# OUTPUTS
# -----------------------------------------------------------------------------
# Эти значения понадобятся в основном проекте HW41 при настройке backend.tf
# =============================================================================
output "bucket_name" {
  description = "Имя бакета для использования в HW41/backend.tf"
  value       = yandex_storage_bucket.tf_state.bucket
}

output "ydb_endpoint" {
  description = "Document API endpoint YDB для использования в backend.tf"
  value       = yandex_ydb_database_serverless.state_lock_db.document_api_endpoint
}

output "access_key" {
  description = "Access key для передачи в -backend-config"
  value       = yandex_iam_service_account_static_access_key.backend_keys.access_key
  sensitive   = true
}

output "secret_key" {
  description = "Secret key для передачи в -backend-config"
  value       = yandex_iam_service_account_static_access_key.backend_keys.secret_key
  sensitive   = true
}

output "sa_id" {
  description = "ID сервисного аккаунта (для аудита)"
  value       = yandex_iam_service_account.backend_sa.id
}