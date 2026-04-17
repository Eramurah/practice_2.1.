try:
    with open("students.txt", "r", encoding="utf-8") as file:
        file.close()
except:
    e = input("""Файл "students.txt" не был найден.
Заполнить вручную? Да | Нет:
- """)
    if (e.lower() == "да") or (e.lower() == "lf"):
        with open("students.txt", "w", encoding='utf-8') as file:
            print("\nВведите данные (для завершения ввода данных оставьте строку пустой):")
            d = 0
            a = ' '
            while a != '':
                a = input(f"{d + 1})")
                if a == '':
                    break
                file.write(a + "\n")
                d = d + 1
            file.close()
    else:
        exit(0)


b = {}
with open("students.txt", "r", encoding="utf-8") as text:
    for line in text:
        line = line.strip()
        if not line:
            continue
        try:
            name, grades = line.split(":")
            c = list(map(int, grades.split(",")))
            average = sum(c) / len(c)
        except:
            print("\nНе все данные в строках были введены верно. Соответствующие строки были пропущены.")
        b[name] = average
    text.close()


with open("result.txt", "w", encoding="utf-8") as result:
    for name, avg in b.items():
        if avg > 4.0:
            result.write(f"{name}:{avg}\n")
    result.close()


try:
    max_student = max(b, key=b.get)
except:
    pass


try:
    min_student = min(b, key=b.get)
except:
    pass


print("\nСтудент с наивысшим средним баллом:")
try:
    print(f"{max_student}: {b[max_student]}")
except:
    print("Недостаточно данных для вывода наивысшего балла.")


print("\nСтудент с наименьшим средним баллом:")
try:
    print(f"{min_student}: {b[min_student]}")
except:
    print("Недостаточно данных для вывода наименьшего балла.")

