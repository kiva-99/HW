# Задание 4: Класс "Книга"

class Book:
    # Конструктор класса - инициализирует объект при создании
    def __init__(self, title, author, year):
        self.__title = title    # Двойное подчёркивание = приватный атрибут
        self.__author = author  # Защита от прямого изменения
        self.__year = year      # Инкапсуляция 
    
    # ===== GETTERS (методы для получения данных) =====
    
    def get_title(self):
        """Возвращает название книги"""
        return self.__title
    
    def get_author(self):
        """Возвращает автора книги"""
        return self.__author
    
    def get_year(self):
        """Возвращает год издания книги"""
        return self.__year
    
    # ===== SETTERS (методы для изменения данных) =====
    
    def set_title(self, new_title):
        """Изменяет название книги с проверкой"""
        if len(new_title) > 0:  # Проверка: название не пустое
            self.__title = new_title
            print(f"✅ Название изменено на: {self.__title}")
        else:
            print("❌ Название книги не может быть пустым!")
    
    def set_author(self, new_author):
        """Изменяет автора книги с проверкой"""
        if len(new_author) > 0:  # Проверка: автор не пустой
            self.__author = new_author
            print(f"✅ Автор изменён на: {self.__author}")
        else:
            print("❌ Имя автора не может быть пустым!")
    
    def set_year(self, new_year):
        """Изменяет год издания с проверкой"""
        # Проверка: год должен быть в разумных пределах
        if 1400 <= new_year <= 2025:
            self.__year = new_year
            print(f"✅ Год издания изменён на: {self.__year}")
        else:
            print(f"❌ Недопустимый год! Введите год от 1400 до 2025")
    
    # Метод для отображения информации о книге
    def display_info(self):
        print(f"\n--- Информация о книге ---")
        print(f"Название: {self.get_title()}")
        print(f"Автор: {self.get_author()}")
        print(f"Год издания: {self.get_year()}")


# Основная часть программы
if __name__ == "__main__":
    print("=== Задание 4: Книга ===\n")
    
    books = []  # Список для хранения объектов книг
    count = 2   # Количество книг для создания
    
    # Создаем несколько объектов (книг)
    for i in range(count):
        print(f"--- Создание книги №{i + 1} ---")
        
        # ЗАПРОС ДАННЫХ У ПОЛЬЗОВАТЕЛЯ (не хардкодим!)
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year = int(input("Введите год издания: "))
        
        # Создание объекта класса Book
        new_book = Book(title, author, year)
        books.append(new_book)
        print(f"✅ Книга '{title}' создана!\n")
    
    # Работа с каждой книгой: просмотр и изменение данных
    for i, book in enumerate(books):
        print(f"\n=== Книга №{i + 1} ===")
        
        # Показываем текущую информацию
        book.display_info()
        
        # Спрашиваем, хочет ли пользователь изменить данные
        print("\n--- Хотите изменить данные книги? ---")
        change = input("Введите 'да' для изменения или любой ключ для пропуска: ")
        
        if change.lower() == 'да':
            # Изменение названия
            print("\n--- Изменение названия ---")
            new_title = input("Введите новое название (или оставьте пустым для пропуска): ")
            if new_title:
                book.set_title(new_title)  # Вызов setter
            
            # Изменение автора
            print("\n--- Изменение автора ---")
            new_author = input("Введите нового автора (или оставьте пустым для пропуска): ")
            if new_author:
                book.set_author(new_author)  # Вызов setter
            
            # Изменение года
            print("\n--- Изменение года ---")
            year_input = input("Введите новый год (или оставьте пустым для пропуска): ")
            if year_input:
                book.set_year(int(year_input))  # Вызов setter
        
        # Показываем итоговую информацию
        print("\n--- Итоговое состояние ---")
        book.display_info()
    
    print("\n=== Все операции завершены ===")