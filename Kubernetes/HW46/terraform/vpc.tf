# =============================================================================
# Existing VPC network and subnet
# =============================================================================
# We do not create a new network because the Yandex Cloud folder has limits.
# Instead, we reuse existing lesson-net and lesson-subnet via data sources.

data "yandex_vpc_network" "existing" {
  network_id = var.existing_network_id
}

data "yandex_vpc_subnet" "existing" {
  subnet_id = var.existing_subnet_id
}
