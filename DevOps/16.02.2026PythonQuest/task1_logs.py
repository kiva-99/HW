# 1. Исходные данные (список строк логов)
logs = [
    "INFO: Service started",
    "ERROR: Connection timeout",
    "WARNING: CPU usage high",
    "ERROR: Disk full",
    "INFO: Health check passed",
    "ERROR: Out of memory"
]

# 2. Фильтруем только ошибки
error_logs = [log for log in logs if "ERROR" in log]

# 3. Считаем количество ошибок
errors_count = len(error_logs)

# 4. Выводим список ошибок (для наглядности)
print("Список ошибок:", error_logs)
print("Количество ошибок:", errors_count)

# 5. Принимаем решение
if errors_count > 2:
    print("Срочно чиним прод!")
else:
    print("Пока держимся")