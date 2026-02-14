import subprocess

# Список IP-адресов для проверки
ips = ["8.8.8.8", "1.1.1.1", "192.168.1.1", "10.255.255.1", "127.0.0.1"]

# Открываем файл для записи результатов
with open("ping_results.txt", "w",encoding="utf-8") as file:
    # Проверяем каждый IP из списка
    for ip in ips:
        print(f"Проверяю {ip}...")
        
        # Выполняем команду: ping -n 1 <ip> (1 запрос в Windows)
        result = subprocess.run(["ping", "-n", "1", ip], capture_output=True)
        
        # Если код возврата 0 — хост доступен
        if result.returncode == 0:
            status = "ДОСТУПЕН"
        else:
            status = "НЕДОСТУПЕН"
        
        # Выводим на экран и записываем в файл
        print(f"  {ip} — {status}")
        file.write(f"{ip} — {status}\n")

print("\nГотово! Результаты сохранены в файле: ping_results.txt")