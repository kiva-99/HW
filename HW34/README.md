# HW34 — CI/CD Pipeline с параллельным выполнением и GitOps

## Цель задания

Построить полноценный CI/CD pipeline с:
- параллельным выполнением тестов
- автоматической сборкой и публикацией Docker образа
- GitOps подходом для управления деплоем

---

## Репозитории

| Репозиторий | Назначение |
|---|---|
| [kiva-99/HW34](https://github.com/kiva-99/HW34) | Исходный код приложения, Dockerfile, Jenkinsfile сборки |
| [kiva-99/HW34-deploy](https://github.com/kiva-99/HW34-deploy) | GitOps конфигурация деплоя, Jenkinsfile деплоера |
| [kirilliva/hw34-flask](https://hub.docker.com/repository/docker/kirilliva/hw34-flask) | Docker образы на DockerHub |

---

## Структура проекта (HW34)

```
hw34/
├── app/
│   ├── app.py              # Flask приложение (GET /, GET /health)
│   ├── test_app.py         # pytest тесты
│   └── requirements.txt    # flask, pytest, flake8
├── Dockerfile
└── Jenkinsfile
```

---

## Jenkins Jobs

### 1. HW34-parallel-pipeline

Основной pipeline сборки. Запускается автоматически через `pollSCM` каждые 2 минуты при появлении новых коммитов в `kiva-99/HW34`.

**Стейджи:**

```
Checkout
    └── скачивает код из GitHub

Build Docker Image
    └── docker build → kirilliva/hw34-flask:build-N

Parallel Tests (3 теста одновременно!)
    ├── pytest       → юнит-тесты приложения
    ├── flake8       → проверка стиля кода
    └── pip list     → аудит зависимостей

Push to DockerHub
    └── пушит :build-N и :latest

Update Deploy Config (GitOps)
    └── клонирует HW34-deploy
        обновляет deploy-config.yml: tag: build-N
        git commit + git push от имени Jenkins CI
```

### 2. HW34-GitOps-Deployer

GitOps деплоер. Запускается автоматически через `pollSCM` при изменении `kiva-99/HW34-deploy`.

**Стейджи:**

```
Read Deploy Config
    └── читает deploy-config.yml
        извлекает image и tag

Deploy
    ├── docker stop hw34-app
    ├── docker rm hw34-app
    └── docker run kirilliva/hw34-flask:build-N

Health Check
    └── python urllib → http://localhost:5000/health
        ожидает ответ ok
```

---

## GitOps — принцип работы

```
Разработчик делает git push в HW34
          │
          ▼
Jenkins HW34-parallel-pipeline
  собирает образ → пушит в DockerHub
  обновляет deploy-config.yml в HW34-deploy
          │
          ▼
Jenkins HW34-GitOps-Deployer
  читает deploy-config.yml
  деплоит актуальную версию
          │
          ▼
hw34-app запущен на порту 5000
```

**Ключевая идея:** `deploy-config.yml` — единственный источник правды о том, что задеплоено. Откат = `git revert` в HW34-deploy.

---

## deploy-config.yml

```yaml
app:
  name: hw34-app
  image: kirilliva/hw34-flask
  tag: build-14        # Jenkins обновляет это поле автоматически
  port: 5000

deploy:
  updated_by: jenkins
  timestamp: "2026-03-11T09:58:32Z"
  build_number: "14"
```

---

## Скриншоты

| Файл | Описание |
|---|---|
| `02-parallel-stages.png` | Параллельные стейджи тестирования в Jenkins |
| `03-gitops-deployer-success.png` | Успешный запуск HW34-GitOps-Deployer |
| `04-deploy-config-github.png` | deploy-config.yml обновлён Jenkins в GitHub |
| `05-dockerhub-tags.png` | Теги образов на DockerHub |
| `06-gitops-commit-history.png` | История коммитов Jenkins CI в HW34-deploy |

---

## Результат

- Приложение доступно на `http://localhost:5000`
- Каждый `git push` автоматически запускает полный цикл: сборка → тесты → публикация → деплой
- История деплоев зафиксирована в Git (коммиты от Jenkins CI)
- Реализован GitOps подход без Kubernetes на стеке Docker + Jenkins