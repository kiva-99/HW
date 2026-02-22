@'
# HW31 — Continuous Integration с Jenkins

## 👤 Автор
Иванов Кирилл Константинович

## 📋 Описание
Реализация CI/CD пайплайна на базе Jenkins в Docker-среде Windows для автоматизации сборки, тестирования и уведомления о результатах.

## 🏗 Архитектура
- **Jenkins Master**: контейнер `jenkins-with-docker` (порт 8080)
- **Python-агент**: `jenkins-agent` (порт 2222, лейбл `docker-agent`)
- **Docker-агент**: `jenkins-docker-builder` (порт 2224, лейбл `docker-builder`)

## 🔄 Pipeline выполняет
1. Клонирование репозитория из GitHub
2. Проверку синтаксиса Python/Shell скриптов
3. Запуск тестов pytest
4. Сборку Docker-образа из `hw24/Dockerfile`
5. Email-уведомление о результате

## 📁 Структура
```
HW31/
├── README.md
├── jenkinsfile.groovy
└── screenshots/
├── nodes.png
├── console-output.png
├── email.png
└── docker-images.txt
```
'@ | Out-File -FilePath .\HW31\README.md -Encoding utf8