# Задание 5: Класс "Автомобиль"

class Car:
    # Конструктор класса - инициализирует объект при создании
    def __init__(self, brand, model, color, year):
        self.__brand = brand    # Приватный атрибут (инкапсуляция)
        self.__model = model    # Защита от прямого изменения
        self.__color = color    # Двойное подчёркивание = private
        self.__year = year      # Инкапсуляция 
    
    # ===== GETTERS (методы для получения данных) =====
    
    def get_brand(self):
        """Возвращает марку автомобиля"""
        return self.__brand
    
    def get_model(self):
        """Возвращает модель автомобиля"""
        return self.__model
    
    def get_color(self):
        """Возвращает цвет автомобиля"""
        return self.__color
    
    def get_year(self):
        """Возвращает год выпуска автомобиля"""
        return self.__year
    
    # ===== SETTERS (методы для изменения данных) =====
    
    def set_brand(self, new_brand):
        """Изменяет марку автомобиля с проверкой"""
        if len(new_brand) > 0:  # Проверка: марка не пустая
            self.__brand = new_brand
            print(f"✅ Марка изменена на: {self.__brand}")
        else:
            print("❌ Марка автомобиля не может быть пустой!")
    
    def set_model(self, new_model):
        """Изменяет модель автомобиля с проверкой"""
        if len(new_model) > 0:  # Проверка: модель не пустая
            self.__model = new_model
            print(f"✅ Модель изменена на: {self.__model}")
        else:
            print("❌ Модель автомобиля не может быть пустой!")
    
    def set_color(self, new_color):
        """Изменяет цвет автомобиля с проверкой"""
        if len(new_color) > 0:  # Проверка: цвет не пустой
            self.__color = new_color
            print(f"✅ Цвет изменён на: {self.__color}")
        else:
            print("❌ Цвет автомобиля не может быть пустым!")
    
    def set_year(self, new_year):
        """Изменяет год выпуска с проверкой"""
        # Проверка: год должен быть в разумных пределах
        # 1886 - год создания первого автомобиля (Karl Benz)
        if 1886 <= new_year <= 2025:
            self.__year = new_year
            print(f"✅ Год выпуска изменён на: {self.__year}")
        else:
            print(f"❌ Недопустимый год! Введите год от 1886 до 2025")
    
    # Метод для отображения информации об автомобиле
    def display_info(self):
        print(f"\n--- Информация об автомобиле ---")
        print(f"Марка: {self.get_brand()}")
        print(f"Модель: {self.get_model()}")
        print(f"Цвет: {self.get_color()}")
        print(f"Год выпуска: {self.get_year()}")


# Основная часть программы
if __name__ == "__main__":
    print("=== Задание 5: Автомобиль ===\n")
    
    cars = []  # Список для хранения объектов автомобилей
    count = 2  # Количество автомобилей для создания
    
    # Создаем несколько объектов (автомобилей)
    for i in range(count):
        print(f"--- Создание автомобиля №{i + 1} ---")
        
        # ЗАПРОС ДАННЫХ У ПОЛЬЗОВАТЕЛЯ (не хардкодим!)
        brand = input("Введите марку автомобиля: ")
        model = input("Введите модель автомобиля: ")
        color = input("Введите цвет автомобиля: ")
        year = int(input("Введите год выпуска: "))
        
        # Создание объекта класса Car
        new_car = Car(brand, model, color, year)
        cars.append(new_car)
        print(f"✅ Автомобиль '{brand} {model}' создан!\n")
    
    # Работа с каждым автомобилем: просмотр и изменение данных
    for i, car in enumerate(cars):
        print(f"\n=== Автомобиль №{i + 1} ===")
        
        # Показываем текущую информацию
        car.display_info()
        
        # Спрашиваем, хочет ли пользователь изменить данные
        print("\n--- Хотите изменить данные автомобиля? ---")
        change = input("Введите 'да' для изменения или любой ключ для пропуска: ")
        
        if change.lower() == 'да':
            # Изменение марки
            print("\n--- Изменение марки ---")
            new_brand = input("Введите новую марку (или оставьте пустым для пропуска): ")
            if new_brand:
                car.set_brand(new_brand)  # Вызов setter
            
            # Изменение модели
            print("\n--- Изменение модели ---")
            new_model = input("Введите новую модель (или оставьте пустым для пропуска): ")
            if new_model:
                car.set_model(new_model)  # Вызов setter
            
            # Изменение цвета
            print("\n--- Изменение цвета ---")
            new_color = input("Введите новый цвет (или оставьте пустым для пропуска): ")
            if new_color:
                car.set_color(new_color)  # Вызов setter
            
            # Изменение года
            print("\n--- Изменение года ---")
            year_input = input("Введите новый год (или оставьте пустым для пропуска): ")
            if year_input:
                car.set_year(int(year_input))  # Вызов setter
        
        # Показываем итоговую информацию
        print("\n--- Итоговое состояние ---")
        car.display_info()
    
    print("\n=== Все операции завершены ===")
   
