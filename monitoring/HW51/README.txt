HW51 — Логирование и ротация логов

Цель:
Настроить логирование приложения, хранение логов в файле и ротацию логов через logrotate.

В рамках задания использовано приложение TypeSpeed Arena из дипломного проекта.

Что реализовано:
1. Backend пишет структурированные JSON-логи.
2. Логи пишутся в stdout контейнера.
3. Логи пишутся в файл typespeed-backend.log.
4. Для каждого HTTP-запроса создаётся request_id.
5. Логируются бизнес-события:
   - app_start
   - texts_loaded
   - texts_requested
   - result_saved
   - leaderboard_requested
   - invalid_result_payload
   - http_request
6. Настроена Ansible-role logging.
7. Настроен шаблон logrotate для файла typespeed-backend.log.
8. В production docker-compose добавлен volume ./logs:/app/logs.

Где хранятся логи:
В контейнере:
  /app/logs/typespeed-backend.log

На сервере:
  /opt/typespeed-arena/logs/typespeed-backend.log

Почему так:
Контейнер пишет логи в /app/logs, а volume пробрасывает эту директорию на host.
Это позволяет не терять логи при пересоздании контейнера.

Logrotate:
Файл:
  /etc/logrotate.d/typespeed-backend

Правила:
  daily          — ротация каждый день
  rotate 7       — хранить 7 архивных файлов
  compress       — сжимать старые логи
  delaycompress  — сжимать не сразу, а со следующей ротации
  missingok      — не падать, если файла нет
  notifempty     — не ротировать пустой файл
  copytruncate   — безопасно ротировать лог без остановки приложения

Проверочные команды:

Запуск тестового контейнера:
docker run --rm -d `
  --name typespeed-backend-logging-test `
  -p 5000:5000 `
  -v ${PWD}\app\backend\logs:/app/logs `
  typespeed-backend-logging-test

Проверка healthcheck:
curl.exe http://localhost:5000/health

Проверка API:
curl.exe http://localhost:5000/api/texts

Проверка записи результата:
$body = @{
  username = "guest"
  wpm = 75
  accuracy = 96
  errors = 2
  text_id = 1
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "http://localhost:5000/api/results" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

Просмотр логов из файла:
Get-Content .\app\backend\logs\typespeed-backend.log -Tail 20

Просмотр логов контейнера:
docker logs typespeed-backend-logging-test --tail=20

Остановка тестового контейнера:
docker stop typespeed-backend-logging-test

Вывод:
HW51 выполнено. Приложение генерирует структурированные JSON-логи, логи сохраняются в файл, доступны через docker logs и подготовлены к централизованному сбору через Loki/ELK.
