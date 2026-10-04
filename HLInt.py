"""HLInt.py - a simple interpreter for the hypothetical language HL.

Usage:  python HLInt.py PROG1.HL

Steps (per CSS125P project specification):
  1. Read the HL source file.
  2. Remove all spaces and write the result to NOSPACES.TXT.
  3. Write the reserved words and symbols found to RES_SYM.TXT.
  4. Print "ERROR" if a syntax error is found, else "NO ERROR(S) FOUND".
  5. If there are no errors, execute the program and show its output.
"""
import operator
import re
import sys
from collections import namedtuple

KEYWORDS = ("integer", "double", "output", "if")
TYPES = ("integer", "double")
RELOPS = {">": operator.gt, "<": operator.lt, "==": operator.eq, "!=": operator.ne}

TOKEN_RE = re.compile(r"""
    (?P<NEWLINE>\n)
  | (?P<SPACE>[ \t\r\f\v]+)
  | (?P<STRING>["“”][^"“”\n]*["“”])
  | (?P<NUMBER>\d+(?:\.\d+)?)
  | (?P<NAME>[A-Za-z_]\w*)
  | (?P<SYMBOL>:=|<<|==|!=|[:;+\-=<>()])
  | (?P<BAD>.)
""", re.VERBOSE)

Token = namedtuple("Token", "kind value line")


class HLError(Exception):
    def __init__(self, line, message):
        super().__init__(f"line {line}: {message}")
        self.line = line


def strip_spaces(source):
    """Remove every whitespace character (spaces, tabs, newlines)."""
    return "".join(source.split())


def tokenize(source):
    """Split source into tokens. Invalid characters become BAD tokens so the
    parser can report them after RES_SYM.TXT has been written."""
    tokens, line = [], 1
    for m in TOKEN_RE.finditer(source):
        kind, value = m.lastgroup, m.group()
        if kind == "NEWLINE":
            line += 1
            continue
        if kind == "SPACE":
            continue
        if kind == "NAME":
            value = value.lower()  # case-insensitive: spec uses If / Output<<X
            kind = "KEYWORD" if value in KEYWORDS else "ID"
        elif kind == "STRING":
            value = value[1:-1]
        tokens.append(Token(kind, value, line))
    return tokens


def reserved_and_symbols(tokens):
    """Unique reserved words and symbols, in the order they first appear."""
    words, symbols = [], []
    for tok in tokens:
        if tok.kind == "KEYWORD" and tok.value not in words:
            words.append(tok.value)
        elif tok.kind == "SYMBOL" and tok.value not in symbols:
            symbols.append(tok.value)
        elif tok.kind == "STRING" and '"' not in symbols:
            symbols.append('"')
    return words, symbols


class Parser:
    """Recursive-descent parser. Produces a list of statement tuples:
        ("decl",   line, name, type)
        ("assign", line, name, expr)
        ("output", line, str_or_expr)
        ("if",     line, left_expr, relop, right_expr, statement)
    An expr is a list of (sign, operand).
    An operand is ("num", value) or ("var", name).
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.types = {}  # declared variable -> "integer" | "double"

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def error(self, message, previous=False):
        # A missing token is reported on the line of the last token read.
        if previous or self.peek() is None:
            tok = self.tokens[self.pos - 1] if self.pos else None
        else:
            tok = self.peek()
        raise HLError(tok.line if tok else 1, message)

    def found(self):
        tok = self.peek()
        return f", found '{tok.value}'" if tok else ", reached end of file"

    def accept(self, value):
        tok = self.peek()
        if tok and tok.kind in ("SYMBOL", "KEYWORD") and tok.value == value:
            self.pos += 1
            return True
        return False

    def expect(self, value):
        if not self.accept(value):
            if self.peek() and self.peek().kind == "BAD":
                self.error(f"invalid character '{self.peek().value}'")
            self.error(f"expected '{value}'{self.found()}", previous=True)

    def parse(self):
        statements = []
        while self.peek():
            statements.append(self.statement())
        return statements

    def statement(self, in_if=False):
        tok = self.peek()
        if tok is None:
            self.error("expected a statement after if(...)")
        if tok.kind == "BAD":
            self.error(f"invalid character '{tok.value}'")
        line = tok.line

        if self.accept("output"):
            self.expect("<<")
            nxt = self.peek()
            if nxt and nxt.kind == "STRING":
                self.pos += 1
                value = nxt.value
            else:
                value = self.expr()
            self.expect(";")
            return ("output", line, value)

        if self.accept("if"):
            self.expect("(")
            left = self.expr()
            op = self.peek()
            if not (op and op.kind == "SYMBOL" and op.value in RELOPS):
                self.error("expected relational operator (>, <, ==, !=)"
                           + self.found())
            self.pos += 1
            right = self.expr()
            self.expect(")")
            return ("if", line, left, op.value, right, self.statement(in_if=True))

        if tok.kind == "ID":
            name = tok.value
            self.pos += 1
            if self.accept(":"):
                if in_if:
                    raise HLError(line, "declaration is not allowed inside if")
                typ = self.peek()
                if not (typ and typ.kind == "KEYWORD" and typ.value in TYPES):
                    self.error("expected data type 'integer' or 'double'"
                               + self.found())
                self.pos += 1
                self.expect(";")
                if name in self.types:
                    raise HLError(line, f"variable '{name}' is already declared")
                self.types[name] = typ.value
                return ("decl", line, name, typ.value)
            if self.accept(":=") or self.accept("="):
                self.check_declared(name, line)
                expr = self.expr()
                if (self.types[name] == "integer"
                        and self.expr_type(expr) == "double"):
                    raise HLError(line, "cannot assign a double value to "
                                        f"integer variable '{name}'")
                self.expect(";")
                return ("assign", line, name, expr)
            self.error(f"expected ':', ':=' or '=' after '{name}'{self.found()}")

        self.error(f"unexpected '{tok.value}'")

    def expr(self):
        terms = [("+", self.operand())]
        while ((tok := self.peek()) and tok.kind == "SYMBOL"
               and tok.value in ("+", "-")):
            self.pos += 1
            terms.append((tok.value, self.operand()))
        return terms

    def operand(self):
        tok = self.peek()
        if tok and tok.kind == "NUMBER":
            self.pos += 1
            if "." in tok.value:
                if len(tok.value.split(".")[1]) > 2:
                    raise HLError(tok.line, f"double value '{tok.value}' has "
                                            "more than 2 decimal places")
                return ("num", float(tok.value))
            if len(tok.value) > 1:
                raise HLError(tok.line,
                              f"integer value '{tok.value}' must be a single digit")
            return ("num", int(tok.value))
        if tok and tok.kind == "ID":
            self.pos += 1
            self.check_declared(tok.value, tok.line)
            return ("var", tok.value)
        if tok and tok.kind == "BAD":
            self.error(f"invalid character '{tok.value}'")
        self.error(f"expected a number or variable{self.found()}")

    def check_declared(self, name, line):
        if name not in self.types:
            raise HLError(line, f"variable '{name}' is not declared")

    def expr_type(self, expr):
        for _, (kind, value) in expr:
            if (kind == "num" and isinstance(value, float)) or \
               (kind == "var" and self.types[value] == "double"):
                return "double"
        return "integer"


def parse(tokens):
    return Parser(tokens).parse()


def format_value(value):
    return f"{value:.2f}" if isinstance(value, float) else str(value)


def run(statements, out=print):
    """Execute parsed statements, sending each output line to `out`."""
    types, values = {}, {}

    def evaluate(expr, line):
        total = 0
        for sign, (kind, value) in expr:
            if kind == "var":
                if values.get(value) is None:
                    raise HLError(line, f"variable '{value}' is used "
                                        "before it has a value")
                value = values[value]
            total = total + value if sign == "+" else total - value
        return round(total, 2) if isinstance(total, float) else total

    def execute(stmt):
        kind, line = stmt[0], stmt[1]
        if kind == "decl":
            types[stmt[2]] = stmt[3]
            values[stmt[2]] = None
        elif kind == "assign":
            value = evaluate(stmt[3], line)
            values[stmt[2]] = float(value) if types[stmt[2]] == "double" else value
        elif kind == "output":
            value = stmt[2]
            if not isinstance(value, str):
                value = format_value(evaluate(value, line))
            out(value)
        elif kind == "if":
            _, _, left, op, right, body = stmt
            if RELOPS[op](evaluate(left, line), evaluate(right, line)):
                execute(body)

    for stmt in statements:
        execute(stmt)


def main():
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = input("Enter source file: ").strip()
    try:
        with open(path, encoding="utf-8-sig") as f:
            source = f.read()
    except OSError as e:
        print(f"Cannot open '{path}': {e.strerror}")
        return 1

    print("HLInt - HL Interpreter")
    print(f"Source file : {path}")

    with open("NOSPACES.TXT", "w", encoding="utf-8") as f:
        f.write(strip_spaces(source))

    tokens = tokenize(source)
    words, symbols = reserved_and_symbols(tokens)
    with open("RES_SYM.TXT", "w", encoding="utf-8") as f:
        f.write("RESERVED WORDS:\n")
        f.writelines(w + "\n" for w in words)
        f.write("SYMBOLS:\n")
        f.writelines(s + "\n" for s in symbols)
    print("Created     : NOSPACES.TXT, RES_SYM.TXT")
    print()

    try:
        statements = parse(tokens)
    except HLError as e:
        print("ERROR")
        print(f"  {e}")
        return 1
    print("NO ERROR(S) FOUND")

    print()
    print("Program output:")
    try:
        run(statements)
    except HLError as e:
        print(f"RUNTIME ERROR: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
