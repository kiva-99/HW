# Задание 3: Работа с директориями и файлами
import os  # Модуль для работы с операционной системой

# Шаг 1: Создаём пустую директорию mydir
if not os.path.exists('mydir'):
    os.mkdir('mydir')
    print("Директория 'mydir' создана")
else:
    print("Директория 'mydir' уже существует")

# Шаг 2: Переходим в директорию mydir
os.chdir('mydir')
print(f" Текущая директория: {os.getcwd()}")

# Шаг 3: Создаём три пустых файла
filenames = ['file1.txt', 'file2.txt', 'file3.txt']  
for filename in filenames:
    with open(filename, 'w', encoding='utf-8') as f:
        pass  # pass = ничего не делать (файл создаётся пустым)
    print(f" Файл '{filename}' создан")

# Шаг 4: Выводим список файлов в директории
files_in_dir = os.listdir('.')
print("\n Список файлов в директории 'mydir':")
for file in files_in_dir:
    print(f"  - {file}")

# Шаг 5: Возвращаемся в исходную директорию (опционально, но хорошая практика)
os.chdir('..')
print(f"\n Вернулись в директорию: {os.getcwd()}")