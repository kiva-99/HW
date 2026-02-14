numbers_str = input("Введите числа через пробел: ")
parts = numbers_str.split()      # ['5', '2', '8']
numbers = []                     # пустой список

for part in parts:
    number = int(part)           # преобразуем текст в число
    numbers.append(number)       # добавляем в список

numbers.sort(reverse=True)
print("\nОтсортированный список (по убыванию):")
print(numbers)