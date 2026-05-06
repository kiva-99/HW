output "cluster_id" {
  description = "Managed Kubernetes cluster ID"
  value       = yandex_kubernetes_cluster.hw46_cluster.id
}

output "cluster_name" {
  description = "Managed Kubernetes cluster name"
  value       = yandex_kubernetes_cluster.hw46_cluster.name
}

output "node_group_id" {
  description = "Managed Kubernetes node group ID"
  value       = yandex_kubernetes_node_group.hw46_node_group.id
}

output "network_id" {
  description = "Existing VPC network ID used by cluster"
  value       = data.yandex_vpc_network.existing.id
}

output "subnet_id" {
  description = "Existing VPC subnet ID used by cluster"
  value       = data.yandex_vpc_subnet.existing.id
}

output "security_group_id" {
  description = "Security group ID for HW46 Kubernetes"
  value       = yandex_vpc_security_group.k8s_main_sg.id
}
