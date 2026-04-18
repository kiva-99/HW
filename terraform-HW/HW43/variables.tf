variable "yc_sa_key_file" {
  description = "Path to service account key file"
  type        = string
}

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

variable "network_name" {
  description = "Name of VPC network"
  type        = string
  default     = "hw43-network"
}

variable "subnet_name" {
  description = "Name of subnet"
  type        = string
  default     = "hw43-subnet-a"
}

variable "security_group_name" {
  description = "Name of security group"
  type        = string
  default     = "hw43-sg"
}

variable "vm_name" {
  description = "Name of virtual machine"
  type        = string
  default     = "hw43-web-vm"
}

variable "vm_hostname" {
  description = "Hostname of virtual machine"
  type        = string
  default     = "hw43-web-vm"
}

variable "ssh_public_key" {
  description = "Public SSH key for VM access"
  type        = string
}