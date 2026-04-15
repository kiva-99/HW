# =============================================================================
# Переменные модуля VM
# =============================================================================

variable "vm_name" {
  description = "Имя ВМ"
  type        = string
}

variable "vm_hostname" {
  description = "Hostname ВМ"
  type        = string
}

variable "vm_description" {
  description = "Описание ВМ"
  type        = string
}

variable "zone" {
  description = "Зона доступности"
  type        = string
}

variable "subnet_id" {
  description = "ID подсети для ВМ"
  type        = string
}

variable "image_family" {
  description = "Семейство образов"
  type        = string
}

variable "image_id" {
  description = "Конкретный image_id. Если пусто — используем image_family"
  type        = string
  default     = ""
}

variable "platform_id" {
  description = "Платформа ВМ"
  type        = string
}

variable "cores" {
  description = "Количество vCPU"
  type        = number
}

variable "memory" {
  description = "RAM в ГБ"
  type        = number
}

variable "core_fraction" {
  description = "Гарантированная доля CPU"
  type        = number
}

variable "boot_disk_size" {
  description = "Размер загрузочного диска"
  type        = number
}

variable "boot_disk_type" {
  description = "Тип загрузочного диска"
  type        = string
}

variable "nat" {
  description = "Назначать публичный IP"
  type        = bool
}

variable "preemptible" {
  description = "Прерываемая ВМ"
  type        = bool
}

variable "ssh_public_key" {
  description = "Публичный SSH ключ"
  type        = string
}