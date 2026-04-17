def fun_1(input_path, output_path, key, decrypt=False):
    with open(input_path, 'rb') as f:
        data = f.read()

    result = bytearray()
    for byte in data:
        if not decrypt: # Шифрование: Сдвиг влево на 2, затем XOR
            processed = ((byte << 2) | (byte >> 6)) & 0xFF
            processed ^= key
        else: # Дешифрование: Сначала XOR, затем сдвиг вправо на 2
            byte ^= key
            processed = ((byte >> 2) | (byte << 6)) & 0xFF

        result.append(processed)

    with open(output_path, 'wb') as f:
        f.write(result)


def main():
    print("""\nПожалуйста, выберите:
1) Шифровать;
2) Дешифровать;
0) Завершить работу.""")

    match input("Выберите действие: "):
        case "1":
            a = 'encrypted.bin'
            try:
                fun_1(str(input("\nВведите полное название файла, который хотите зашифровать: ")), a, 0x42)
            except IOError:
                print("Данный файл не найден.")
                main()

            print(f"Файл зашифрован в '{a}'")
            main()

        case "2":
            a = str(input("\nВведите полное название файла, который хотите расшифровать: "))
            b = 'decrypted' + str(input("Введите формат файла: "))
            try:
                fun_1(a, b, 0x42, decrypt=True)
            except IOError:
                print("Данный файл не найден.")
                main()

            print(f"Файл расшифрован в '{b}'")
            main()

        case "0":
            print("\nЗавершение работы...")
            exit(0)

        case _:
            main()


if __name__ == "__main__":
    main() # 0x42 - 1 байт (ключ)