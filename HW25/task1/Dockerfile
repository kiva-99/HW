# Шаг 1: Базовый образ Ubuntu 20.04
# FROM — ВСЕГДА первая инструкция 
FROM ubuntu:20.04

# Шаг 2: Метаданные (опционально, но полезно для документирования)
LABEL maintainer="roman"

# Шаг 3: Установка nginx и curl
# RUN — выполняет команды внутри контейнера
# && — объединяем команды в ОДИН слой 
# --no-install-recommends — уменьшаем размер образа
# apt-get clean + rm -rf /var/lib/apt/lists/* — очищаем кэш (важно для уменьшения размера!)
RUN apt-get update && apt-get install -y --no-install-recommends nginx curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Шаг 4: Создание каталога для статики
# mkdir -p — создаёт всю цепочку директорий, если не существует
RUN mkdir -p /app/static

# Шаг 5: Копирование конфигурации nginx
# COPY — копирует файлы с хоста в контейнер
# nginx.conf → /etc/nginx/conf.d/default.conf (стандартное место для кастомных конфигов)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Шаг 6: Копирование статических файлов
# Обратите внимание: копируем СОДЕРЖИМОЕ папки (слэш на конце!)
COPY app/static/ /app/static/

# Шаг 7: Декларация порта
# EXPOSE — документирует намерение использовать порт 8080
# Реальное открытие произойдёт при запуске через -p 8080:8080
EXPOSE 8080

# Шаг 8: Запуск nginx в foreground-режиме
# ВАЖНО: "daemon off" — иначе nginx запустится как демон и контейнер завершится!
# CMD — ВСЕГДА последняя инструкция 
CMD ["nginx", "-g", "daemon off;"]
