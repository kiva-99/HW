# HW33 - Jenkins Agent: Удалённый агент на Ubuntu VM

**Автор:** Иванов Кирилл Константинович

---

## Цель задания

Настроить удалённый Jenkins агент на виртуальной машине Ubuntu (VirtualBox),
создать Pipeline который выполняется на этом агенте, реализовать Jenkinsfile
в Git репозитории с отчётностью через JUnit.

---

## Архитектура решения

Jenkins Master (localhost:8080)
    |
    |  SSH соединение
    |  IP: 192.168.56.101, Port: 2222
    v
Ubuntu2 VM (pg2) - Jenkins Agent
    - Java 17 (для запуска agent.jar)
    - Docker 29.3.0 (для сборки и деплоя)
    - Git 2.43.0 (для клонирования репо)

---

## Что сделано

### 1. Настройка агента на Ubuntu VM

- ВМ: Ubuntu 24.04, hostname pg2
- Сеть: Host-Only адаптер 192.168.56.101
- SSH порт: 2222
- Установлено: Java 17, Docker, Git
- Создана папка агента: /home/roman/jenkins-agent
- Сгенерированы SSH ключи: ~/hw33-agent-keys/hw33-agent

### 2. Настройка Jenkins

- Добавлен Credential типа SSH Username with private key
  - ID: hw33-ubuntu-agent-key
  - Username: roman
- Создан Node ubuntu2-hw33-agent
  - Host: 192.168.56.101
  - Port: 2222
  - Label: ubuntu2-agent
  - Remote root: /home/roman/jenkins-agent

### 3. Jenkinsfile в Git

- Репозиторий: https://github.com/kiva-99/jenkins-pipelines
- Pipeline job: HW33-Ubuntu-Agent-Pipeline
- Тип: Pipeline from SCM

### 4. Этапы Pipeline

| Этап | Описание |
|------|----------|
| Agent Info | Вывод информации об агенте (hostname, java, docker, git) |
| Checkout Application | Клонирование репо HW с GitHub |
| Build Application | Сборка Docker образа hw33-webapp на убунту2 |
| Run Tests | Запуск pytest, генерация JUnit XML отчёта |
| Cleanup Old Containers | Удаление старых контейнеров |
| Deploy Application | Запуск контейнера на порту 8091 |
| Health Check | Проверка доступности приложения |
| Generate Report | Генерация JSON отчёта о сборке |

### 5. Отчётность (JUnit)

Pipeline генерирует test-results.xml и публикует его через
JUnit плагин Jenkins. В интерфейсе Jenkins отображается статистика тестов.

---

## Результаты

- Приложение задеплоено на Ubuntu2 VM: http://192.168.56.101:8091
- Все 3 теста прошли успешно
- Pipeline статус: SUCCESS

---

## Скриншоты

- screenshots/01-agent-connected.png - агент подключён в Jenkins
- screenshots/02-pipeline-success.png - успешный запуск pipeline
- screenshots/03-junit-report.png - JUnit отчёт о тестах
- screenshots/05-app-deployed.png - задеплоенное приложение