class XmlTool:
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
        node = self.parse_node()
        self.skip_ws()

        if self.pos != len(self.text):
            self.error("Лишние символы после XML")

        return node

    def parse_node(self):
        self.skip_ws()

        if self.text[self.pos] != "<":
            self.error("Ожидался тег")

        self.pos += 1

        # ❗ закрывающий тег
        if self.text[self.pos] == "/":
            self.error("Неожиданный закрывающий тег")

        name = self.read_name()

        attrs = self.read_attributes()

        self.skip_ws()

        # 👉 self-closing tag <tag/>
        if self.text.startswith("/>", self.pos):
            self.pos += 2
            return {"name": name, "attrs": attrs, "children": [], "text": ""}

        if self.text[self.pos] != ">":
            self.error("Ожидался '>'")
        self.pos += 1

        children = []
        text = ""

        while True:
            self.skip_ws()

            # закрытие </tag>
            if self.text.startswith(f"</{name}>", self.pos):
                self.pos += len(name) + 3
                break

            if self.text[self.pos] == "<":
                children.append(self.parse_node())
            else:
                text += self.read_text()

        return {
            "name": name,
            "attrs": attrs,
            "children": children,
            "text": text.strip()
        }

    def read_name(self):
        start = self.pos
        while self.pos < len(self.text) and (
            self.text[self.pos].isalnum() or self.text[self.pos] in "_-"
        ):
            self.pos += 1

        if start == self.pos:
            self.error("Пустое имя тега")

        return self.text[start:self.pos]

    def read_attributes(self):
        attrs = {}

        while True:
            self.skip_ws()

            if self.pos >= len(self.text):
                self.error("Неожиданный конец")

            if self.text[self.pos] in [">", "/"]:
                break

            name = self.read_name()

            self.skip_ws()
            if self.text[self.pos] != "=":
                self.error("Ожидался '='")
            self.pos += 1

            self.skip_ws()
            if self.text[self.pos] != '"':
                self.error("Ожидались кавычки")
            self.pos += 1

            value = ""
            while self.pos < len(self.text) and self.text[self.pos] != '"':
                value += self.text[self.pos]
                self.pos += 1

            if self.pos >= len(self.text):
                self.error("Не закрыты кавычки")

            self.pos += 1
            attrs[name] = value

        return attrs

    def read_text(self):
        start = self.pos

        while self.pos < len(self.text) and self.text[self.pos] != "<":
            if self.text[self.pos] == "\n":
                self.line += 1
            self.pos += 1

        return self.text[start:self.pos]

    @staticmethod
    def serialize(node, indent=0, step=2): #Сериализация
        space = " " * indent

        attrs = ""
        for k, v in node.get("attrs", {}).items():
            attrs += f' {k}="{v}"'

        children = node.get("children", [])
        text = node.get("text", "")

        if not children and not text:
            return f"{space}<{node['name']}{attrs}/>\n"

        result = f"{space}<{node['name']}{attrs}>"

        if text:
            result += text

        if children:
            result += "\n"
            for c in children:
                result += XmlTool.serialize(c, indent + step, step)
            result += space

        result += f"</{node['name']}>\n"
        return result

    @staticmethod
    def pretty(node, indent=4):
        return XmlTool.serialize(node, 0, indent)


if __name__ == "__main__":
    with open("test.xml", "r", encoding="utf-8") as file:
        try:
            tool = XmlTool(file.read())
            root = tool.parse()

            print("--- Корректный XML ---\n")
            print(XmlTool.pretty(root, indent=4))

        except Exception as e:
            print(f"--- Ошибка: ---\n{e}")

        file.close()