# Задание 2: Работа с файлами
# Создание и запись в файл

# Шаг 1: Создаём файл и записываем строку
with open('test.txt', 'w', encoding='utf-8') as file:
    file.write("Это тестовый файл для домашнего задания по программированию")

print("Файл test.txt создан и записан")

# Шаг 2: Открываем файл для чтения
with open('test.txt', 'r', encoding='utf-8') as file:
    content = file.read()

print("Содержимое файла:")
print(content)