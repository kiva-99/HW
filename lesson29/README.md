#  DevOps Infrastructure Automation

Проект для автоматизации задач управления инфраструктурой: сбор логов, архивирование, ротация и мониторинг сервисов.

## Описание

Система состоит из трёх модулей:

| Модуль | Файл | Назначение |
|--------|------|------------|
| **Log Collector** | `log_collector.py` | Сбор и архивирование .log файлов с меткой времени |
| **Log Manager** | `log_manager.py` | ООП-класс для управления жизненным циклом логов (архивация + очистка) |
| **Service Monitor** | `service_monitor.py` | Мониторинг состояния сервисов и генерация отчётов |

##  Быстрый старт

## Использование
Задание 1: Сбор и архивирование логов

python log_collector.py --source test_logs --dest backups

# Аргументы:
--source — путь к директории с логами
--dest — путь к директории для бэкапов

Задание 2: LogManager (ООП + ротация)

# Архивация + очистка старых файлов
python log_manager.py --source test_logs --dest backups --retention 7

# Только очистка (без новой архивации)
python log_manager.py --source test_logs --dest backups --retention 7 --cleanup-only

# Аргументы:
--retention — количество дней хранения архивов (по умолчанию 7)
--cleanup-only — флаг только для очистки

Задание 3: Мониторинг сервисов

python service_monitor.py --config services.json --output service_status_report.txt

# Аргументы:
--config — путь к JSON файлу конфигурации
--output — имя файла отчёта

Структура проекта
```
lesson29/
├── log_collector.py          # Задание 1
├── log_manager.py            # Задание 2 (класс LogManager)
├── service_monitor.py        # Задание 3 (класс ServiceMonitor)
├── services.json             # Конфигурация сервисов
├── README.md                 # Этот файл
├── test_logs/                # Тестовые логи
├── backups/                  # Архивы логов
└── service_status_report.txt # Отчёт мониторинга
```
# Пример конфигурации (services.json)

{
  "services": [
    {"name": "BITS"},
    {"name": "Spooler"},
    {"name": "W32Time"}
  ]
}

# Особенности реализации
✅ Кроссплатформенность (Windows + Linux)
✅ Обработка ошибок (отсутствие директорий, файлов)
✅ ООП подход (классы LogManager, ServiceMonitor)
✅ Гибкая настройка через аргументы командной строки
✅ JSON конфигурация для мониторинга