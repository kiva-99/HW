output "existing_network_id" {
  description = "Existing network ID"
  value       = data.yandex_vpc_network.existing.id
}

output "existing_subnet_id" {
  description = "Existing subnet ID"
  value       = data.yandex_vpc_subnet.existing.id
}