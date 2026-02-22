# Запрашиваем первый список
list1_str = input("Введите первый список (элементы через пробел): ")
list1 = list1_str.split()

# Запрашиваем второй список
list2_str = input("Введите второй список (элементы через пробел): ")
list2 = list2_str.split()

# ШАГ 1: Находим общие элементы (с возможными дубликатами)
# Перебираем каждый элемент первого списка
common_with_duplicates = []
for element in list1:
    if element in list2:
        common_with_duplicates.append(element)

# ШАГ 2: Убираем дубликаты, сохраняя порядок первого вхождения
unique_common = []
for element in common_with_duplicates:
    if element not in unique_common:  # Если элемента ещё нет в списке уникальных
        unique_common.append(element)

# Выводим результаты
print("\nОбщие элементы (с дубликатами):")
print(common_with_duplicates)

print("\nУникальные общие элементы (без дубликатов):")
if unique_common:
    for elem in unique_common:
        print(f"  - {elem}")
else:
    print("  Нет общих элементов")