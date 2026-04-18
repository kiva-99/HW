data "yandex_vpc_network" "existing" {
  name = "default"
}

data "yandex_vpc_subnet" "existing" {
  name = "default-ru-central1-a"
}

resource "yandex_vpc_security_group" "main" {
  name        = var.security_group_name
  description = "Security group for HW43 web server"
  network_id  = data.yandex_vpc_network.existing.id

  ingress {
    description    = "SSH"
    protocol       = "TCP"
    port           = 22
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description    = "HTTP"
    protocol       = "TCP"
    port           = 80
    v4_cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description    = "Allow all outbound traffic"
    protocol       = "ANY"
    v4_cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "yandex_compute_instance" "main" {
  name        = var.vm_name
  hostname    = var.vm_hostname
  zone        = var.yc_zone
  platform_id = "standard-v3"

  resources {
    cores         = 2
    memory        = 1
    core_fraction = 20
  }

  scheduling_policy {
    preemptible = true
  }

  boot_disk {
    auto_delete = true

    initialize_params {
      image_id = "fd8rnq92aj5v7sgi91e8"
      size     = 10
      type     = "network-ssd"
    }
  }

  network_interface {
    subnet_id          = data.yandex_vpc_subnet.existing.id
    nat                = true
    security_group_ids = [yandex_vpc_security_group.main.id]
  }

  metadata = {
    "ssh-keys"  = "ubuntu:${var.ssh_public_key}"
    "user-data" = file("${path.module}/files/cloud-init.yaml")
  }
}