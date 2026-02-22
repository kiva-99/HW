from jinja2 import Template  # Импорт класса Template из установленной библиотеки Jinja2

# Шаг 1: Создаём список пользователей (список словарей)

users = [
    {"name": "Иван Иванов", "email": "ivan@example.com"},
    {"name": "Мария Петрова", "email": "maria@example.com"},
    {"name": "Алексей Сидоров", "email": "alexey@example.com"}
]

print("Создан список пользователей:")
for i, user in enumerate(users, 1):  
    print(f"   {i}. {user['name']} <{user['email']}>")

# Шаг 2: Загружаем шаблон из файла
print("\n Загружаем шаблон из файла template.html")
with open('template.html', 'r', encoding='utf-8') as file:  # encoding='utf-8' — обязательно для кириллицы!
    template_content = file.read()

# Шаг 3: Создаём объект шаблона
template = Template(template_content)
print(" Шаблон загружен")

# Шаг 4: Передаём данные в шаблон и получаем результат
# "template.render() — метод для подстановки данных в шаблон"
rendered_html = template.render(users=users)  # users=users: слева — имя в шаблоне, справа — переменная в Python

# Шаг 5: Выводим результат на экран
print("\n Сгенерированный HTML-код:")
print("=" * 60)
print(rendered_html)
print("=" * 60)

# Шаг 6 (бонус): Сохраняем результат в файл для просмотра в браузере
with open('result.html', 'w', encoding='utf-8') as file:
    file.write(rendered_html)
print("\n Результат сохранён в файл result.html")
print("Совет: Открой файл двойным кликом в Проводнике для просмотра в браузере!")