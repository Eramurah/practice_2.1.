import math
from datetime import datetime


def logs():
    try:
        with open("calculator.log", "r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                print("Лог-файл пока пуст.")
                return
            print("\nПоследние операции:")
            for line in lines[-5:]:
                print(line, end="")
    except FileNotFoundError:
        print("Лог-файл отсутствует.")


def clear_logs():
    with open("calculator.log", "w", encoding="utf-8"):
        pass
    print("\nЛог-файл очищен.")


def write_log(expression, result):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("calculator.log", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {expression} = {result}\n")


def calculate():
    print("""\nПожалуйста, выберите:
1) Выполнить сложение;
2) Выполнить вычитание;
3) Выполнить умножение;
4) Выполнить деление;
5) Вычислить логарифм;
6) Вычислить синус;
0) Вернуться.""")

    match input("Действие: "):
        case "1":
            a = float(input("\nВведите число 'a': "))
            b = float(input("Введите число 'b': "))
            c = a + b
            print(f"Сумма равна '{c}'")
            write_log(f"Сумма чисел '{a}' и '{b}'", f"'{c}'")
            calculate()
        case "2":
            a = float(input("\nВведите число 'a': "))
            b = float(input("Введите число 'b': "))
            c = a - b
            print(f"Разность равна '{c}'")
            write_log(f"Разность чисел '{a}' и '{b}'", f"'{c}'")
            calculate()
        case "3":
            a = float(input("\nВведите число 'a': "))
            b = float(input("Введите число 'b': "))
            c = a * b
            print(f"Произведение равно '{c}'")
            write_log(f"Произведение чисел '{a}' и '{b}'", f"'{c}'")
            calculate()
        case "4":
            a = float(input("\nВведите число 'a': "))
            b = float(input("Введите число 'b': "))
            if b == 0:
                print("\nЧисло 'b' является нулем. Деление на ноль запрещено.")
            else:
                c = a / b
                print(f"Частное равно '{c}'")
                write_log(f"Частное чисел '{a}' и '{b}'", f"'{c}'")
            calculate()
        case "5":
            a = float(input("\nВведите число из которого хотите вычислить логарифм: "))
            b = math.log(a)
            print(f"Логарифм равен '{b}'")
            write_log(f"Логарифм числа '{a}'", f"'{b}'")
            calculate()
        case "6":
            a = float(input("\nВведите число из которого хотите вычислить синус: "))
            b = math.sin(a)
            print(f"Синус равен '{b}'")
            write_log(f"Синус числа '{a}'", f"'{b}'")
            calculate()
        case _:
            print()
            menu()


def menu():
    logs()

    print("""\nПожалуйста, выберите:
1) Вычислить;
2) Очистить логи;
0) Завершить работу.""")

    match input("Действие: "):
        case "1":
            calculate()
            menu()
        case "2":
            clear_logs()
            menu()
        case "0":
            print("\nЗавершение работы...")
            exit(0)
        case _:
            print()
            menu()


if __name__ == "__main__":
    menu()