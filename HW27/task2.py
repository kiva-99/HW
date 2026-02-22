import string  # Подключаем модуль со знаками пунктуации

# Запрашиваем строку у пользователя
text = input("Введите строку: ")

# Создаём счётчики (все начинаются с нуля)
upper_count = 0  # Буквы в ВЕРХНЕМ регистре (A, B, C...)
lower_count = 0  # Буквы в нижнем регистре (a, b, c...)
digit_count = 0  # Цифры (0, 1, 2...)
space_count = 0  # Пробелы (' ')
tab_count = 0    # Табуляции ('\t')
punct_count = 0  # Знаки пунктуации (!, ?, ., ,, и т.д.)

# Перебираем каждый символ в строке
for char in text:
    if char.isupper():          # Заглавная буква?
        upper_count += 1
    elif char.islower():        # Строчная буква?
        lower_count += 1
    elif char.isdigit():        # Цифра?
        digit_count += 1
    elif char == ' ':           # Пробел? (символ с кодом 32)
        space_count += 1
    elif char == '\t':          # Табуляция? (символ с кодом 9, создаётся клавишей Tab)
        tab_count += 1
    elif char in string.punctuation:  # Знак пунктуации?
        punct_count += 1

# Выводим результаты
print("\nРезультаты подсчёта:")
print(f"Буквы в верхнем регистре: {upper_count}")
print(f"Буквы в нижнем регистре: {lower_count}")
print(f"Цифры: {digit_count}")
print(f"Пробелы: {space_count}")
print(f"Табуляции: {tab_count}")
print(f"Знаки пунктуации: {punct_count}")