import csv

FILENAME = "products.csv"
SORTED_FILENAME = "sorted_products.csv"


def load_products():
    products = []
    try:
        with open(FILENAME, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                name, price, quantity = row
                products.append({"Название": name, "Цена": float(price), "Количество": int(quantity)})
    except FileNotFoundError:
        print("Файл не найден.")
    return products


def save_products(products):
    with open(FILENAME, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for p in products:
            writer.writerow([p["Название"], p["Цена"], p["Количество"]])
    file.close()

    sorted_products = sorted(products, key=lambda x: x["Цена"])
    with open(SORTED_FILENAME, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for p in sorted_products:
            writer.writerow([p["Название"], p["Цена"], p["Количество"]])
    file.close()


def add(products):
    name = input("\nВведите название товара: ")
    price = float(input("Введите цену (руб): "))
    quantity = int(input("Введите количество (шт): "))

    products.append({"Название": name, "Цена": price, "Количество": quantity})
    print("\nТовар был добавлен.")

    save_products(products)


def find(products):
    name = input("\nВведите название для поиска: ")
    for p in products:
        if p["Название"].lower() == name.lower():
            print(f'Найдено: {p["Название"]}, цена: {p["Цена"]}, количество: {p["Количество"]}')
            return
    print("Товар не найден.")


def total(products):
    a = sum(p["Цена"] * p["Количество"] for p in products)
    print(f"\nОбщая стоимость всех товаров: {a}")


def main():
    products = load_products()

    print("""\nПожалуйста, выберите:
1) Показать товары;
2) Добавить товар;
3) Найти товары;
4) Общая стоимость;
0) Завершить работу.""")

    choice = input("Действие: ")

    if choice == "1":
        print()
        for p in products:
            print(p)
        main()
    elif choice == "2":
        add(products)
        main()
    elif choice == "3":
        find(products)
        main()
    elif choice == "4":
        total(products)
        main()
    elif choice == "0":
        save_products(products)
        print("\nЗавершение работы...")
        exit(0)
    else:
        main()


if __name__ == "__main__":
    main()