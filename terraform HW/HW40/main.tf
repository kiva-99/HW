resource "yandex_vpc_network" "net" {
  name = "lesson-net"
}
resource "yandex_vpc_subnet" "subnet" {
  name           = "lesson-subnet"
  zone           = "ru-central1-a"
  network_id     = yandex_vpc_network.net.id
  v4_cidr_blocks = ["10.10.0.0/16"]
}

resource "yandex_compute_instance" "vm" {
  name        = "lesson-vm"
  platform_id = "standard-v3" # или "standard-v3" для Ice Lake
  zone        = "ru-central1-a"

  # ✅ Разрешаем остановку ВМ для применения изменений
  allow_stopping_for_update = true

  resources {
    cores         = 2
    memory        = 1  # Уменьшаем до 1 ГБ (как в hw-35-vm)
    core_fraction = 20 # ✅ Гарантированная доля 20% (вместо 100%)
  }

  # ✅ Прерываемая ВМ (значительно дешевле!)
  scheduling_policy {
    preemptible = true
  }

  boot_disk {
    initialize_params {
      image_id = "fd83ica41cade1mj35sr"
      type     = "network-hdd"
      size     = 10
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet.id
    nat       = true
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_rsa.pub")}"
  }
}