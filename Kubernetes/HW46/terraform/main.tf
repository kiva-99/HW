# =============================================================================
# Managed Kubernetes cluster and node group
# =============================================================================

resource "yandex_kubernetes_cluster" "hw46_cluster" {
  name        = var.cluster_name
  description = "HW46 Managed Kubernetes cluster"
  folder_id   = var.folder_id
  network_id  = data.yandex_vpc_network.existing.id

  service_account_id      = yandex_iam_service_account.k8s_manager.id
  node_service_account_id = yandex_iam_service_account.k8s_node.id

  master {
    version   = var.k8s_version
    public_ip = true

    zonal {
      zone      = data.yandex_vpc_subnet.existing.zone
      subnet_id = data.yandex_vpc_subnet.existing.id
    }

    security_group_ids = [
      yandex_vpc_security_group.k8s_main_sg.id
    ]
  }

  depends_on = [
    yandex_resourcemanager_folder_iam_member.k8s_agent,
    yandex_resourcemanager_folder_iam_member.vpc_public_admin,
    yandex_resourcemanager_folder_iam_member.load_balancer_admin,
    yandex_resourcemanager_folder_iam_member.images_puller
  ]
}

resource "yandex_kubernetes_node_group" "hw46_node_group" {
  name        = var.node_group_name
  description = "HW46 Managed Kubernetes node group"
  cluster_id  = yandex_kubernetes_cluster.hw46_cluster.id

  instance_template {
    platform_id = "standard-v3"

    network_interface {
      nat                = true
      subnet_ids         = [data.yandex_vpc_subnet.existing.id]
      security_group_ids = [yandex_vpc_security_group.k8s_main_sg.id]
    }

    resources {
      cores  = var.node_cores
      memory = var.node_memory
    }

    boot_disk {
      type = "network-ssd"
      size = var.node_disk_size
    }

    scheduling_policy {
      preemptible = true
    }
  }

  scale_policy {
    fixed_scale {
      size = var.node_count
    }
  }

  allocation_policy {
    location {
      zone = data.yandex_vpc_subnet.existing.zone
    }
  }

  depends_on = [
    yandex_kubernetes_cluster.hw46_cluster
  ]
}
