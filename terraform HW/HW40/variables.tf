variable "cloud_id" {
  description = "Идентификатор облака Yandex Cloud"
  type        = string
}

variable "folder_id" {
  description = "Идентификатор каталога для развертывания"
  type        = string
}

variable "access_key" {
  description = "Access key сервисного аккаунта"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Secret key сервисного аккаунта"
  type        = string
  sensitive   = true
}

variable "zone" {
  description = "Зона доступности по умолчанию"
  type        = string
  default     = "ru-central1-a"
}

variable "sa_key_file" {
  description = "Путь к файлу ключа сервисного аккаунта"
  type        = string
}