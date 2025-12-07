#!/bin/bash

# Проверяем, передан ли аргумент
if [ $# -ne 1 ]; then
    echo "Использование: $0 <каталог>"
    exit 1
fi

catalog="$1"

# Проверим, существует ли каталог
if [ ! -d "$catalog" ]; then
    echo "Ошибка: '$catalog' не является каталогом или не существует"
    exit 1
fi

# Получаем список всех файлов
files=$(find "$catalog" -type f)

# Проходим по каждому файлу с помощью for
for file in $files; do
    # Выводим права доступа и размер с помощью ls -l
    ls -l "$file"
done
