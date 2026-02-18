import json           # Для чтения JSON конфигурации
import subprocess     # Для выполнения системных команд
import platform       # Для определения операционной системы
import datetime       # Для метки времени в отчете
import os             # Для работы с путями


class ServiceMonitor:
    """
    Класс для мониторинга состояния сервисов.
    
    Атрибуты:
        config_file (str): Путь к JSON файлу с конфигурацией
        services (list): Список сервисов для проверки
        results (list): Результаты проверок
    """
    
    def __init__(self, config_file):
        """
        Конструктор класса.
        
        Аргументы:
            config_file (str): Путь к JSON файлу с конфигурацией сервисов
        """
        self.config_file = config_file
        self.services = []
        self.results = []
        
        # Загружаем конфигурацию при создании объекта
        self._load_config()
    
    def _load_config(self):
        """
        Приватный метод для загрузки конфигурации из JSON файла.
        """
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.services = config.get('services', [])
                print(f"Загружено {len(self.services)} сервисов из {self.config_file}")
        except FileNotFoundError:
            print(f" Ошибка: Файл конфигурации '{self.config_file}' не найден!")
            self.services = []
        except json.JSONDecodeError as e:
            print(f" Ошибка: Неверный формат JSON в {self.config_file}: {e}")
            self.services = []
    
    def check_service_status(self, service_name):
        """
        Проверяет состояние сервиса.
        
        Аргументы:
            service_name (str): Имя сервиса для проверки
        
        Возвращает:
            dict: {'name': имя, 'status': 'UP'/'DOWN', 'time': время проверки}
        """
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Определяем операционную систему
        os_name = platform.system()
        
        try:
            if os_name == "Windows":
                # === WINDOWS: используем PowerShell Get-Service ===
                # Команда: Get-Service -Name "serviceName" | Select-Object -ExpandProperty Status
                command = [
                    "powershell",
                    "-Command",
                    f"Get-Service -Name '{service_name}' -ErrorAction Stop | Select-Object -ExpandProperty Status"
                ]
            else:
                # === LINUX: используем systemctl ===
                command = ["systemctl", "is-active", service_name]
            
            # Выполняем команду
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=10  # Таймаут 10 секунд
            )
            
            # Анализируем результат
            if os_name == "Windows":
                # На Windows статус 'Running' = UP
                status = "UP" if result.stdout.strip() == "Running" else "DOWN"
            else:
                # На Linux статус 'active' = UP
                status = "UP" if result.returncode == 0 else "DOWN"
            
        except subprocess.TimeoutExpired:
            print(f"  Таймаут при проверке сервиса '{service_name}'")
            status = "DOWN"
        except Exception as e:
            print(f"  Ошибка проверки '{service_name}': {e}")
            status = "DOWN"
        
        # Формируем результат
        service_result = {
            'name': service_name,
            'status': status,
            'time': current_time
        }
        
        return service_result
    
    def generate_report(self, output_file="service_status_report.txt"):
        """
        Генерирует отчет о состоянии всех сервисов и сохраняет в файл.
        
        Аргументы:
            output_file (str): Имя файла для сохранения отчета
        
        Возвращает:
            int: Количество проверенных сервисов
        """
        if not self.services:
            print(" Нет сервисов для проверки!")
            return 0
        
        print(f"\n Начинаю проверку {len(self.services)} сервисов...")
        print("=" * 50)
        
        self.results = []
        
        # Проверяем каждый сервис
        for service in self.services:
            service_name = service.get('name', 'unknown')
            result = self.check_service_status(service_name)
            self.results.append(result)
            
            # Выводим статус в консоль
            status_icon = "ok" if result['status'] == "UP" else "not ok"
            print(f"   {status_icon} {result['name']}: {result['status']}")
        
        print("=" * 50)
        
        # Генерируем текстовый отчет
        report_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report_content = []
        report_content.append("=" * 60)
        report_content.append("ОТЧЕТ О СОСТОЯНИИ СЕРВИСОВ")
        report_content.append(f"Время генерации: {report_time}")
        report_content.append("=" * 60)
        report_content.append("")
        report_content.append(f"{'№':<4} {'Сервис':<20} {'Статус':<10} {'Время проверки'}")
        report_content.append("-" * 60)
        
        up_count = 0
        down_count = 0
        
        for i, result in enumerate(self.results, 1):
            report_content.append(
                f"{i:<4} {result['name']:<20} {result['status']:<10} {result['time']}"
            )
            if result['status'] == "UP":
                up_count += 1
            else:
                down_count += 1
        
        report_content.append("-" * 60)
        report_content.append(f"ВСЕГО: {len(self.results)} | UP: {up_count} | DOWN: {down_count}")
        report_content.append("=" * 60)
        
        # Записываем отчет в файл
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(report_content))
            
            print(f"\n Отчет сохранен в файл: {output_file}")
            print(f" Итого: {up_count} UP, {down_count} DOWN")
            
        except Exception as e:
            print(f" Ошибка записи отчета: {e}")
            return 0
        
        return len(self.results)


def main():
    """
    Главная функция. Запускает мониторинг сервисов.
    """
    import argparse
    
    parser = argparse.ArgumentParser(
        description="ServiceMonitor — мониторинг состояния сервисов"
    )
    
    parser.add_argument(
        "--config",
        default="services.json",
        help="Путь к JSON файлу конфигурации (по умолчанию: services.json)"
    )
    
    parser.add_argument(
        "--output",
        default="service_status_report.txt",
        help="Имя файла отчета (по умолчанию: service_status_report.txt)"
    )
    
    args = parser.parse_args()
    
    # Создаем объект ServiceMonitor
    monitor = ServiceMonitor(config_file=args.config)
    
    # Генерируем отчет
    monitor.generate_report(output_file=args.output)


if __name__ == "__main__":
    main()