# HW39: Cloud CDN + Cloud Function Monitoring (Yandex Cloud)

## 👤 Студент
**Иванов Кирилл Константинович**

## 🎯 Цель задания
Настроить раздачу статического сайта через **Yandex Cloud CDN** (аналог AWS CloudFront) и создать **Cloud Function** для автоматического сбора метрик работы CDN.

## 🏗 Архитектура решения

```
┌─────────────────────────────────────────────────────┐
│                    ПОЛЬЗОВАТЕЛЬ                      │
│              (браузер, мобильное приложение)          │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│              Yandex Cloud CDN                        │
│  • Домен: cdn.typespeedarena.ru                     │
│  • Resource ID: bc8rjft7hd6zxa3unmtt                 │
│  • Кеширование: CDN=86400s, Browser=3600s           │
│  • gzip: ✅, CORS: *, Host Header: настроен         │
└────────────────┬────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────┐
│         Object Storage (Origin)                     │
│  • Бакет: hw39-cdn-site-8945                        │
│  • Файлы: index.html, style.css, app.js            │
│  • Доступ: публичный (read, list)                   │
└────────────────┬────────────────────────────────────┘
                 │
    ┌────────────┴────────────┐
    ▼                         ▼
┌─────────┐         ┌─────────────────┐
│ Cloud   │         │ Cloud Function  │
│ DNS     │         │ hw39-cdn-monitoring │
│ CNAME   │         │ • Timer: каждые 3ч │
│ запись  │         │ • Отчёты в S3   │
└─────────┘         └─────────────────┘
```

---

## 📦 Компоненты инфраструктуры

### 1️⃣ Object Storage (Origin)
| Параметр | Значение |
|----------|----------|
| **Имя бакета** | `hw39-cdn-site-8945` |
| **Folder ID** | `b1gcijdrjlf3m935prl2` |
| **Файлы** | `index.html` (556 B), `style.css` (542 B), `app.js` (281 B) |
| **Публичный доступ** | `read: true`, `list: true` |
| **Проверка** | `curl -I → HTTP 200, Content-Type: text/html` |

**Команды создания:**
```bash
# Создание бакета
yc storage bucket create --name hw39-cdn-site-8945

# Загрузка файлов
aws s3 sync ~/hw39-site/ s3://hw39-cdn-site-8945/

# Включение публичного доступа
yc storage bucket update --name hw39-cdn-site-8945 --public-read --public-list
```

---

### 2️⃣ Cloud CDN
| Параметр | Значение |
|----------|----------|
| **CNAME (домен)** | `cdn.typespeedarena.ru` |
| **Resource ID** | `bc8rjft7hd6zxa3unmtt` |
| **Origin Group** | `s3-hw39-cdn-site-8945` (ID: `4173645582027495463`) |
| **Origin Protocol** | `HTTP` |
| **Host Header** | `hw39-cdn-site-8945.storage.yandexcloud.net` ⚠️ |
| **Кеширование (CDN)** | `86400s` (1 день) |
| **Кеширование (браузер)** | `3600s` (1 час) |
| **gzip** | ✅ включено |
| **CORS** | `Access-Control-Allow-Origin: *` |
| **Ignore cookies/query** | ✅ включено |

**Ключевая команда создания (CLI):**
```bash
yc cdn resource create cdn.typespeedarena.ru \
--origin-group-id 4173645582027495463 \
--origin-protocol HTTP
```

> ⚠️ **Важно**: В версии `yc CLI 1.0.0` расширенные настройки (`--host-header`, `--gzip-on`, `--cors`) применяются через `yc cdn resource update` после создания ресурса.

---

### 3️⃣ Cloud DNS
| Параметр | Значение |
|----------|----------|
| **Зона** | `typespeedarena-zone` |
| **Запись** | `cdn.typespeedarena.ru. CNAME 7aae7b166e022b18.topology.gslb.yccdn.ru` |
| **TTL** | `3600` |

**Команда создания:**
```bash
yc dns zone add-records \
--name typespeedarena-zone \
--record "cdn 3600 CNAME 7aae7b166e022b18.topology.gslb.yccdn.ru"
```

---

### 4️⃣ Cloud Function (Monitoring)
| Параметр | Значение |
|----------|----------|
| **Имя функции** | `hw39-cdn-monitoring` |
| **Function ID** | `d4e2o2mcuvpcltg0ab5m` |
| **Runtime** | `python39` |
| **Entry point** | `index.handler` |
| **Memory / Timeout** | `128 MB / 30s` |
| **Service Account** | `aje0lsie3loedsgnp9gh` |
| **Роли SA** | `monitoring.viewer`, `storage.editor`, `functions.functionInvoker`, `iam.serviceAccounts.user` |

#### Timer Trigger
| Параметр | Значение |
|----------|----------|
| **Имя триггера** | `hw39-cdn-monitoring-timer` |
| **Trigger ID** | `a1sadadjbl28k9epj1ib` |
| **Cron-выражение** | `0 */3 ? * * *` (каждые 3 часа) |
| **Статус** | `ACTIVE` |

#### Логика функции
```python
1. Получение IAM-токена из метаданных функции
2. Запрос к Monitoring API:
   POST /monitoring/v2/data/read?folderId=<FOLDER_ID>
   Body: {
     "query": '{service="cdn", resource_id="<CDN_ID>"}',
     "fromTime": "...",
     "toTime": "..."
   }
3. Агрегация метрик: requests_total, bandwidth, cache_hit/miss
4. Формирование сжатого JSON-отчёта (~125 байт)
5. Сохранение в S3: s3://hw39-cdn-site-8945/cdn-reports/cdn-monitoring-YYYY-MM-DD.json
```

**Пример отчёта:**
```json
{"ts":"2026-04-04T17:53:11.674702Z","cdn":"bc8rjft7hd6zxa3unmtt","period":"3h","req":0,"bw":0,"ch":0,"cm":0,"chr":0,"err":""}
```

---

## 🧪 Тестирование

### Проверка CDN
```powershell
curl -I http://cdn.typespeedarena.ru/index.html
```
**Ожидаемый вывод:**
```
HTTP/1.1 200 OK
Server: nginx
Content-Type: text/html
Cache-Control: max-age=3600
Cache-Status: MISS  # После повторного запроса → HIT
```

### Проверка функции
```powershell
yc serverless function invoke --id d4e2o2mcuvpcltg0ab5m
```
**Ожидаемый вывод:**
```json
{"statusCode": 200, "body": "✅ Report saved: cdn-reports/cdn-monitoring-2026-04-04.json"}
```

### Проверка отчёта в бакете
```powershell
aws s3 cp s3://hw39-cdn-site-8945/cdn-reports/cdn-monitoring-2026-04-04.json - --endpoint-url https://storage.yandexcloud.net | python3 -m json.tool
```

---

## ⚠️ Известные ограничения

### Метрики CDN в Monitoring API
На момент тестирования функция возвращает пустые значения метрик (`req: 0, bw: 0, ...`). Это связано с **особенностью Yandex Cloud**:

> **Шард для хранения метрик CDN** создаётся автоматически в Monitoring API только после появления данных. Для новых CDN-ресурсов это может занять **24-48 часов** после начала генерации трафика.

**Что уже работает:**
- ✅ Функция запускается без ошибок (`statusCode: 200`)
- ✅ Запрос к Monitoring API формируется корректно (правильный синтаксис `query`, `folderId` в URL)
- ✅ Отчёты сохраняются в Object Storage
- ✅ Формат отчёта соответствует требованиям (сжатый JSON, ~125 байт)

**После появления шарда** функция автоматически начнёт получать реальные метрики без изменений в коде.

---

## 💰 Оценка стоимости

| Компонент | Расход | Стоимость/мес |
|-----------|--------|---------------|
| **Cloud Function** | 8 вызовов/день × 128MB × 30s | ~0.02₽ |
| **Object Storage** (отчёты) | ~125 байт/день × 30 дней | ~0.001₽ |
| **Cloud CDN** (базовый тариф) | Без логов, минимальный трафик | ~0₽ |
| **Итого** | | **~0.03₽/мес** ✅ |

> Все ресурсы укладываются в грант нового пользователя.

---

## 🗂 Структура репозитория

```
HW39/
├── README.md                          # Этот файл
├── configs/
│   ├── cdn-config.yaml               # Экспорт конфигурации CDN
│   ├── cdn-resource.yaml             # Детали CDN-ресурса
│   ├── dns-zone.yaml                 # Настройки DNS-зоны
│   ├── function-config.yaml          # Параметры Cloud Function
│   └── trigger-config.yaml           # Конфигурация Timer Trigger
├── scripts/cdn-monitoring/
│   ├── index.py                      # Исходный код функции (Python)
│   ├── requirements.txt              # Зависимости: requests, boto3
│   └── function.zip                  # Архив для деплоя
├── screenshots/
│   ├── CDN Resource (конфигурация).png
│   ├── Cloud Function (параметры).png
│   ├── Object Storage (список файлов в бакете).png
│   ├── Timer Trigger (настройки).png
│   ├── Ручной запуск функции (тест).png
│   └── Содержимое отчёта (скачать и показать).png
└── tests/
    ├── cdn-monitoring-report.json    # Пример отчёта из бакета
    ├── curl-cdn-test.txt             # Вывод curl-тестов CDN
    └── function-invoke.json          # Результат ручного вызова функции
```

---

## 🔧 Ключевые команды для воспроизведения

```bash
# === 1. Создание бакета и загрузка файлов ===
yc storage bucket create --name hw39-cdn-site-8945
aws s3 sync ~/hw39-site/ s3://hw39-cdn-site-8945/
yc storage bucket update --name hw39-cdn-site-8945 --public-read --public-list

# === 2. Создание CDN-ресурса ===
yc cdn resource create cdn.typespeedarena.ru \
--origin-group-id 4173645582027495463 \
--origin-protocol HTTP

# === 3. Настройка параметров через update ===
yc cdn resource update bc8rjft7hd6zxa3unmtt \
--host-header hw39-cdn-site-8945.storage.yandexcloud.net \
--browser-cache-expiration-time 3600 \
--gzip-on \
--cors '*'

# === 4. Настройка DNS ===
yc dns zone add-records \
--name typespeedarena-zone \
--record "cdn 3600 CNAME 7aae7b166e022b18.topology.gslb.yccdn.ru"

# === 5. Создание Cloud Function ===
yc serverless function create --name hw39-cdn-monitoring
yc serverless function version create \
--function-name hw39-cdn-monitoring \
--runtime python39 \
--entrypoint index.handler \
--memory 128m \
--execution-timeout 30s \
--service-account-id aje0lsie3loedsgnp9gh \
--source-path function.zip \
--environment FOLDER_ID=b1gcijdrjlf3m935prl2 \
--environment CDN_RESOURCE_ID=bc8rjft7hd6zxa3unmtt \
--environment BUCKET_NAME=hw39-cdn-site-8945 \
--environment AWS_ACCESS_KEY_ID=<ключ> \
--environment AWS_SECRET_ACCESS_KEY=<секрет>

# === 6. Создание Timer Trigger ===
yc serverless trigger create timer \
--name hw39-cdn-monitoring-timer \
--cron-expression "0 */3 ? * * *" \
--invoke-function-id d4e2o2mcuvpcltg0ab5m \
--invoke-function-service-account-id aje0lsie3loedsgnp9gh \
--folder-id b1gcijdrjlf3m935prl2
```

---
```
## 📚 Использованные ресурсы

- [Yandex Cloud CDN Documentation](https://yandex.cloud/ru/docs/cdn/)
- [Monitoring API: метод read](https://yandex.cloud/ru/docs/monitoring/api-ref/MetricsData/read)
- [Cloud Functions Documentation](https://yandex.cloud/ru/docs/functions/)
- [Object Storage S3 API](https://yandex.cloud/ru/docs/storage/s3/api/)
```
