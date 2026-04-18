# =========================
# Existing infrastructure used as data
# =========================

data "yandex_vpc_network" "existing" {
  name = var.existing_network_name
}

data "yandex_vpc_subnet" "existing" {
  name = var.existing_subnet_name
}

locals {
  cloud_init_user_data = format(
    "%s\n",
    replace(trimspace(file("${path.module}/files/cloud-init.yaml")), "\r\n", "\n")
  )
}

# =========================
# Existing security group to import
# =========================

resource "yandex_vpc_security_group" "main" {
  name        = var.existing_security_group_name
  description = "Default security group for network"
  network_id  = data.yandex_vpc_network.existing.id
}

# =========================
# Existing VM to import
# =========================

resource "yandex_compute_instance" "main" {
  name               = var.existing_vm_name
  hostname           = var.existing_vm_name
  platform_id        = "standard-v3"
  zone               = var.yc_zone
  service_account_id = var.existing_vm_service_account_id

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

  secondary_disk {
    disk_id     = "fhmuab7r74l5o7q1fd3c"
    auto_delete = false
  }

  metadata = {
    "ssh-keys"  = "ubuntu:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5PpEPEIeP5a9vLQmDTA5ZdYTwSDeEaDpFB0HHU9l0n+LzJzjO3lMBXpC/e1DBJ15MFq+/p/UX4wrpZK1VRqPNiY6QFoLd/Q9zpqbsgwEUzS9Wu00ACa2BpEhA8VpEzOnMioDJQ4rOP7tKkQSozp7QFwG1la5pCGE4uDy/2P0bfleUlFKR2DZlIPq7cbGuIWXFJYM69zifkZN8LUbplty4bcTr4hGcw7Uj4MSw8ill445e1In8HR0fxbzvbcBiFiifGqcZP5WVuXyIcq/yvk7AWsmTMGGZB6vYIf0MH/EmHhiPQXc30mwzq2oYKODHe8qPdZ1lDyXbLro3gF7+//h3 roman@DESKTOP-AGLSB50"
    "user-data" = local.cloud_init_user_data
  }

  metadata_options {
    aws_v1_http_endpoint = 1
    aws_v1_http_token    = 2
    gce_http_endpoint    = 1
    gce_http_token       = 1
  }

  network_interface {
    subnet_id = data.yandex_vpc_subnet.existing.id
    nat       = true
  }

  lifecycle {
    ignore_changes = [
      metadata["user-data"]
    ]
  }
}