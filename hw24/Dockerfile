# STAGE 1: Базовый образ
FROM nginx:alpine

# Метаданные образа (кто собрал, для чего)
LABEL maintainer="roman" \
      hw="HW-24" \
      description="Custom Nginx image with persistent volumes"

# Копируем наш HTML-файл ВНУТРЬ образа (станет частью образа)
COPY index.html /usr/share/nginx/html/index.html

# Добавляем файл-маркер для демонстрации работы тома
RUN echo "Этот файл СОЗДАН ПРИ СБОРКЕ образа (внутри образа)" > /usr/share/nginx/html/build-marker.txt

# Переменные окружения (как в продакшене)
ENV APP_ENV=production \
    APP_NAME="hw24-nginx"

# Порт, который слушает приложение (документация для Docker)
EXPOSE 80

# Точка входа остаётся от базового образа nginx:alpine
# ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["nginx", "-g", "daemon off;"]