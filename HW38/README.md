# 📦 HW38: Работа с AWS CLI и Boto3 в Yandex Cloud

## 👨‍ Студент
**Иванов Кирилл**

## 📅 Дата выполнения
2 апреля 2026 года

## 🎯 Цель задания
Освоить работу с Object Storage через AWS CLI и Boto3, настроить права доступа, создать ВМ с сервисным аккаунтом и настроить serverless-функцию с триггером.

---

## 📋 Задание

### Обязательные пункты:
1. ✅ Установить AWS CLI и настроить конфигурацию
2. ✅ Создать бакет S3 и загрузить файлы (через Boto3)
3. ✅ Изменить права доступа к файлу
4. ✅ Скачать файл через AWS CLI
5. ✅ Удалить файл через AWS CLI
6. ✅ Создать EC2 instance с правами на S3

### Опциональный пункт:
7. ✅ Cloud Functions + триггер на Object Storage

---

## 🛠 Выполненные шаги

### 1️⃣ Настройка AWS CLI

```bash
# Версия AWS CLI
aws --version
# aws-cli/2.34.21 Python/3.14.3 Linux/5.15.0-173-generic

# Настройка алиаса для Yandex Cloud
echo "alias aws='aws --endpoint-url=https://storage.yandexcloud.net'" >> ~/.bashrc
source ~/.bashrc
```

### 2️⃣ Создание бакета с публичным доступом

**Скрипт автоматизации:** `~/create-public-bucket.sh`

```bash
#!/bin/bash
# Создание бакета
yc storage bucket create --name hw38-demo-****

# Включение публичного доступа
yc storage bucket update hw38-demo-***** \
  --public-read \
  --public-list
```

**Результат:**
- Бакет: `hw38-demo-*****`
- Публичный доступ: ✅ `read=true`, `list=true`
- Файлы:
  - `file1.txt` (58 bytes)
  - `index.html` (1779 bytes)
  - `boto3-test.txt` (133 bytes)

**Публичные ссылки:**
- https://storage.yandexcloud.net/hw38-demo-******/index.html
- https://storage.yandexcloud.net/hw38-demo-******/file1.txt

### 3️⃣ Работа с Boto3 (Python)

**Скрипт:** `~/boto3-s3-demo.py`

```python
import boto3

s3_client = boto3.client(
    's3',
    endpoint_url='https://storage.yandexcloud.net',
    region_name='ru-central1'
)

# Загрузка файла
s3_client.upload_file('/tmp/boto3-test.txt', 'hw38-demo-****', 'boto3-test.txt')

# Установка публичного доступа
s3_client.put_object_acl(
    ACL='public-read',
    Bucket='hw38-demo-***',
    Key='boto3-test.txt'
)

# Скачивание файла
s3_client.download_file('hw38-demo-****', 'boto3-test.txt', '/tmp/downloaded-boto3.txt')

# Удаление файла
s3_client.delete_object(Bucket='hw38-demo-****', Key='boto3-test.txt')
```

### 4️⃣ Скачивание и удаление через AWS CLI

```bash
# Скачать файл
aws s3 cp s3://hw38-demo-****/file1.txt ./downloaded-file1.txt

# Удалить файл
aws s3 cp /tmp/to-delete.txt s3://hw38-demo-********/to-delete.txt
aws s3 rm s3://hw38-demo-****/to-delete.txt
```

### 5️⃣ ВМ с сервисным аккаунтом

**ВМ:** `hw-35-vm` (IP: `178.*****`)

**Сервисный аккаунт:** `hw35-service-account` (ID: `aje*****`)

**Роли:**
- `storage.admin` — полный доступ к Object Storage
- `editor` — доступ на редактирование ресурсов

**Привязка СА к ВМ:**
```bash
yc compute instance update hw-35-vm \
  --service-account-id aje5q******

yc compute instance restart hw-35-vm
```

**Проверка доступа через метаданные:**
```bash
yc storage bucket list
# Работает без ~/.aws/credentials через IAM-токен из метаданных
```

### 6️⃣ Cloud Functions + триггер (Optional)

**Функция:** `hw38-s3-trigger-function` (ID: `d4ei9m*****`)

**Триггер:** `hw38-s3-trigger` (ID: `a1s48******`)

**Сервисные аккаунты:**
- Для функции: `hw38-function-sa` (`aje90************`)
- Для триггера: `hw38-trigger-sa` (`aje904***********`)

**Создание триггера:**
```bash
# Создаём триггер через CLI
yc serverless trigger create object-storage \
--name hw38-s3-trigger \
--bucket-id hw38****** \
--prefix uploads/ \
--events create-object \
--invoke-function-id d4ei9m******* \
--invoke-function-service-account-id aje***** \
--retry-attempts 3
```

**Тестирование:**
```bash
# Загрузка файла в папку uploads/
aws s3 cp /tmp/trigger-test.txt s3://hw38-demo-****/uploads/trigger-test.txt

# Проверка логов функции
yc serverless function logs hw38-s3-trigger-function --limit 10
```

**Результат:** Функция автоматически запускается при загрузке файла в бакет!

---

## 📊 Инфраструктура

```
┌─────────────────────────────────────────────────────────────┐
│  Yandex Cloud Infrastructure (HW38)                         │
├─────────────────────────────────────────────────────────────┤
│  ВМ: hw-35-vm                                               │
│  IP: 178****                                      │
│  СА: aje5qjelspl42t0bt197 (storage.admin, editor)           │
├─────────────────────────────────────────────────────────────┤
│  Бакет: hw38-demo-*****                                     │
│  ID: e3e0******************                                 │
│  Публичный доступ: read=true, list=true                     │
│  Файлы: file1.txt, index.html, boto3-test.txt               │
├─────────────────────────────────────────────────────────────┤
│  Cloud Function: hw38-s3-trigger-function                   │
│  ID: d4ei9m****************                                 │
│  Trigger: hw38-s3-trigger                                   │
│  Событие: загрузка файла → вызов функции                    │
├─────────────────────────────────────────────────────────────┤
│  CLI:                                                       │
│    - yc: 0.204.0                                            │
│    - aws: 2.34.21 (с endpoint YC)                           │
│    - boto3: 1.42.80                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Файлы проекта

```
HW38/
├── README.md                    # Этот файл
├── create-public-bucket.sh      # Скрипт создания бакета
├── boto3-s3-demo.py             # Python-скрипт с Boto3
└── Скриншоты/
    ├── Публичный доступ к файлу.png
    ├── Роли сервисного аккаунта.png
    ├── Сервисный аккаунт ВМ.png
    ├── Скрипты.png
    ├── Список файлов в бакете.png
    └── Функции-тригеры.png