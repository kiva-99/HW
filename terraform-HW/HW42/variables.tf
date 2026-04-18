#variable "yc_token" {
#  description = "IAM token for Yandex Cloud"
#  type        = string
#  sensitive   = true
#}

variable "yc_cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "yc_folder_id" {
  description = "Yandex Cloud folder ID"
  type        = string
}

variable "yc_zone" {
  description = "Default availability zone"
  type        = string
  default     = "ru-central1-a"
}

variable "existing_network_name" {
  description = "Name of existing VPC network"
  type        = string
  default     = "default"
}

variable "existing_subnet_name" {
  description = "Name of existing subnet"
  type        = string
  default     = "default-ru-central1-a"
}

variable "existing_security_group_name" {
  description = "Name of existing security group"
  type        = string
  default     = "default-sg-enpnkes38osg7vp076d5"
}

variable "existing_vm_name" {
  description = "Name of existing VM to import"
  type        = string
  default     = "hw-35-vm"
}

variable "yc_sa_key_file" {
  description = "Path to service account key file"
  type        = string
}

variable "existing_vm_service_account_id" {
  description = "Service account attached to existing VM"
  type        = string
  default     = "aje5qjelspl42t0bt197"
}