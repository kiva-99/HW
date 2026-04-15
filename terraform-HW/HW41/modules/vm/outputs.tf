# =============================================================================
# Выходные значения модуля VM
# =============================================================================

output "vm_id" {
  description = "ID ВМ"
  value       = yandex_compute_instance.this.id
}

output "vm_internal_ip" {
  description = "Внутренний IP"
  value       = yandex_compute_instance.this.network_interface[0].ip_address
}

output "vm_public_ip" {
  description = "Публичный IP"
  value       = try(yandex_compute_instance.this.network_interface[0].nat_ip_address, null)
}

output "vm_fqdn" {
  description = "FQDN ВМ"
  value       = yandex_compute_instance.this.fqdn
}