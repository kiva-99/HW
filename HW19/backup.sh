#!/bin/bash
set -e

BACKUP_DIR="/home/roman/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="postgres"
DB_USER="postgres"

# Жёстко задаём IP этой ноды
#MY_IP="192.168.100.102"
MY_IP=$(ip -4 addr show | grep -oP '192\.168\.100\.\d+' | head -1)

# Получаем роль текущей ноды через jq
ROLE=$(curl -s "http://$MY_IP:8008/cluster" | \
       jq -r --arg ip "$MY_IP" '.members[] | select(.host == $ip) | .role')

if [ "$ROLE" != "leader" ]; then
    echo "[$(date)] Not a leader. Skipping backup."
    exit 0
fi

mkdir -p "$BACKUP_DIR"

# Выполняем бэкап
pg_dump -U "$DB_USER" -h "$MY_IP" -p 5432 "$DB_NAME" > "$BACKUP_DIR/backup_$DATE.sql"

# Оставляем только последние 7 бэкапов
ls -t "$BACKUP_DIR"/backup_*.sql | tail -n +8 | xargs -r rm

echo "[$(date)] Backup created: $BACKUP_DIR/backup_$DATE.sql"
