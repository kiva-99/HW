#!/bin/bash
# Автоматический бэкап базы hw18
DATE=$(date +%Y%m%d_%H%M)
sudo mysqldump hw18 > /home/roman/backups/hw18_$DATE.sql
# Удалим бэкапы старше 7 дней (опционально, но полезно)
find /home/roman/backups -name "hw18_*.sql" -mtime +7 -delete
