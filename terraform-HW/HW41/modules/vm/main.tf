terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
}

data "yandex_compute_image" "vm_image" {
  count  = var.image_id == "" ? 1 : 0
  family = var.image_family
}

resource "yandex_compute_instance" "this" {
  name        = var.vm_name
  hostname    = var.vm_hostname
  description = var.vm_description

  zone        = var.zone
  platform_id = var.platform_id

  allow_stopping_for_update = true

  resources {
    cores         = var.cores
    memory        = var.memory
    core_fraction = var.core_fraction
  }

  boot_disk {
    initialize_params {
      image_id = var.image_id != "" ? var.image_id : data.yandex_compute_image.vm_image[0].id
      size     = var.boot_disk_size
      type     = var.boot_disk_type
    }
  }

  network_interface {
    subnet_id = var.subnet_id
    nat       = var.nat
  }

  metadata = {
    ssh-keys = "ubuntu:${var.ssh_public_key}"
  }

  scheduling_policy {
    preemptible = var.preemptible
  }
}