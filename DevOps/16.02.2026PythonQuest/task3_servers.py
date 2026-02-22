# task3_servers.py

# 1. Исходные данные (список кортежей: имя, статус)
# Обратите внимание: я добавил запятую между предпоследним и последним элементом!
servers = [
    ("web-1", "online"),
    ("web-2", "offline"),
    ("db-1", "online"),
    ("cache-1", "offline"),
    ("cache-2", "offline") 
]

# 2. Выводим только имена серверов со статусом "offline"
# Распаковываем кортеж сразу в цикле: name, status
offline_servers = [name for name, status in servers if status == "offline"]

# 3. Считаем количество онлайн серверов
online_count = sum(1 for name, status in servers if status == "online")

# Вывод промежуточных результатов
print("Оффлайн серверы:", offline_servers)
print("Количество онлайн серверов:", online_count)

# 4. Проверка риска
if online_count < 2:
    print("Риск падения сервиса!")
else:
    print("Сервис стабилен")