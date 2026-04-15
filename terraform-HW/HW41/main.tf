# =============================================================================
# HW-41: root module
# Логика:
# - если переданы existing_network_id / existing_subnet_id -> используем их
# - если не переданы -> создаём новые сеть и подсеть
# =============================================================================

locals {
  use_existing_network = var.existing_network_id != ""
  use_existing_subnet  = var.existing_subnet_id != ""

  network_id = local.use_existing_network ? var.existing_network_id : yandex_vpc_network.hw41-network[0].id
  subnet_id  = local.use_existing_subnet ? var.existing_subnet_id : yandex_vpc_subnet.hw41-subnet[0].id
}

# -----------------------------------------------------------------------------
# Создаём сеть только если не передан existing_network_id
# -----------------------------------------------------------------------------
resource "yandex_vpc_network" "hw41-network" {
  count = local.use_existing_network ? 0 : 1
  name  = "hw41-network"
}

# -----------------------------------------------------------------------------
# Создаём подсеть только если не передан existing_subnet_id
# -----------------------------------------------------------------------------
resource "yandex_vpc_subnet" "hw41-subnet" {
  count          = local.use_existing_subnet ? 0 : 1
  name           = "hw41-subnet-a"
  zone           = var.yc_zone
  network_id     = local.network_id
  v4_cidr_blocks = [var.subnet_cidr]
}

# -----------------------------------------------------------------------------
# Модуль виртуальной машины
# -----------------------------------------------------------------------------
module "hw41-vm" {
  source = "./modules/vm"

  vm_name        = var.vm_name
  vm_hostname    = var.vm_hostname
  vm_description = var.vm_description

  zone      = var.yc_zone
  subnet_id = local.subnet_id

  image_family = var.image_family
  image_id     = var.image_id
  platform_id  = var.platform_id

  cores         = var.cores
  memory        = var.memory
  core_fraction = var.core_fraction

  boot_disk_size = var.boot_disk_size
  boot_disk_type = var.boot_disk_type

  nat         = var.nat
  preemptible = var.preemptible

  ssh_public_key = var.ssh_public_key

  # Явная зависимость для выполнения optional-задания по HW41.
  # Даже если используются существующие сеть/подсеть, Terraform это спокойно обработает.
  depends_on = [
    yandex_vpc_network.hw41-network,
    yandex_vpc_subnet.hw41-subnet
  ]
}