import os

DIVISOR = 73**2 + 29


def process_numbers(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Ошибка: Файл {input_file} не найден.")
        return

    with open(input_file, 'r') as text, open(output_file, 'w') as file:
        for line in text:
            try:
                num = float(line.strip())

                if num % 7 == 0:
                    result = num * 100 / DIVISOR
                    file.write(f"{result}\n")
                else:
                    file.write(f"{num}\n")

            except ValueError:
                continue

        text.close(), file.close()


def testfile():
    with open("data.txt", "w", encoding="utf-8") as file:
        a = 1
        for i in range(100):
            file.write(str(a) + "\n")
            a = a + 1
        file.close()


if __name__ == "__main__":
    process_numbers('data.txt', 'results.txt')
