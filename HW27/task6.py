import os  # Модуль для работы с файловой системой

# Запрашиваем подстроку для поиска
substring = input("Введите подстроку для поиска в именах файлов: ")

# Получаем список всех элементов в текущей директории
all_items = os.listdir('.')

# Создаём пустой список для найденных файлов
found_files = []

# Перебираем каждый элемент в директории
for item in all_items:
    # Проверяем: это файл (не папка)?
    if os.path.isfile(item):
        # Проверяем: содержится ли подстрока в имени файла?
        # .lower() делает поиск РЕГИСТРОНЕЗАВИСИМЫМ (например, "TASK" найдёт "task1.py")
        if substring.lower() in item.lower():
            found_files.append(item)

# Выводим результаты
print("\nНайденные файлы:")
if found_files:
    for filename in found_files:
        print(f"  - {filename}")
else:
    print("  Файлы не найдены")