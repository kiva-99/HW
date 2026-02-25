# Задание 2: Класс "Банковский счет"

class BankAccount:
    # Конструктор класса - инициализирует объект при создании
    def __init__(self, account_number, owner_name, balance):
        self.account_number = account_number  # Номер счета
        self.owner_name = owner_name          # Имя владельца
        self.balance = balance                # Баланс (сумма денег)
    
    # Метод пополнения счета
    def deposit(self, amount):
        # Проверяем, что сумма положительная
        if amount > 0:
            self.balance += amount  # Увеличиваем баланс
            print(f"✅ Пополнение на {amount:.2f} руб. успешно!")
        else:
            print("❌ Сумма пополнения должна быть больше нуля!")
    
    # Метод снятия денег со счета
    def withdraw(self, amount):
        # Проверяем два условия:
        # 1. Сумма положительная
        # 2. На счету достаточно денег
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount  # Уменьшаем баланс
                print(f"✅ Снятие {amount:.2f} руб. успешно!")
            else:
                print(f"❌ Недостаточно средств! На счету: {self.balance:.2f} руб.")
        else:
            print("❌ Сумма снятия должна быть больше нуля!")
    
    # Метод для отображения информации о счете
    def display_info(self):
        print(f"\n--- Информация о счете ---")
        print(f"Номер счета: {self.account_number}")
        print(f"Владелец: {self.owner_name}")
        print(f"Баланс: {self.balance:.2f} руб.")


# Основная часть программы
if __name__ == "__main__":
    print("=== Задание 2: Банковский счет ===\n")
    
    accounts = []  # Список для хранения объектов счетов
    count = 2      # Количество счетов для создания
    
    # Создаем несколько объектов (счетов)
    for i in range(count):
        print(f"--- Создание счета №{i + 1} ---")
        
        # ЗАПРОС ДАННЫХ У ПОЛЬЗОВАТЕЛЯ 
        acc_number = input("Введите номер счета: ")
        owner = input("Введите имя владельца: ")
        # balance преобразуем в float, так как деньги могут быть с копейками
        initial_balance = float(input("Введите начальный баланс: "))
        
        # Создание объекта класса BankAccount
        new_account = BankAccount(acc_number, owner, initial_balance)
        accounts.append(new_account)
        print(f"✅ Счет для {owner} создан!\n")
    
    # Работа с каждым счетом: пополнение и снятие
    for i, account in enumerate(accounts):
        print(f"\n=== Операции со счетом №{i + 1} ===")
        account.display_info()
        
        # Пополнение
        print("\n--- Пополнение счета ---")
        deposit_amount = float(input("Введите сумму для пополнения: "))
        account.deposit(deposit_amount)  # Вызов метода объекта
        
        # Снятие
        print("\n--- Снятие со счета ---")
        withdraw_amount = float(input("Введите сумму для снятия: "))
        account.withdraw(withdraw_amount)  # Вызов метода объекта
        
        # Показываем итоговый баланс после операций
        print("\n--- Итоговое состояние ---")
        account.display_info()
    
    print("\n=== Все операции завершены ===")