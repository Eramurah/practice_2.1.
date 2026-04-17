import json
import os


class Library:
    def __init__(self):
        self.books = []
        self.load()


    def load(self):
        if os.path.exists("library.json"):
            with open("library.json", "r", encoding="utf-8") as file:
                self.books = json.load(file)
        else:
            self.books = []


    def save(self):
        with open("library.json", "w", encoding="utf-8") as file:
            json.dump(self.books, file, indent=4, ensure_ascii=False)


    def show(self):
        if not self.books:
            print("\nКниг нет.")
            return

        print()
        for book in self.books:
            if book["available"]:
                status = "Доступна"
            else:
                status = "Взята"
            print(f'ID: {book["id"]} | {book["title"]} - {book["author"]} | {status}')

    def search(self, query):
        results = []
        query = query.lower()

        for b in self.books:
            title = b["title"].lower()
            author = b["author"].lower()

            if (query in title) or (query in author):
                results.append(b)

        if not results:
            print("Ничего не найдено")
            return

        for book in results:
            if book["available"]:
                status = "Доступна"
            else:
                status = "Взята"
            print(f'ID: {book["id"]} | {book["title"]} - {book["author"]} | {status}')


    def add_book(self, title, author):
        max_id = 0
        for b in self.books:
            if b["id"] > max_id:
                max_id = b["id"]

        new_id = max_id + 1

        self.books.append({
            "id": new_id,
            "title": title,
            "author": author,
            "available": True
        })

        self.save()
        print("\nКнига добавлена")


    def toggle_status(self, book_id):
        for book in self.books:
            if book["id"] == book_id:
                book["available"] = not book["available"]
                self.save()
                print("Статус обновлен")
                return

        print("Книга не найдена")


    def delete_book(self, book_id):
        for book in self.books:
            if book["id"] == book_id:
                self.books.remove(book)
                self.save()
                print("Книга удалена")
                return

        print("Книга не найдена")


    def export_available(self):
        available_books = []

        for b in self.books:
            if b["available"]:
                available_books.append(b)

        with open("available_books.txt", "w", encoding="utf-8") as f:
            for book in available_books:
                f.write(f'{book["title"]} - {book["author"]}\n')

        print("\nЭкспортировано.")


def main():
    lib = Library()

    print("""\nПожалуйста, выберите:
1) Вывести список книг;
2) Найти книгу;
3) Добавить книгу;
4) Изменить статус;
5) Удалить книгу;
6) Экспорт списка доступных книг;
0) Завершить работу.""")

    match input("Выберите действие: "):
        case "1":
            lib.show()
            main()
        case "2":
            q = input("\nВведите название или автора: ")
            lib.search(q)
            main()
        case "3":
            title = input("\nНазвание: ")
            author = input("Автор: ")
            lib.add_book(title, author)
            main()
        case "4":
            book_id = int(input("\nID книги: "))
            lib.toggle_status(book_id)
            main()
        case "5":
            book_id = int(input("\nID книги: "))
            lib.delete_book(book_id)
            main()
        case "6":
            lib.export_available()
            main()
        case "0":
            print("\nЗавершение работы...")
            exit(0)
        case _:
            main()


if __name__ == "__main__":
    main()