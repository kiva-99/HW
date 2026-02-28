# HW32 - Jenkins Pipeline с использованием Groovy и DSL

## 👤 Студент
**Иванов Кирилл Константинович**

## 📝 Описание задания
Создание Jenkins Pipeline для автоматизации сборки, тестирования и деплоя веб-приложения с использованием:
- Declarative Pipeline syntax
- Groovy scripting
- Docker контейнеризации
- DSL для генерации отчетов

## 🏗 Архитектура решения

### Репозитории
1. **pipeline** (https://github.com/kiva-99/pipeline) - содержит Jenkinsfile и Groovy-скрипты
2. **HW** (https://github.com/kiva-99/HW) - содержит веб-приложение (hw24/Dockerfile)

### Компоненты
- **Jenkinsfile** - основной декларативный pipeline
- **groovy-scripts/deploy-app.groovy** - скрипт деплоя Docker-контейнера
- **dsl-scripts/report-generator.groovy** - генерация JSON-отчета о сборке

## 🚀 Этапы Pipeline

### 1. Checkout Application
- Клонирование репозитория приложения из GitHub
- Переключение на ветку main

### 2. Build Application
- Проверка наличия Dockerfile
- Сборка Docker-образа с тегом `hw32-webapp:${BUILD_NUMBER}`

### 3. Run Tests (опционально)
- Установка pytest
- Запуск автоматических тестов
- Публикация отчета JUnit

### 4. Cleanup Old Containers (опционально)
- Удаление старых контейнеров с именем hw32-webapp

### 5. Deploy Application
- Загрузка внешнего Groovy-скрипта deploy-app.groovy
- Остановка и удаление предыдущего контейнера
- Запуск нового контейнера на порту 8090

### 6. Health Check
- Проверка доступности приложения через docker exec
- Многократные попытки (до 10) с интервалом 2 секунды
- Вывод логов при ошибке

### 7. Generate Report
- Генерация JSON-отчета о сборке
- Сохранение в reports/build-${BUILD_NUMBER}.json

## ⚙️ Параметры Pipeline

| Параметр | Тип | Значение по умолчанию | Описание |
|----------|-----|----------------------|----------|
| DEPLOY_ENV | choice | dev | Окружение (dev/staging/production) |
HW_BRANCH | string | (пусто) | Ветка репозитория HW для сборки (main, develop, feature/...)
| RUN_TESTS | boolean | true | Запускать ли тесты |
| CLEAN_OLD | boolean | true | Удалять ли старые контейнеры |
| APP_VERSION_OVERRIDE | string | (пусто) | Переопределить версию |

## 📊 Результаты выполнения

### Успешная сборка #24
- ✅ Docker-образ собран: `hw32-webapp:24`
- ✅ Контейнер запущен: `hw32-webapp-dev`
- ✅ Приложение доступно на порту: **8090**
- ✅ Health Check пройден: HTTP 200 OK
- ✅ Email-уведомление отправлено

### Скриншоты
В папке `screenshots/` представлены:
1. Jenkins - окно запуска с параметрами.png
2. Pipeline view с зелеными галочками всех этапов.png
3. Артефакты сборки (вкладка Artifacts).png
4. Браузер с открытым httplocalhost8090.png

## 🔧 Требования к окружению

- Jenkins с установленными плагинами:
  - Pipeline
  - Docker Pipeline
  - Git
  - JUnit
  - Email Extension

- Docker агент с меткой `docker-builder`
- Доступ к GitHub (публичные репозитории)

## 📄 Выполненные требования

✅ **Требование 1-9**: Declarative Pipeline с агентами, этапами, условиями, параметрами и обработкой ошибок

✅ **Требование 10**: Groovy-скрипт для сборки и деплоя веб-приложения с:
- Клонированием репозитория
- Docker сборкой
- Запуском контейнера
- Проверкой доступности
- Обработкой ошибок

✅ **Требование 11**: Удаление предыдущей версии контейнера перед деплоем

✅ **Требование 12**: DSL для генерации отчета (Groovy-скрипт report-generator.groovy)

## 🌐 Доступ к приложению

После успешного деплоя приложение доступно по адресу:
http://localhost:8090/
