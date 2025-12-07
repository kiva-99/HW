#!/bin/bash

# Проверим, что передано ровно 3 аргумента
if [ $# -ne 3 ]; then
    echo "Использование: $0 <файл_результата> <каталог> <расширение>"
    exit 1
fi

output_file="$1"
search_dir="$2"
extension="$3"

# Ищем файлы с указанным расширением и записываем их имена в файл
find "$search_dir" -type f -name "*.$extension" > "$output_file"

# Дополнительно: выведем в консоль, что нашли
echo "Найденные файлы записаны в $output_file:"
cat "$output_file"
