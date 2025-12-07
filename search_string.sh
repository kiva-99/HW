#!/bin/bash

# Проверяем количество аргументов
if [ $# -ne 2 ]; then
    echo "Использование: $0 <строка> <каталог>"
    exit 1
fi

search_str="$1"
catalog="$2"

# Проверяем, существует ли каталог и доступен ли он
if [ ! -d "$catalog" ]; then
    echo "Ошибка: каталог '$catalog' не существует"
    exit 1
fi

if [ ! -r "$catalog" ]; then
    echo "Нет доступа к каталогу '$catalog'"
    exit 1
fi

# Ищем все файлы в каталоге и подкаталогах
files=$(find "$catalog" -type f)

# Перебираем каждый файл
for file in $files; do
    # Проверим, можем ли мы его прочитать
    if [ ! -r "$file" ]; then
        echo "Нет доступа к файлу: $file"
        continue
    fi

    # Ищем строку в файле
    if grep -l "$search_str" "$file" > /dev/null; then
        # Строка найдена — выводим путь и размер
        size=$(stat -c %s "$file")
        echo "Файл: $file, Размер: $size байт"
    fi
done
