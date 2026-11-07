from tokens import Token

KEYWORDS = {"если", "иначе", "пока", "возврат", "функция", "истина", "ложь", "программа"}
SINGLE = set("+-*/%=<>!(){}[],;.")
DOUBLE = {"==", "!=", "<=", ">=", "+=", "-=", "&&", "||", "++"}

class Lexer:
    def __init__(self, source: str):
        self.src = source
        self.pos = 0 # индекс текущего символа
        self.line = 1
        self.col = 1

    def advance(self) -> str:
        ch = self.src[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def peek(self, offset: int = 0) -> str:
        i = self.pos + offset
        return self.src[i] if i < len(self.src) else ""

    def tokenize(self) -> list[Token]:
        tokens = []
        while self.pos < len(self.src):
            ch = self.peek()
            if ch.isspace():
                self.advance()
            else:
                self.advance()
            # elif ch == "/" and self.peek(1) == "/":
            #     self.skip_line_comment()
            # elif ch == "/" and self.peek(1) == "*":
            #     self.skip_block_comment()
            # elif ch.isdigit() or (ch == "." and self.peek(1).isdigit()):
            #     tokens.append(self.read_number())
            # elif ch.isalpha() or ch == "_":
            #     tokens.append(self.read_identifier())
            # elif ch == '"':
            #     tokens.append(self.read_string())
            # elif ch in SINGLE:
            #     tokens.append(self.read_operator())
            # else:
            #     raise LexError(f"недопустимый символ {ch!r}", self.line, self.col)
        tokens.append(Token("EOF", "", self.line, self.col))
        return tokens
