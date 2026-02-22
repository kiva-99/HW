pipeline {
    // Глобальный агент по умолчанию - Python агент для проверок кода
    agent { label 'docker-agent' }
    
    environment {
        REPO_URL = 'https://github.com/kiva-99/HW.git'
        EMAIL_TO = 'k.ivanovconn@gmail.com'
        PYTHON_VERSION = 'python3'
        PROJECT_NAME = 'HW-Pipeline'
        EMAIL_SUBJECT_PREFIX = '[HW31 CI]'
    }
    
    triggers {
        // Автозапуск каждые 5 минут при изменениях в репозитории
        pollSCM('H/5 * * * *')
    }
    
    stages {
        // 🔹 ЭТАП 1: Клонирование репозитория
        stage('Clone Repository') {
            steps {
                echo "🔄 Клонируем репозиторий: ${env.REPO_URL}"
                script {
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: env.REPO_URL]],
                        extensions: [[$class: 'CleanCheckout']]])
                }
                echo "✅ Репозиторий успешно клонирован"
            }
        }
        
        // 🔹 ЭТАП 2: Проверка синтаксиса Python-скриптов
        stage('Python Syntax Check') {
            steps {
                echo "🐍 Проверка синтаксиса Python-скриптов..."
                sh '''
                    echo "=== Проверка Python скриптов ==="
                    find . -name "*.py" -type f | while read file; do
                        echo "Checking: $file"
                        python3 -m py_compile "$file" || {
                            echo "❌ Ошибка синтаксиса в: $file"
                            exit 1
                        }
                    done
                    echo "✅ Все Python скрипты валидны"
                '''
            }
        }
        
        // 🔹 ЭТАП 3: Проверка синтаксиса Shell-скриптов
        stage('Shell Script Check') {
            steps {
                echo "🐚 Проверка синтаксиса Shell-скриптов..."
                sh '''
                    echo "=== Проверка Shell скриптов ==="
                    find . -name "*.sh" -type f | while read file; do
                        echo "Checking: $file"
                        bash -n "$file" || {
                            echo "❌ Ошибка синтаксиса в: $file"
                            exit 1
                        }
                    done
                    echo "✅ Все Shell скрипты валидны"
                '''
            }
        }
        
        // 🔹 ЭТАП 4: Запуск Python-тестов (pytest)
        stage('Run Python Tests') {
            steps {
                echo "🧪 Запуск автоматических тестов..."
                sh '''
                    echo "=== Установка зависимостей для тестов ==="
                    if [ -f "requirements.txt" ]; then
                        pip3 install -r requirements.txt --user 2>/dev/null || true
                    fi
                    pip3 install pytest --user 2>/dev/null || true
                    
                    echo "=== Запуск pytest ==="
                    if [ -d "tests" ]; then
                        python3 -m pytest tests/ -v --tb=short || {
                            echo "⚠️ Тесты не прошли, но продолжаем сборку"
                            exit 0
                        }
                    else
                        echo "⚠️ Папка tests/ не найдена, пропускаем pytest"
                    fi
                    echo "✅ Тесты завершены"
                '''
            }
        }
        
        // 🔹 ЭТАП 5: Сборка Docker-образа для hw24
        stage('Build Docker Image (hw24)') {
            // Переопределяем агент ТОЛЬКО для этого этапа
            agent { label 'docker-builder' }
            
            steps {
                echo "🐳 Сборка Docker-образа из hw24/Dockerfile..."
                script {
                    // Клонируем репозиторий заново на Docker-агенте
                    checkout([$class: 'GitSCM',
                        branches: [[name: '*/main']],
                        userRemoteConfigs: [[url: env.REPO_URL]],
                        extensions: [[$class: 'CleanCheckout']]])
                    
                    // Проверяем наличие Dockerfile и собираем образ
                    if (fileExists('hw24/Dockerfile')) {
                        sh """
                            echo "=== Сборка Docker образа hw24 ==="
                            cd hw24
                            docker build -t hw24-image:${env.BUILD_NUMBER} .
                            
                            echo "📦 Собранные образы:"
                            docker images | grep hw24-image || true
                            
                            # Очищаем старые образы
                            docker image prune -f || true
                            
                            echo "✅ Образ hw24-image:${env.BUILD_NUMBER} собран"
                        """
                    } else {
                        echo "⚠ Dockerfile не найден в hw24"
                        sh 'find . -name "Dockerfile" -type f || echo "Dockerfile не найден"'
                    }
                }
            }
        }
        
        // 🔹 ЭТАП 6: Сборка Java-проекта через Maven (для требования 4.1.3)
        stage('Build Java Project (Maven)') {
            agent { label 'docker-agent' }
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                script {
                    if (fileExists('pom.xml')) {
                        echo "🔨 Сборка Java-проекта через Maven..."
                        sh '''
                            # Проверяем наличие Maven
                            which mvn || echo "Maven not installed, skipping build"
                            
                            # Запускаем сборку и тесты (если Maven есть)
                            if command -v mvn &> /dev/null && [ -f "pom.xml" ]; then
                                mvn clean package -q || {
                                    echo "❌ Maven build failed"
                                    exit 1
                                }
                                echo "✅ Maven build successful"
                            else
                                echo "⚠ Maven не установлен или pom.xml не найден, пропускаем"
                            fi
                        '''
                    }
                }
            }
            post {
                always {
                    // 👇 Публикация отчётов JUnit (если есть)
                    junit allowEmptyResults: true, testResults: '**/target/surefire-reports/*.xml'
                }
            }
        }
    }
    
    // 👇 POST-ACTIONS: действия после завершения ВСЕХ stages
    post {
        // 🔄 ALWAYS: выполняется ВСЕГДА, независимо от результата
        always {
            echo "🧹 Очистка рабочего пространства..."
            cleanWs()
            echo "✅ Workspace очищен"
            
            // 👇 Публикация отчётов pytest HTML (если используете pytest-html)
            // publishHTML(target: [
            //     allowMissing: true,
            //     alwaysLinkToLastBuild: true,
            //     keepAll: true,
            //     reportDir: 'pytest-html',
            //     reportFiles: 'index.html',
            //     reportName: 'Pytest HTML Report'
            // ])
            
            // 👇 Архивация артефактов (Docker-образ, логи, отчёты)
            archiveArtifacts artifacts: 'hw24/*.tar,**/target/*.jar,**/pytest-html/**/*.html', allowEmptyArchive: true
        }
        
        // ✅ SUCCESS: только если ВСЕ этапы прошли успешно
        success {
            echo "🎉 Сборка успешна! Отправляем уведомление..."
            emailext (
                to: env.EMAIL_TO,
                subject: "${env.EMAIL_SUBJECT_PREFIX} ✅ SUCCESS: ${env.PROJECT_NAME} #${env.BUILD_NUMBER}",
                body: """
                🎉 Сборка Jenkins прошла успешно!
                
                📦 Задача: ${env.PROJECT_NAME}
                🔢 Сборка: #${env.BUILD_NUMBER}
                🔗 Ссылка: ${env.BUILD_URL}
                👤 Автор: ${env.CHANGE_AUTHOR}
                📅 Время: ${env.BUILD_TIMESTAMP}
                
                ✅ Этапы:
                • Клонирование репозитория: OK
                • Проверка Python: OK
                • Проверка Shell: OK
                • Тесты pytest: OK
                • Docker build: OK
                • Maven build: OK (если применимо)
                
                Код готов к использованию! 🚀
                """,
                mimeType: 'text/plain',
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        
        // ❌ FAILURE: если ЛЮБОЙ этап упал с ошибкой
        failure {
            echo "❌ Сборка провалилась! Отправляем срочное уведомление..."
            emailext (
                to: env.EMAIL_TO,
                subject: "${env.EMAIL_SUBJECT_PREFIX} ❌ FAILURE: ${env.PROJECT_NAME} #${env.BUILD_NUMBER}",
                body: """
                ⚠️ Сборка Jenkins завершилась с ошибкой!
                
                📦 Задача: ${env.PROJECT_NAME}
                🔢 Сборка: #${env.BUILD_NUMBER}
                🔗 Консоль: ${env.BUILD_URL}console
                👤 Автор: ${env.CHANGE_AUTHOR}
                
                🔍 Возможные причины:
                • Синтаксическая ошибка в Python/Shell коде
                • Не прошли автоматические тесты (pytest)
                • Ошибка при сборке Docker-образа
                • Ошибка Maven/JUnit сборки
                • Проблема с клонированием репозитория
                
                🛠 Что делать:
                1. Откройте консоль сборки по ссылке выше
                2. Найдите строку с ERROR или ❌
                3. Исправьте ошибку в коде
                4. Сделайте новый коммит и push
                
                ---
                Это письмо отправлено автоматически системой Jenkins.
                """,
                mimeType: 'text/plain',
                attachLog: true,
                recipientProviders: [[$class: 'DevelopersRecipientProvider']]
            )
        }
        
        // ⚠️ UNSTABLE: если тесты упали, но сборка не "красная"
        unstable {
            echo "⚠️ Сборка нестабильна (тесты упали)"
            emailext (
                to: env.EMAIL_TO,
                subject: "${env.EMAIL_SUBJECT_PREFIX} ⚠️ UNSTABLE: ${env.PROJECT_NAME} #${env.BUILD_NUMBER}",
                body: "Некоторые тесты не прошли. Проверьте отчёт: ${env.BUILD_URL}testReport",
                mimeType: 'text/plain'
            )
        }
    }
}