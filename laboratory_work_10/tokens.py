from dataclasses import dataclass

@dataclass
class Token:
    type: str # KW, ID, INT, FLOAT, STR, OP, SEP, EOF
    value: str # исходный текст лексемы
    line: int # номер строки (с 1)
    col: int # номер столбца (с 1)

    def __repr__(self) -> str:
        return f"{self.type}({self.value!r}) [{self.line}:{self.col}]"