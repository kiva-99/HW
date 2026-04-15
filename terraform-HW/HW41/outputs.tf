# =============================================================================
# Выходные значения root module
# =============================================================================

output "vm_id" {
  description = "ID созданной ВМ"
  value       = module.hw41-vm.vm_id
}

output "vm_internal_ip" {
  description = "Внутренний IP адрес ВМ"
  value       = module.hw41-vm.vm_internal_ip
}

output "vm_public_ip" {
  description = "Публичный IP адрес ВМ"
  value       = module.hw41-vm.vm_public_ip
}

output "vm_fqdn" {
  description = "FQDN ВМ"
  value       = module.hw41-vm.vm_fqdn
}

output "used_network_id" {
  description = "ID сети, в которой развёрнута ВМ"
  value       = local.network_id
}

output "used_subnet_id" {
  description = "ID подсети, в которой развёрнута ВМ"
  value       = local.subnet_id
}