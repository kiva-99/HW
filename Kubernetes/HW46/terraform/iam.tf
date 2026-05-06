# =============================================================================
# IAM: Service accounts and roles for Managed Kubernetes
# =============================================================================

resource "yandex_iam_service_account" "k8s_manager" {
  name        = "hw46-k8s-manager"
  description = "Service account for HW46 Managed Kubernetes control plane"
  folder_id   = var.folder_id
}

resource "yandex_resourcemanager_folder_iam_member" "k8s_agent" {
  folder_id = var.folder_id
  role      = "k8s.clusters.agent"
  member    = "serviceAccount:${yandex_iam_service_account.k8s_manager.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "vpc_public_admin" {
  folder_id = var.folder_id
  role      = "vpc.publicAdmin"
  member    = "serviceAccount:${yandex_iam_service_account.k8s_manager.id}"
}

resource "yandex_resourcemanager_folder_iam_member" "load_balancer_admin" {
  folder_id = var.folder_id
  role      = "load-balancer.admin"
  member    = "serviceAccount:${yandex_iam_service_account.k8s_manager.id}"
}

resource "yandex_iam_service_account" "k8s_node" {
  name        = "hw46-k8s-node-sa"
  description = "Service account for HW46 Kubernetes worker nodes"
  folder_id   = var.folder_id
}

resource "yandex_resourcemanager_folder_iam_member" "images_puller" {
  folder_id = var.folder_id
  role      = "container-registry.images.puller"
  member    = "serviceAccount:${yandex_iam_service_account.k8s_node.id}"
}
