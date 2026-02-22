import argparse
import os
import tarfile
import datetime
import sys
import time


class LogManager:
    """
    Класс для управления логами: сбор, архивация и очистка старых архивов.
    
    Атрибуты:
        source_dir (str): Путь к папке с исходными логами
        dest_dir (str): Путь к папке для архивов
        retention_days (int): Сколько дней хранить архивы
    """
    
    def __init__(self, source_dir, dest_dir, retention_days=7):
        """
        Конструктор класса — вызывается при создании объекта.
        
        Аргументы:
            source_dir (str): Путь к папке с логами
            dest_dir (str): Путь к папке для бэкапов
            retention_days (int): Количество дней хранения архивов (по умолчанию 7)
        """
        self.source_dir = source_dir
        self.dest_dir = dest_dir
        self.retention_days = retention_days
        
        print(f"LogManager инициализирован:")
        print(f"Источник: {self.source_dir}")
        print(f"Бэкапы: {self.dest_dir}")
        print(f"Хранение: {self.retention_days} дн.")
        print()
    
    def collect_logs(self):
        """
        Метод для сбора и архивации всех .log файлов.
        Возвращает True если успешно, False если ошибка.
        """
        # 1. Проверка существования исходной директории
        if not os.path.exists(self.source_dir):
            print(f"Ошибка: Директория '{self.source_dir}' не существует!")
            return False
        
        if not os.path.isdir(self.source_dir):
            print(f"Ошибка: '{self.source_dir}' не является директорией!")
            return False
        
        # 2. Поиск всех .log файлов
        all_files = os.listdir(self.source_dir)
        log_files = [f for f in all_files if f.endswith('.log')]
        
        # 3. Проверка наличия файлов
        if not log_files:
            print(f"Предупреждение: В директории '{self.source_dir}' нет файлов .log")
            return False
        
        # 4. Создание имени архива с меткой времени
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"logs_{timestamp}.tar.gz"
        archive_path = os.path.join(self.dest_dir, archive_name)
        
        # 5. Создание директории для бэкапов если не существует
        if not os.path.exists(self.dest_dir):
            print(f" Директория '{self.dest_dir}' не найдена. Создаем её...")
            os.makedirs(self.dest_dir)
        
        # 6. Создание архива
        print(f" Начинаю архивацию {len(log_files)} файлов...")
        
        try:
            with tarfile.open(archive_path, "w:gz") as tar:
                for log_file in log_files:
                    file_path = os.path.join(self.source_dir, log_file)
                    tar.add(file_path, arcname=log_file)
                    print(f" Добавлен: {log_file}")
            
            # 7. Получение размера архива
            archive_size = os.path.getsize(archive_path)
            
            # 8. Вывод информации
            print("\n" + "="*40)
            print("Архивация успешно завершена!")
            print(f"Имя архива: {archive_name}")
            print(f"Файлов архивировано: {len(log_files)}")
            print(f"Размер архива: {archive_size} байт")
            print(f"Путь: {archive_path}")
            print("="*40 + "\n")
            
            return True
            
        except Exception as e:
            print(f"Ошибка при создании архива: {e}")
            return False
    
    def cleanup_old_archives(self):
        """
        Метод для удаления старых архивов.
        Удаляет файлы .tar.gz старше retention_days дней.
        Возвращает количество удаленных файлов.
        """
        # 1. Проверка существования директории с архивами
        if not os.path.exists(self.dest_dir):
            print(f" Директория '{self.dest_dir}' не существует. Нечего очищать.")
            return 0
        
        # 2. Получение текущего времени
        current_time = time.time()
        
        # 3. Расчет порога возраста в секундах
        # retention_days * 24 часа * 60 минут * 60 секунд
        age_threshold = self.retention_days * 24 * 60 * 60
        
        # 4. Поиск всех архивов .tar.gz
        all_files = os.listdir(self.dest_dir)
        archive_files = [f for f in all_files if f.endswith('.tar.gz')]
        
        if not archive_files:
            print(f" В директории '{self.dest_dir}' нет архивов .tar.gz")
            return 0
        
        print(f" Начинаю очистку архивов старше {self.retention_days} дн....")
        print(f"   Найдено архивов: {len(archive_files)}")
        
        deleted_count = 0
        kept_count = 0
        
        # 5. Проверка каждого архива
        for archive_name in archive_files:
            archive_path = os.path.join(self.dest_dir, archive_name)
            
            # Получаем время последней модификации файла
            file_mtime = os.path.getmtime(archive_path)
            
            # Вычисляем возраст файла в секундах
            file_age = current_time - file_mtime
            
            # 6. Сравнение с порогом
            if file_age > age_threshold:
                # Файл старше порога — удаляем
                try:
                    os.remove(archive_path)
                    print(f" Удален: {archive_name} (возраст: {int(file_age / 86400)} дн.)")
                    deleted_count += 1
                except Exception as e:
                    print(f" Ошибка удаления {archive_name}: {e}")
            else:
                # Файл молодой — оставляем
                print(f" Сохранен: {archive_name} (возраст: {int(file_age / 86400)} дн.)")
                kept_count += 1
        
        # 7. Итоговый отчет
        print("\n" + "="*40)
        print(" Очистка завершена!")
        print(f"  Удалено архивов: {deleted_count}")
        print(f" Сохранено архивов: {kept_count}")
        print("="*40 + "\n")
        
        return deleted_count


def main():
    """
    Главная функция. Парсит аргументы и управляет LogManager.
    """
    parser = argparse.ArgumentParser(
        description="LogManager — сбор, архивация и очистка логов"
    )
    
    parser.add_argument(
        "--source", 
        required=True, 
        help="Путь к директории с логами"
    )
    
    parser.add_argument(
        "--dest", 
        required=True, 
        help="Путь к директории для бэкапов"
    )
    
    parser.add_argument(
        "--retention", 
        type=int, 
        default=7, 
        help="Количество дней хранения архивов (по умолчанию 7)"
    )
    
    parser.add_argument(
        "--cleanup-only", 
        action="store_true", 
        help="Только очистка старых архивов (без архивации)"
    )
    
    args = parser.parse_args()
    
    # Создаем объект LogManager
    log_manager = LogManager(
        source_dir=args.source,
        dest_dir=args.dest,
        retention_days=args.retention
    )
    
    # Если только очистка — не архивируем
    if not args.cleanup_only:
        log_manager.collect_logs()
    
    # Всегда выполняем очистку
    log_manager.cleanup_old_archives()
    
    sys.exit(0)


if __name__ == "__main__":
    main()