class JsonTool:
    def __init__(self, text=""):
        self.text = text
        self.pos = 0
        self.line = 1

    def error(self, msg):
        raise Exception(f"[Строка {self.line}] Ошибка: {msg}")

    def skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            if self.text[self.pos] == "\n":
                self.line += 1
            self.pos += 1

    def parse(self): #Десериализация
        self.skip_ws()
        value = self.parse_value()
        self.skip_ws()

        if self.pos != len(self.text):
            self.error("Лишние символы после JSON")

        return value

    def parse_value(self):
        self.skip_ws()

        if self.pos >= len(self.text):
            self.error("Непредвиденный конец")

        ch = self.text[self.pos]

        if ch == "{":
            return self.parse_object()
        if ch == "[":
            return self.parse_array()
        if ch == '"':
            return self.parse_string()
        if ch.isdigit() or ch == "-":
            return self.parse_number()

        if self.text.startswith("true", self.pos):
            self.pos += 4
            return True
        if self.text.startswith("false", self.pos):
            self.pos += 5
            return False
        if self.text.startswith("null", self.pos):
            self.pos += 4
            return None

        self.error("Неизвестное значение")

    def parse_object(self):
        obj = {}
        self.pos += 1

        self.skip_ws()
        if self.text[self.pos] == "}":
            self.pos += 1
            return obj

        while True:
            self.skip_ws()

            if self.text[self.pos] != '"':
                self.error("Ожидался ключ")

            key = self.parse_string()

            self.skip_ws()
            if self.text[self.pos] != ":":
                self.error("Ожидался ':'")
            self.pos += 1

            value = self.parse_value()
            obj[key] = value

            self.skip_ws()

            if self.text[self.pos] == "}":
                self.pos += 1
                return obj
            elif self.text[self.pos] == ",":
                self.pos += 1
            else:
                self.error("Ожидался ',' или '}'")

    def parse_array(self):
        arr = []
        self.pos += 1

        self.skip_ws()
        if self.text[self.pos] == "]":
            self.pos += 1
            return arr

        while True:
            arr.append(self.parse_value())
            self.skip_ws()

            if self.text[self.pos] == "]":
                self.pos += 1
                return arr
            elif self.text[self.pos] == ",":
                self.pos += 1
            else:
                self.error("Ожидался ',' или ']'")

    def parse_string(self):
        self.pos += 1
        result = ""

        while self.pos < len(self.text):
            ch = self.text[self.pos]

            if ch == '"':
                self.pos += 1
                return result

            if ch == "\\":
                self.pos += 1
                if self.pos >= len(self.text):
                    self.error("Некорректный escape")

                esc = self.text[self.pos]
                escapes = {'"': '"', '\\': '\\', 'n': '\n', 't': '\t'}

                if esc in escapes:
                    result += escapes[esc]
                else:
                    self.error("Неизвестный escape")
            else:
                result += ch

            self.pos += 1

        self.error("Строка не закрыта")

    def parse_number(self):
        start = self.pos

        while self.pos < len(self.text) and self.text[self.pos] in "-0123456789.eE":
            self.pos += 1

        num_str = self.text[start:self.pos]

        try:
            if "." in num_str or "e" in num_str or "E" in num_str:
                return float(num_str)
            return int(num_str)
        except:
            self.error("Некорректное число")

    @staticmethod
    def serialize(obj, indent=0, step=2): #Сериализация
        space = " " * indent

        if obj is None:
            return "null"
        if isinstance(obj, bool):
            return "true" if obj else "false"
        if isinstance(obj, (int, float)):
            return str(obj)
        if isinstance(obj, str):
            return '"' + obj.replace('"', '\\"') + '"'

        if isinstance(obj, list):
            if not obj:
                return "[]"

            result = "[\n"
            for i, item in enumerate(obj):
                result += " " * (indent + step)
                result += JsonTool.serialize(item, indent + step, step)
                if i < len(obj) - 1:
                    result += ","
                result += "\n"
            result += space + "]"
            return result

        if isinstance(obj, dict):
            if not obj:
                return "{}"

            result = "{\n"
            items = list(obj.items())

            for i, (k, v) in enumerate(items):
                result += " " * (indent + step)
                result += f'"{k}": {JsonTool.serialize(v, indent + step, step)}'
                if i < len(items) - 1:
                    result += ","
                result += "\n"

            result += space + "}"
            return result

        raise TypeError("Неподдерживаемый тип")

    @staticmethod
    def pretty(obj, indent=4):
        return JsonTool.serialize(obj, 0, indent)


if __name__ == "__main__":
    with open("test.json", "r", encoding="utf-8") as file:
        try:
            tool = JsonTool(file.read())
            data = tool.parse()

            print("--- Корректный JSON ---\n")
            print(JsonTool.pretty(data, indent=4))

        except Exception as e:
            print(f"--- Ошибка: ---\n{e}")

        file.close()