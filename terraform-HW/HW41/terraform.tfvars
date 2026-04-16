
sa_key_file  = "key.json"
yc_cloud_id  = "b1g7n8p29nt9r3i5e3m5"
yc_folder_id = "b1ga0ad79qngmcfham7u"
yc_zone      = "ru-central1-a"

existing_network_id = "enpo97c65fm8aa12m3a3"
existing_subnet_id  = "e9bg48ijtd56irh19o8e"

subnet_cidr = "10.11.0.0/24"

vm_name        = "hw41-vm-optimized"
vm_hostname    = "vm"
vm_description = "Создана через Terraform модуль"

image_family = "ubuntu-2204-lts"
platform_id  = "standard-v3"
image_id     = "fd8r71tg4mg5b3uiholm"

cores         = 2
memory        = 1
core_fraction = 20

boot_disk_size = 10
boot_disk_type = "network-hdd"

nat         = true
preemptible = true

ssh_public_key = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC5PpEPEIeP5a9vLQmDTA5ZdYTwSDeEaDpFB0HHU9l0n+LzJzjO3lMBXpC/e1DBJ15MFq+/p/UX4wrpZK1VRqPNiY6QFoLd/Q9zpqbsgwEUzS9Wu00ACa2BpEhA8VpEzOnMioDJQ4rOP7tKkQSozp7QFwG1la5pCGE4uDy/2P0bfleUlFKR2DZlIPq7cbGuIWXFJYM69zifkZN8LUbplty4bcTr4hGcw7Uj4MSw8ill445e1In8HR0fxbzvbcBiFiifGqcZP5WVuXyIcq/yvk7AWsmTMGGZB6vYIf0MH/EmHhiPQXc30mwzq2oYKODHe8qPdZ1lDyXbLro3gF7+//h3 roman@DESKTOP-AGLSB50"