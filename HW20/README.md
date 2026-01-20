cat > README.md << 'EOF'
# HW20: Управление конфигурацией с Ansible

## Цель
Настроить Ansible на машине `pg2` для управления нодой `pg1`.

## Инфраструктура
- Control node: `pg2` (192.168.100.102)
- Managed node: `pg1` (192.168.100.101), SSH на порту 2222
- Используется существующий SSH-ключ (~/.ssh/id_rsa)

## Файлы
- `inventory.ini` — описание хоста с указанием порта 2222
- `ansible.cfg` — отключение host_key_checking
- `playbook.yaml` — создаёт файл `/tmp/ansible_hw20_test.txt` на `pg1`

## Результат
- Playbook успешно выполнен (см. `снимок1.png`)
- Файл подтверждён на удалённой машине через Ansible (см. `снимок2.png`)

EOF
