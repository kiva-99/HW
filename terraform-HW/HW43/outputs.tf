output "vm_id" {
  description = "ID of the virtual machine"
  value       = yandex_compute_instance.main.id
}

output "vm_name" {
  description = "Name of the virtual machine"
  value       = yandex_compute_instance.main.name
}

output "vm_internal_ip" {
  description = "Internal IP address of the virtual machine"
  value       = yandex_compute_instance.main.network_interface[0].ip_address
}

output "vm_public_ip" {
  description = "Public IP address of the virtual machine"
  value       = yandex_compute_instance.main.network_interface[0].nat_ip_address
}

output "network_id" {
  description = "ID of the existing VPC network"
  value       = data.yandex_vpc_network.existing.id
}

output "subnet_id" {
  description = "ID of the existing subnet"
  value       = data.yandex_vpc_subnet.existing.id
}