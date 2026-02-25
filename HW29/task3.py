# Задание 3: Класс "Студент"

class Student:
    # Конструктор класса - инициализирует объект при создании
    def __init__(self, name, age):
        self.name = name              # Имя студента
        self.age = age                # Возраст студента
        self.gpa = 0.0                # Средний балл (изначально 0)
        self.grades = []              # Список оценок для вычисления среднего
    
    # Метод для добавления оценок и вычисления среднего балла
    def calculate_gpa(self):
        # Проверяем, есть ли оценки
        if len(self.grades) > 0:
            # Суммируем все оценки и делим на их количество
            self.gpa = sum(self.grades) / len(self.grades)
            print(f"✅ Средний балл вычислен: {self.gpa:.2f}")
        else:
            print("❌ Нет оценок для вычисления среднего балла!")
    
    # Метод для определения статуса студента
    def get_status(self):
        # Проверяем, вычислен ли средний балл
        if self.gpa == 0.0 and len(self.grades) == 0:
            return "Статус не определен (нет оценок)"
        
        # Определяем статус по среднему баллу
        if self.gpa >= 4.5:
            return "Отличник"
        elif self.gpa >= 3.5:
            return "Хорошист"
        elif self.gpa >= 2.0:
            return "Троечник"
        else:
            return "Неудовлетворительно (отчислен)"
    
    # Метод для добавления оценки в список
    def add_grade(self, grade):
        # Проверяем, что оценка в допустимом диапазоне (2-5)
        if 2 <= grade <= 5:
            self.grades.append(grade)
            print(f"✅ Оценка {grade} добавлена!")
        else:
            print("❌ Оценка должна быть от 2 до 5!")
    
    # Метод для отображения информации о студенте
    def display_info(self):
        print(f"\n--- Информация о студенте ---")
        print(f"Имя: {self.name}")
        print(f"Возраст: {self.age} лет")
        print(f"Оценки: {self.grades}")
        print(f"Средний балл: {self.gpa:.2f}")
        print(f"Статус: {self.get_status()}")


# Основная часть программы
if __name__ == "__main__":
    print("=== Задание 3: Студент ===\n")
    
    students = []  # Список для хранения объектов студентов
    count = 2      # Количество студентов для создания
    
    # Создаем несколько объектов (студентов)
    for i in range(count):
        print(f"--- Создание студента №{i + 1} ---")
        
        # ЗАПРОС ДАННЫХ У ПОЛЬЗОВАТЕЛЯ (не хардкодим!)
        name = input("Введите имя студента: ")
        age = int(input("Введите возраст студента: "))
        
        # Создание объекта класса Student
        new_student = Student(name, age)
        students.append(new_student)
        
        # Запрашиваем оценки для студента
        print(f"\n--- Ввод оценок для {name} ---")
        num_grades = int(input("Сколько оценок хотите ввести? "))
        
        for j in range(num_grades):
            grade = float(input(f"Введите оценку №{j + 1} (2-5): "))
            new_student.add_grade(grade)
        
        # Вычисляем средний балл
        new_student.calculate_gpa()
        print(f"✅ Студент {name} создан!\n")
    
    # Вывод информации о каждом студенте
    for i, student in enumerate(students):
        print(f"\n=== Студент №{i + 1} ===")
        student.display_info()
    
    print("\n=== Все данные обработаны ===")