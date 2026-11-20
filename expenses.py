import datetime
import json
import os

class Expense:
    def __init__(self, amount, category, note, date=None):
        self.amount = amount
        self.category = category
        self.note = note
        if date == None:
            date = datetime.date.today().isoformat()
        self.date = date
        
    def to_dict(self):
        return {"amount": self.amount, "category": self.category, "note": self.note, "date": self.date}
    
class ExpenseTracker:
    def __init__(self, filename="expense.json"):
        self.expenses = []
        self.filename = filename
        self.load_expenses()
        
    def add_expense(self, amount, category, note):
        new_expense = Expense(amount, category, note)
        self.expenses.append(new_expense)
        self.save_expenses()
        print(f"Добавлено: {new_expense.amount} - {new_expense.category}")
        
    def show_expenses(self):
        if not self.expenses:
            print("Ничего нет!")
            return
        
        print("---Expense List---")
        for i, expense in enumerate(self.expenses, start=1):
            print(f"{i}: {expense.date} | {expense.category} | {expense.amount:.2f} | {expense.note}")
            
    def delete_expense(self, number):
        if 1 <= number <= len(self.expenses):
            removed = self.expenses.pop(number - 1)
            self.save_expenses()
            print(f"Удалено: {removed.note}")
        else:
            print("Неверный номер!")
            
    def save_expenses(self):
        data = []
        for expense in self.expenses:
            data.append(expense.to_dict())
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            
    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                for item in data:
                    expense = Expense(item["amount"], item["category"], item["note"], item["date"])
                    self.expenses.append(expense)
                    
    def show_totals(self):
        totals = {}
        if not self.expenses:
            print("Список пуст!")
            return
        for expense in self.expenses:
            if expense.category in totals:
                totals[expense.category] += expense.amount
            else:
                totals[expense.category] = expense.amount
                
        print("---Итоги---")
        for category, total in totals.items():
            print(f"{category}: {total:.2f}")
        print(f"Всего: {sum(totals.values()):.2f}")
            
    
def ask_num(prompt):
    while True:
        text = input(prompt)
        try:
            number = float(text)
            if number <= 0:
                print("Некорректная сумма!")
                continue
            return number
        except ValueError:
            print("Введите число?")
    
def main():
    expense_list = ExpenseTracker()
    
    while True:
        print("\n [1] Добавить  [2] Показать все  [3] Удалить  [4] Итоги  [5] Выйти")
        choice = input("Выберите опцию (1-5): ")
        
        if choice == "1":
            amount = ask_num("Сумма: ")
            category = input("Категория: ").strip().lower()
            note = input("Заметка: ").strip()
            expense_list.add_expense(amount, category, note)
        elif choice == "2":
            expense_list.show_expenses()
        elif choice == "3":
            expense_list.show_expenses()
            num = int(ask_num("Удалить номер: "))
            expense_list.delete_expense(num)
        elif choice == "4":
            expense_list.show_totals()
        elif choice == "5":
            print("Пака пака!")
            break
        else:
            print("Неверный ввод!")
            
if __name__ == "__main__":
    main()