# =============================================================================
# Security Group for HW46 Managed Kubernetes
# =============================================================================

resource "yandex_vpc_security_group" "k8s_main_sg" {
  name        = "hw46-k8s-main-sg"
  description = "Security group for HW46 Managed Kubernetes cluster"
  folder_id   = var.folder_id
  network_id  = data.yandex_vpc_network.existing.id

  ingress {
    protocol       = "TCP"
    description    = "Allow Kubernetes API access from trusted IP"
    v4_cidr_blocks = [var.trusted_ip_cidr]
    port           = 6443
  }

  ingress {
    protocol       = "TCP"
    description    = "Allow HTTPS API access from trusted IP"
    v4_cidr_blocks = [var.trusted_ip_cidr]
    port           = 443
  }

  ingress {
    protocol       = "TCP"
    description    = "Allow SSH from trusted IP"
    v4_cidr_blocks = [var.trusted_ip_cidr]
    port           = 22
  }

  ingress {
    protocol       = "TCP"
    description    = "Allow NodePort range from trusted IP for tests"
    v4_cidr_blocks = [var.trusted_ip_cidr]
    from_port      = 30000
    to_port        = 32767
  }

  ingress {
    protocol          = "TCP"
    description       = "Allow Network Load Balancer health checks"
    predefined_target = "loadbalancer_healthchecks"
    from_port         = 0
    to_port           = 65535
  }

  ingress {
    protocol       = "ANY"
    description    = "Allow internal cluster communication inside subnet"
    v4_cidr_blocks = ["10.10.0.0/16"]
    from_port      = 0
    to_port        = 65535
  }

  egress {
    protocol       = "ANY"
    description    = "Allow all outbound traffic"
    v4_cidr_blocks = ["0.0.0.0/0"]
    from_port      = 0
    to_port        = 65535
  }
}
