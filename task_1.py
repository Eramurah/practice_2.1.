try:
    with open("text.txt", "w", encoding='utf-8') as file:

        print("Введите строки:")

        for i in range(5):
            file.write(input(f"{i + 1})") + "\n")

        file.close()

except Exception as ex:
    print(ex)

try:
    counter = open("text.txt", "r", encoding='utf-8') #Строки

    a = len(counter.readlines())
    print("Количество строк:", str(a))

    counter.close()

    with open("text.txt", "r", encoding='utf-8') as counter: #Слова

        b = 0
        for line in counter:
            b += len(line.split())

        counter.close()

    print("Количество слов:", str(b))

except Exception as ex:
    print(ex)

try:
    with open("text.txt", "r", encoding="utf-8") as file:

        max_line = ""

        for line in file:
            if len(line) > len(max_line):
                max_line = line

        if "\n" in max_line:
            max_line = max_line.replace("\n", "")

        print("Самая длинная строка:", max_line)

except Exception as ex:
    print(ex)

try:
    with open("text.txt", "r", encoding="utf-8") as file:

        letters = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяabcdefghijklmnopqrstuvwxyz"
        text = file.read().lower(); d = 0

        for char in text:
            if char in letters:
                d += 1

        file.close()

    print("Общее количество гласных и согласных букв:", str(d))

except Exception as ex:
    print(ex)