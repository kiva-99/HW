# =============================================================================
# Переменные root module
# =============================================================================

# -----------------------------------------------------------------------------
# Аутентификация Yandex Cloud
# -----------------------------------------------------------------------------
variable "yc_token" {
  description = "IAM token для Yandex Cloud"
  type        = string
  sensitive   = true
}

variable "yc_cloud_id" {
  description = "Cloud ID"
  type        = string
}

variable "yc_folder_id" {
  description = "Folder ID"
  type        = string
}

variable "yc_zone" {
  description = "Зона доступности"
  type        = string
  default     = "ru-central1-a"
}

# -----------------------------------------------------------------------------
# Использование существующей сети/подсети
# -----------------------------------------------------------------------------
variable "existing_network_id" {
  description = "ID существующей VPC сети. Если пусто — будет создана новая сеть"
  type        = string
  default     = ""
}

variable "existing_subnet_id" {
  description = "ID существующей подсети. Если пусто — будет создана новая подсеть"
  type        = string
  default     = ""
}

variable "subnet_cidr" {
  description = "CIDR новой подсети, если existing_subnet_id не указан"
  type        = string
  default     = "10.11.0.0/24"
}

# -----------------------------------------------------------------------------
# Параметры ВМ
# -----------------------------------------------------------------------------
variable "vm_name" {
  description = "Имя ВМ"
  type        = string
  default     = "hw41-vm-optimized"
}

variable "vm_hostname" {
  description = "Hostname ВМ"
  type        = string
  default     = "vm"
}

variable "vm_description" {
  description = "Описание ВМ"
  type        = string
  default     = "Создана через Terraform модуль"
}

variable "image_family" {
  description = "Семейство образов"
  type        = string
  default     = "ubuntu-2204-lts"
}

variable "image_id" {
  description = "Конкретный image_id. Если задан, используется он; если пусто — ищем по family"
  type        = string
  default     = ""
}

variable "platform_id" {
  description = "Платформа ВМ"
  type        = string
  default     = "standard-v3"
}

variable "cores" {
  description = "Количество vCPU"
  type        = number
  default     = 2
}

variable "memory" {
  description = "RAM в ГБ"
  type        = number
  default     = 1
}

variable "core_fraction" {
  description = "Гарантированная доля CPU"
  type        = number
  default     = 20
}

variable "boot_disk_size" {
  description = "Размер загрузочного диска"
  type        = number
  default     = 10
}

variable "boot_disk_type" {
  description = "Тип загрузочного диска"
  type        = string
  default     = "network-hdd"
}

variable "nat" {
  description = "Назначать публичный IP"
  type        = bool
  default     = true
}

variable "preemptible" {
  description = "Прерываемая ВМ"
  type        = bool
  default     = true
}

variable "ssh_public_key" {
  description = "Публичный SSH ключ целиком"
  type        = string
}