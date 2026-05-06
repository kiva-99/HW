variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
}

variable "folder_id" {
  description = "Yandex Cloud folder ID where HW46 resources will be created"
  type        = string
}

variable "sa_key_file" {
  description = "Path to Yandex Cloud service account key JSON file"
  type        = string
  sensitive   = true
}

variable "cloud_zone" {
  description = "Yandex Cloud availability zone"
  type        = string
  default     = "ru-central1-a"
}

variable "trusted_ip_cidr" {
  description = "Your public IP in CIDR format"
  type        = string
}

variable "existing_network_id" {
  description = "Existing VPC network ID"
  type        = string
}

variable "existing_subnet_id" {
  description = "Existing VPC subnet ID"
  type        = string
}

variable "cluster_name" {
  description = "Managed Kubernetes cluster name"
  type        = string
  default     = "hw46-k8s-cluster"
}

variable "k8s_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.29"
}

variable "node_group_name" {
  description = "Managed Kubernetes node group name"
  type        = string
  default     = "hw46-k8s-node-group"
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 1
}

variable "node_cores" {
  description = "CPU cores per node"
  type        = number
  default     = 2
}

variable "node_memory" {
  description = "Memory GB per node"
  type        = number
  default     = 2
}

variable "node_disk_size" {
  description = "Boot disk size GB per node"
  type        = number
  default     = 24
}
