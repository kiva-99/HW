import argparse       # Для обработки аргументов командной строки
import os             # Для работы с путями и файлами
import tarfile        # Для создания архивов .tar.gz
import datetime       # Для получения текущего времени (метки времени)
import sys            # Для корректного завершения программы при ошибках


def collect_and_archive_logs(source_dir, dest_dir):
    """
    Функция собирает все .log файлы из source_dir и архивирует их в dest_dir.
    
    Аргументы:
        source_dir (str): Путь к папке с логами.
        dest_dir (str): Путь к папке для сохранения архива.
    """
    
    # 1. Проверка: существует ли исходная директория
    if not os.path.exists(source_dir):
        print(f" Ошибка: Директория '{source_dir}' не существует!")
        return False
    
    if not os.path.isdir(source_dir):
        print(f" Ошибка: '{source_dir}' не является директорией!")
        return False

    # 2. Поиск всех .log файлов в директории
    # os.listdir() возвращает список всех файлов в папке
    all_files = os.listdir(source_dir)
    log_files = [f for f in all_files if f.endswith('.log')]
    
    # 3. Проверка: есть ли файлы для архивации
    if not log_files:
        print(f" Предупреждение: В директории '{source_dir}' нет файлов .log")
        return False

    # 4. Создаем имя архива с меткой времени
    # Формат: logs_ГГГГММДД_ЧЧММСС.tar.gz
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"logs_{timestamp}.tar.gz"
    
    # Полный путь к будущему архиву
    archive_path = os.path.join(dest_dir, archive_name)

    # 5. Проверка: существует ли директория для бэкапов
    # Если нет — создаем её (os.makedirs создает папку, если её нет)
    if not os.path.exists(dest_dir):
        print(f"ℹ️  Директория '{dest_dir}' не найдена. Создаем её...")
        os.makedirs(dest_dir)

    # 6. Создание архива
    print(f"Начинаю архивацию {len(log_files)} файлов...")
    
    try:
        # Открываем архив для записи ('w:gz' означает запись с gzip сжатием)
        with tarfile.open(archive_path, "w:gz") as tar:
            for log_file in log_files:
                # Полный путь к файлу лога
                file_path = os.path.join(source_dir, log_file)
                # Добавляем файл в архив (arcname сохраняет только имя файла без пути)
                tar.add(file_path, arcname=log_file)
                print(f" Добавлен: {log_file}")
        
        # 7. Получаем размер созданного архива
        archive_size = os.path.getsize(archive_path)
        
        # 8. Выводим итоговую информацию
        print("\n" + "="*40)
        print("Архивация успешно завершена!")
        print(f"Имя архива: {archive_name}")
        print(f"Файлов архивировано: {len(log_files)}")
        print(f"Размер архива: {archive_size} байт")
        print(f"Путь: {archive_path}")
        print("="*40 + "\n")
        
        return True
        
    except Exception as e:
        # Обработка непредвиденных ошибок при записи
        print(f"❌ Ошибка при создании архива: {e}")
        return False


def main():
    """
    Главная функция. Настраивает аргументы командной строки и запускает логику.
    """
    # Создаем парсер аргументов
    parser = argparse.ArgumentParser(
        description="Сбор и архивирование логов"
    )
    
    # Добавляем аргумент --source (обязательный)
    parser.add_argument(
        "--source", 
        required=True, 
        help="Путь к директории с логами"
    )
    
    # Добавляем аргумент --dest (обязательный)
    parser.add_argument(
        "--dest", 
        required=True, 
        help="Путь к директории для бэкапов"
    )
    
    # Парсим аргументы (превращаем текст команды в переменные Python)
    args = parser.parse_args()
    
    # Запускаем функцию сбора логов
    success = collect_and_archive_logs(args.source, args.dest)
    
    # Завершаем программу с кодом 0 (успех) или 1 (ошибка)
    # Это важно для автоматизации и CI/CD
    sys.exit(0 if success else 1)


# Эта конструкция гарантирует, что код выполнится только при прямом запуске скрипта
if __name__ == "__main__":
    main()